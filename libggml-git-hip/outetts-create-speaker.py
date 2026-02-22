#!/usr/bin/env python3
import os
import sys

import json
import argparse

import torch
import torch.nn.functional as F
import torchaudio
import torchcodec
from torchcodec.decoders import AudioDecoder
import numpy as np
from transformers import pipeline, AutoModel, DacModel

# Text Normalization logic from OuteTTS (simplified)
def text_normalizations(text: str) -> str:
    import re
    text = re.sub(r'\s+', ' ', text)
    text = text.replace("…", "...")
    text = text.strip()
    text = re.sub(r'[“”]', '"', text)
    text = re.sub(r'[‘’]', "'", text)
    text = re.sub(r'[–—]', '-', text)
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    return text

# Feature extraction logic from OuteTTS v3
def calculate_pitch(audio_tensor, sr):
    if audio_tensor.numel() == 0:
        return torch.tensor([0.0], device=audio_tensor.device)
    if audio_tensor.dim() > 1:
        audio_tensor = torch.mean(audio_tensor, dim=0)
    audio_tensor = audio_tensor.squeeze()
    
    frame_length = 400
    hop_length = 160
    num_samples = audio_tensor.shape[-1]
    pad_len = (frame_length - (num_samples % hop_length)) % hop_length
    audio_tensor = F.pad(audio_tensor, (0, pad_len))
    
    frames = audio_tensor.unfold(0, frame_length, hop_length)
    window = torch.hann_window(frame_length, device=audio_tensor.device)
    frames_windowed = frames * window
    
    f = torch.fft.rfft(frames_windowed, n=2*frame_length, dim=1)
    power_spectrum = f.real.pow(2) + f.imag.pow(2)
    autocorr = torch.fft.irfft(power_spectrum, dim=1)[:, :frame_length]
    
    min_freq, max_freq = 75.0, 600.0
    min_idx = max(1, int(sr / max_freq))
    max_idx = min(frame_length, int(sr / min_freq))
    
    relevant_autocorr = autocorr[:, min_idx:max_idx]
    peak_values, peak_indices = torch.max(relevant_autocorr, dim=1)
    peak_indices += min_idx
    
    indices = torch.clamp(peak_indices, 1, frame_length-2)
    num_frames = frames.shape[0]
    alpha = autocorr[torch.arange(num_frames), indices-1]
    beta = autocorr[torch.arange(num_frames), indices]
    gamma = autocorr[torch.arange(num_frames), indices+1]
    
    delta = 0.5 * (alpha - gamma) / (alpha - 2*beta + gamma + 1e-8)
    best_period = (peak_indices + delta) / sr
    pitch = torch.where(best_period > 0, 1.0 / best_period, 0.0)
    
    voiced = (peak_values / (autocorr[:, 0] + 1e-8)) > 0.3
    pitch = torch.where(voiced, pitch, 0.0)
    return torch.clamp(pitch, min_freq, max_freq)

def extract_features(audio, sr, device):
    if audio.numel() == 0 or audio.shape[-1] < 10:
        return {
            "energy": 0,
            "spectral_centroid": 0,
            "pitch": 0
        }
        
    if audio.dim() == 2 and audio.shape[0] > 1:
        audio = torch.mean(audio, dim=0, keepdim=True)
    
    eps = 1e-10
    energy = float(torch.sqrt(torch.mean(audio ** 2)))
    
    spec = torch.abs(torch.fft.rfft(audio))
    freqs = torch.linspace(0, sr/2, spec.shape[-1], device=device)
    spec_sum = torch.sum(spec) + eps
    centroid = float(torch.sum(freqs * spec.squeeze()) / spec_sum / (sr/2))
    
    pitch_tensor = calculate_pitch(audio, sr)
    pitch = float((torch.mean(pitch_tensor) - 75.0) / (600.0 - 75.0))
    
    return {
        "energy": round(energy * 100),
        "spectral_centroid": round(centroid * 100),
        "pitch": round(max(0, min(1, pitch)) * 100)
    }

