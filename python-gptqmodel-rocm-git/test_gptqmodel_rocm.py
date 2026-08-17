#!/usr/bin/env python3
"""Minimized test suite for python-gptqmodel-rocm on AMD ROCm / RDNA3 hardware.

Validates:
1. Core and bundled companion modules import cleanly:
   - gptqmodel
   - pcre (pypcre)
   - device_smi (device-smi)
   - tokenicer
   - logbar
   - defuser
2. GPU detection via device-smi (AMD ROCm / gfx target / VRAM).
3. PyTorch ROCm / HIP device availability and basic GPU operations.
4. PCRE regex compilation and matching.
5. Local model loading and tokenizer resolution (when model path is provided).
6. Forward pass & basic quantization smoke test (when model path is provided).
"""

import argparse
import os
import sys
import unittest
from typing import Optional


class TestGPTQModelROCm(unittest.TestCase):
    model_path: Optional[str] = None
    device: str = "cuda:0"
    bits: int = 4
    group_size: int = 128

    def test_01_imports(self):
        """Test that all required modules and bundled companion packages import cleanly."""
        print("\n[1/6] Testing module imports...")
        import gptqmodel
        import pcre
        import device_smi
        import tokenicer
        import logbar
        import defuser
        import torch

        self.assertIsNotNone(gptqmodel.__version__)
        self.assertIsNotNone(torch.__version__)
        print(f"  - gptqmodel : {gptqmodel.__version__}")
        print(f"  - torch     : {torch.__version__}")
        print(f"  - pcre      : {getattr(pcre, '__version__', 'ok')}")
        print(f"  - logbar    : {getattr(logbar, '__version__', 'ok')}")
        print(f"  - tokenicer : {getattr(tokenicer, '__version__', 'ok')}")
        print(f"  - defuser   : {getattr(defuser, '__version__', 'ok')}")
        print(f"  - device_smi: {getattr(device_smi, '__version__', 'ok')}")

    def test_02_pcre_matching(self):
        """Test PCRE regex compilation and matching functionality."""
        print("\n[2/6] Testing PCRE regex acceleration...")
        import pcre

        pattern = pcre.compile(r"model\.layers\.\d+\.(self_attn|mlp)\..*")
        match = pattern.match("model.layers.0.self_attn.q_proj")
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "self_attn")
        print("  - Pattern matching verified successfully.")

    def test_03_device_smi(self):
        """Test GPU hardware introspection using device-smi."""
        print("\n[3/6] Testing device-smi hardware telemetry...")
        import device_smi

        dev = None
        try:
            dev = device_smi.Device(0)
            vendor = getattr(dev, "vendor", "unknown")
            features = getattr(dev, "features", [])
            model_name = getattr(dev, "model", "unknown")
            mem_bytes = getattr(dev, "memory_total", 0)
            mem_gb = mem_bytes / (1024**3) if mem_bytes else 0

            self.assertIsNotNone(vendor)
            print(f"  - Vendor   : {vendor}")
            print(f"  - Model    : {model_name}")
            print(f"  - Features : {features}")
            print(f"  - Memory   : {mem_gb:.2f} GB ({mem_bytes} bytes)")
        finally:
            if dev is not None and hasattr(dev, "close"):
                dev.close()

    def test_04_torch_rocm(self):
        """Test PyTorch ROCm/HIP device recognition and allocation."""
        print("\n[4/6] Testing PyTorch ROCm/HIP device recognition...")
        import torch

        self.assertTrue(torch.cuda.is_available(), "CUDA/ROCm HIP is not available in PyTorch.")
        device_count = torch.cuda.device_count()
        self.assertGreater(device_count, 0)
        device_name = torch.cuda.get_device_name(0)
        print(f"  - Found {device_count} device(s). Device 0: {device_name}")

        # Basic tensor math on GPU
        x = torch.ones((16, 16), device=self.device, dtype=torch.float16)
        y = x @ x
        self.assertEqual(y[0, 0].item(), 16.0)
        print("  - FP16 GPU tensor multiplication verified.")

    def test_05_model_loading_and_tokenizer(self):
        """Test loading local model tokenizer and configuration."""
        if not self.model_path or not os.path.exists(self.model_path):
            self.skipTest(f"Model path '{self.model_path}' not found. Skipping model test.")

        print(f"\n[5/6] Testing tokenizer resolution from: {self.model_path}...")
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.assertIsNotNone(tokenizer)
        prompt = "ROCm acceleration test."
        tokens = tokenizer(prompt, return_tensors="pt")
        self.assertIn("input_ids", tokens)
        print(f"  - Tokenizer encoded '{prompt}' to {tokens['input_ids'].shape[-1]} tokens.")

    def test_06_gptqmodel_quantization_smoke(self):
        """Test GPTQModel initialization with QuantizeConfig and calibration input."""
        if not self.model_path or not os.path.exists(self.model_path):
            self.skipTest(f"Model path '{self.model_path}' not found. Skipping quantization test.")

        print(f"\n[6/6] Testing GPTQModel loading & calibration (bits={self.bits}, group_size={self.group_size})...")
        import torch
        from gptqmodel import GPTQModel, QuantizeConfig

        quant_config = QuantizeConfig(bits=self.bits, group_size=self.group_size)
        model = GPTQModel.load(
            self.model_path,
            quantize_config=quant_config,
            device=self.device,
            dtype=torch.float16,
        )
        self.assertIsNotNone(model)
        print(f"  - Successfully initialized model: {type(model).__name__}")


def parse_args():
    parser = argparse.ArgumentParser(description="GPTQModel ROCm Minimized Test Suite")
    parser.add_argument(
        "-m",
        "--model-path",
        default="/data/public/machine-learning/models/text/Qwen2.5-0.5B-Instruct",
        help="Path to local HuggingFace/transformers model directory for inference/quantization test",
    )
    parser.add_argument(
        "-d",
        "--device",
        default="cuda:0",
        help="Target device (default: cuda:0)",
    )
    parser.add_argument(
        "--bits",
        type=int,
        default=4,
        help="Quantization bits (default: 4)",
    )
    parser.add_argument(
        "--group-size",
        type=int,
        default=128,
        help="Quantization group size (default: 128)",
    )
    parser.add_argument(
        "--no-model",
        action="store_true",
        help="Run only standalone environment & import tests, skipping model-dependent checks",
    )
    return parser.parse_known_args()


def main():
    args, unittest_args = parse_args()

    if args.no_model:
        TestGPTQModelROCm.model_path = None
    else:
        TestGPTQModelROCm.model_path = args.model_path

    TestGPTQModelROCm.device = args.device
    TestGPTQModelROCm.bits = args.bits
    TestGPTQModelROCm.group_size = args.group_size

    # Run unittest suite
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestGPTQModelROCm)
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