def create_speaker(audio_path, output_path, whisper_model="openai/whisper-large-v3-turbo", codec_model="descript/dac_24khz"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # 1. Transcription with Word Timestamps
    print(f"Transcribing {audio_path} using {whisper_model}...")
    pipe = pipeline("automatic-speech-recognition", model=whisper_model, device=device, chunk_length_s=30)
    result = pipe(audio_path, return_timestamps="word")
    
    full_text = text_normalizations(result["text"])
    words = []
    for chunk in result["chunks"]:
        words.append({
            "word": chunk["text"].strip(),
            "start": chunk["timestamp"][0],
            "end": chunk["timestamp"][1]
        })

    # 2. Audio Encoding (DAC)
    print(f"Encoding audio using {codec_model}...")
    
    # Using torchcodec for efficient audio decoding
    decoder = AudioDecoder(audio_path)
    samples = decoder.get_all_samples()
    # samples.data is [num_samples, num_channels]
    audio = samples.data.to(torch.float32)
    sr = samples.sample_rate
    
    # Normalize if it looks like int16
    if audio.abs().max() > 1.0:
        audio = audio / 32768.0
        
    # torchcodec returns [channels, samples] or [samples]
    if audio.ndim == 1:
        audio = audio.unsqueeze(0)
    elif audio.ndim == 2:
        # Check if it's [samples, channels] and fix it
        # Usually samples >> channels
        if audio.shape[0] > audio.shape[1] and audio.shape[1] < 10:
            audio = audio.T
            
    if audio.shape[0] > 1:
        audio = torch.mean(audio, dim=0, keepdim=True)
    
    if sr != 24000:
        audio = torchaudio.functional.resample(audio, sr, 24000)
    
    # Ensure minimum length for DAC encoder (at least one window)
    if audio.shape[-1] < 1024:
        audio = F.pad(audio, (0, 1024 - audio.shape[-1]))
        
    audio_tensor = audio.unsqueeze(0).to(device) # [1, 1, seq_len]
    
    # Load DAC model via transformers
    try:
        codec = DacModel.from_pretrained(codec_model).to(device)
    except Exception as e:
        print(f"Error loading DacModel: {e}. Falling back to AutoModel...")
        codec = AutoModel.from_pretrained(codec_model, trust_remote_code=True).to(device)

    # Encode audio
    with torch.no_grad():
        hop_length = getattr(codec.config, "hop_length", 320)
        outputs = codec.encode(audio_tensor)
        # DacEncoderOutput has audio_codes, not codes
        codes = outputs.audio_codes # [batch, num_codebooks, seq_len]
        
    # OuteTTS 1.0 (v3) uses the first two codebooks (c1, c2)
    # codes shape is [1, 9, seq_len] for dac_24khz
    c1 = codes[0, 0].cpu().tolist()
    c2 = codes[0, 1].cpu().tolist()
    
    tps = 24000 / hop_length
    print(f"Tokens per second: {tps}")
    
    # 3. Global and per-word features
    audio_duration = audio_tensor.shape[-1] / 24000.0
    global_features = extract_features(audio_tensor.squeeze(0), 24000, device)
    
    word_codes = []
    for word_info in words:
        start_t = word_info["start"] if word_info["start"] is not None else 0.0
        end_t = word_info["end"] if word_info["end"] is not None else audio_duration
        
        # Clamp to bounds
        start_t = max(0.0, min(start_t, audio_duration))
        end_t = max(start_t, min(end_t, audio_duration))
        
        # Calculate indices
        s_idx = int(start_t * tps)
        e_idx = int(end_t * tps)
        
        w_c1 = c1[s_idx:e_idx]
        w_c2 = c2[s_idx:e_idx]
        
        if not w_c1:
            w_c1 = [0]
            w_c2 = [0]
            
        # Word features
        word_audio = audio_tensor.squeeze(0)[:, int(start_t*24000):int(end_t*24000)]
        features = extract_features(word_audio, 24000, device)
        
        word_codes.append({
            "word": word_info["word"],
            "duration": round(len(w_c1) / tps, 2),
            "c1": w_c1,
            "c2": w_c2,
            "features": features
        })
    
    speaker_data = {
        "text": full_text,
        "words": word_codes,
        "global_features": global_features,
        "version": "1.0" # Triggers OuteTTS v1.0 logic in tts.cpp
    }
    
    with open(output_path, "w") as f:
        json.dump(speaker_data, f, indent=2)
    print(f"Speaker profile saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", help="Path to input audio file")
    parser.add_argument("--output", default="speaker.json", help="Output JSON path")
    parser.add_argument("--whisper", default="openai/whisper-large-v3-turbo", help="Whisper model ID")
    parser.add_argument("--codec", default="descript/dac_24khz", help="Codec model ID (must be a DAC model)")
    args = parser.parse_args()
    
    create_speaker(args.audio, args.output, args.whisper, args.codec)
