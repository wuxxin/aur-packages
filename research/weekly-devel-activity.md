# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

**Recreating this Analysis**: You can run the automation script `scripts/update-activity.py` with the `--write` (or `-w`) flag to automatically pull all repository updates, calculate the statistics, and optionally write the updated tables directly back into this file:
```bash
python scripts/update-activity.py [--write]
```



## 📅 Summary

<!-- START_DATE -->
**Last 7 Days Activity (November 17, 2026 – November 24, 2026)**
<!-- END_DATE -->

<!-- START_TABLES -->
| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **amux-git** | [mixpeek/amux](https://github.com/mixpeek/amux) | 363 | 39 | `main` | 2026-11-24 | **190** | 0 | 1 | 335.2 | `desktop-latest` | `0.1.0.r3681.g3ba5e733-1` (ref `3ba5e733`) | 5845 | **Highly Active** |
| **aoe-git-tag** | [agent-of-empires/agent-of-empires](https://github.com/agent-of-empires/agent-of-empires) | 3,118 | 321 | `main` | 2026-11-24 | **91** | 0 | 7 | 112.2 | `nightly-20261119`, `nightly-20261120` | `1.15.0.r0.gb90c4b0-1` (ref `b90c4b0`) | 1247 | **Highly Active** |
| *└─ llama.cpp* | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 125,181 | 22,029 | `master` | 2026-11-24 | **224** | 0 | 137 | 193.5 | `b12491`, `b12492` | `12550.r4.g7fce543-1` (ref `7fce543`) | 160 | **Highly Active** |
| *└─ whisper.cpp* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 53,105 | 6,087 | `master` | 2026-11-24 | **20** | 0 | 2 | 81.8 | `b5907`, `v1.9.6` | `12550.r4.g7fce543-1` (ref `ca19af2`) | 14 | **Active** |
| *└─ llama-cpp-python* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,572 | 1,444 | `main` | 2026-11-23 | **11** | 0 | 5 | 4.0 | `v0.3.38`, `v0.3.38-hip-radeon` | `12550.r4.g7fce543-1` (ref `3691546`) | 20 | **Active** |
| *└─ stable-diffusion.cpp* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,817 | 745 | `master` | 2026-11-24 | **21** | 0 | 9 | 27.5 | `master-1111-6874e49`, `master-1116-bf31b9c` | `12550.r4.g7fce543-1` (ref `532d2c1`) | 21 | **Active** |
| *└─ qwen3-tts.cpp* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) | 0 | 0 | `main` | 2026-06-16 | 0 | 0 | 0 | 0.0 | — | `12550.r4.g7fce543-1` (ref `0c8b2ba`) | 0 | **Stale** |
| *└─ parakeet.cpp* | [mudler/parakeet.cpp](https://github.com/mudler/parakeet.cpp) | 0 | 0 | `master` | 2026-10-30 | 0 | 0 | 0 | 0.8 | — | `12550.r4.g7fce543-1` (ref `e75de9b`) | 41 | **Stale** |
| **strata-engine-git-hip** | [Niko1221/Strata](https://github.com/Niko1221/Strata) | 0 | 0 | `main` | 2026-11-24 | **837** | 176 | 6 | 836.5 | `v0.2.16`, `v0.2.17` | `0.2.16.r4.g58ee322-1` (ref `58ee322`) | 766 | **Highly Active** |
| **oh-my-pi-git** | [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) | 0 | 0 | `main` | 2026-11-24 | **1342** | 451 | 6 | 1408.0 | `v18.22.1`, `v18.22.2` | `19.1.1.r184.g0aefd54-1` (ref `0aefd54`) | 141 | **Highly Active** |
| **pocket-tts.cpp-git** | [VolgaGerm/PocketTTS.cpp](https://github.com/VolgaGerm/PocketTTS.cpp) | 0 | 0 | `master` | 2026-03-29 | 0 | 0 | 0 | 0.0 | — | `0.1.0.r18.ge801e7d-1` (ref `e801e7d`) | 0 | **Stale** |
| **python-bitsandbytes-rocm-git** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 0 | 0 | `main` | 2026-10-27 | 0 | 0 | 0 | 0.2 | — | `0.50.2.r2.g83364904-1` (ref `83364904`) | 1 | **Stale** |
| **python-gptqmodel-rocm-git** | [ModelCloud/GPTQModel](https://github.com/ModelCloud/GPTQModel) | 0 | 0 | `main` | 2026-11-24 | **665** | 0 | 5 | 393.0 | `v7.11.1`, `v7.11.2` | `7.3.2.r31.g7df3d1e83-1` (ref `7df3d1e83`) | 1990 | **Highly Active** |
| **signal-cli-rest-api-git** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 0 | 0 | `master` | 2026-11-21 | **3** | 1 | 2 | 1.5 | `0.102`, `0.102-pre` | `0.101.pre.r1.gebb7c1d-1` (ref `ebb7c1d`) | 26 | **Active** |
| **vllm.cpp-git-hip** | [mudler/vllm.cpp](https://github.com/mudler/vllm.cpp) | 0 | 0 | `main` | 2026-11-24 | **93** | 0 | 0 | 66.5 | — | `0.0.2.r829.g7481a2e-1` (ref `7481a2e`) | 3121 | **Highly Active** |
| **python-optimum-amd** | [huggingface/optimum-amd](https://github.com/huggingface/optimum-amd) | 0 | 0 | `main` | 2026-10-14 | 0 | 0 | 0 | 0.0 | — | `0.1.0.r63.gf36a96b-1` (ref `f36a96b`) | 4 | **Stale** |
| **smg** | [lightseekorg/smg](https://github.com/lightseekorg/smg) | 0 | 0 | `main` | 2026-11-24 | **1408** | 0 | 0 | 818.2 | — | not installed | - | **Highly Active** |
| **tei-rocm** | [huggingface/text-embeddings-inference](https://github.com/huggingface/text-embeddings-inference) | 0 | 0 | `main` | 2026-11-24 | **5** | 0 | 0 | 10.0 | — | `1.9.3-6` (ref `v1.9.3`) | 66 | **Active** |
| **python-optimum-rocm** | [huggingface/optimum](https://github.com/huggingface/optimum) | 0 | 0 | `main` | 2026-11-02 | 0 | 0 | 0 | 1.2 | `2.3.0` | `2.3.0-2` (ref `v2.3.0`) | - | **Stale** |
| **python-peft** | [huggingface/peft](https://github.com/huggingface/peft) | 0 | 0 | `main` | 2026-11-24 | **17** | 0 | 1 | 19.0 | `0.22.0` | `0.22.0-1` (ref `v0.22.0`) | - | **Active** |
| **python-pocket-tts** | [kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts) | 0 | 0 | `main` | 2026-11-23 | **3** | 0 | 0 | 5.2 | `4.0.1` | `2.1.0-1` (ref `v2.1.0`) | - | **Active** |
| **python-infinity-emb** | [michaelfeil/infinity](https://github.com/michaelfeil/infinity) | 0 | 0 | `main` | 2026-11-12 | 0 | 0 | 0 | 26.2 | `0.0.80` | `0.0.75-3` (ref `0.0.75`) | - | **Stale** |
<!-- END_TABLES -->

---

## 🔍 Repository Focus & Developments Details

<!-- START_DETAILS -->
### amux-git (`mixpeek/amux`)
* **Status**: Highly Active (190 commits, 1 tag/release in the last week). **5845 commits since installed 0.1.0.r3681.g3ba5e733-1 (ref `3ba5e733`).**
* **Recent Focus**:
  - `61e05573` docs(ux): the button audit lists the CRM tab's touch Done button
  - `a65674bc` feat(crm): GitHub stargazers of a repo become people in the CRM, enrollable in a sequence
  - `32e7762c` fix(crm): the next sequence step passes the outbound checks, and a refused approval says why
  - `e1e298b9` feat(crm): outbound sequences across online and offline touch points, personal briefs, due events and guardrails
  - `85fd8243` feat(seo): top Cloud box on /features/ (EXP-167), 29 guides into llms.txt, EXP-163 first read
  - `3959300c` feat(requests): a landed request says what its land tested, from the gate's receipt
  - `e0af8b17` feat(crm): amux Cloud signups reach the CRM as a person, a company, a deal and a crm.signup event
  - `7c2d45b7` feat(land): a carry asks the repo which deploying members its tree changes
  - `f6f21c98` docs(pr-handling): 2026-11-24, the worker-lifecycle red that held #490's land
  - `3d00d709` fix(peek): a just-created worker's Board switch shows once the list has it, not after the board fetch
  - `9e59cd65` docs(pr-handling): 2026-11-24 pass, #491 and #489 merged, #490 landed with its conflict resolved
  - `00f74a41` feat(dashboard): Save as default for list filters; deleting the peeked worker returns to the overview
  - `c1ec085e` Drag tabs in the in-page tab strip to reorder them, with no tab reloading (#489)
  - `47c4c430` feat(workers): a new worker's card opens from its name, before its terminal preview arrives (#491)
  - `aed2eb42` fix(network-watch): judge git and the tools that inherit its socket per destination

### aoe-git-tag (`agent-of-empires/agent-of-empires`)
* **Status**: Highly Active (91 commits, 7 tags/releases in the last week). **1247 commits since installed 1.15.0.r0.gb90c4b0-1 (ref `b90c4b0`).**
* **Recent Focus**:
  - `735a2e8c` ci(tessl): move factory loops into tessl.json with maintainer allowlist (#6020)
  - `581c45e9` chore(deps-dev): bump minimatch from 10.2.5 to 10.2.6 in /web (#5979)
  - `7a9c07d1` feat(server): set one Agent's default model in a profile, refusing a pin (#5969)
  - `462ae175` refactor(daemon): remove axum from client transport (#5987)
  - `204b9f32` fix(plugin): journal default-mode publication (#5989)
  - `3f2b78ed` fix(session): name the command-selector remedy after a reload or restart (#5930)
  - `2d223e4e` fix(server): answer a re-posted queue id the daemon already delivered (#5738)
  - `2e18bf34` ci: run macOS release builds on GetMac runners (#5986)
  - `b33999ea` fix(web): start side panels closed, with daemon-owned defaults (#5974)
  - `7b1c0145` fix(tui): mount the structured preview without blocking input (#5808)
  - `c684cd29` fix(plugin): bound pre-consent staging disk use (#5759)
  - `b6e6b30f` docs(api): document the sandbox image endpoints (#5959)
  - `9c044243` docs: correct false and stale claims on the website, docs and in-app help text (#5967)
  - `89cdc7e6` feat(acp): record the submitting surface on UserPromptSent (#5954)
  - `63d07b08` fix(cli): start a stopped structured worker from aoe acp restart (#5951)

### [libggml-git-hip] llama.cpp (`ggml-org/llama.cpp`)
* **Status**: Highly Active (224 commits, 137 tags/releases in the last week). **160 commits since installed 12550.r4.g7fce543-1 (ref `7fce543`).**
* **Recent Focus**:
  - `0ce7f213b0` ui: run Llama Chat apart from llama-server, named in config.json or npx --server (#32945)
  - `96eb41bc48` ui: fix prebuilt UI download in shallow clones (#32952)
  - `23f0c0182f` convert : fix qwen3-omni conversion (#32941)
  - `f20c5907c0` ggml-cpu: repack kernels for targets without dotprod (ARMv8.0 64-bit) for Q4_0/Q8_0 (#32142)
  - `8bf2eae708` ui: expect the Llama Chat name in the PWA manifest e2e test (#32959)
  - `5fddd0b998` ggml-cpu: add SVE-optimized q5_0 and q5_1 dot-product kernels (#30867)
  - `66a3b01b0a` server : include MCP image and audio data in tool results (#32064)
  - `d3c257a493` context : prevent excessive CPU polling without OpenMP (#32378)
  - `3090e45a86` metal : reserve the top-k scratch only for short rows (#32942)
  - `ba8521a44e` ui: smooth chat form height and working directory chip across routes (#32950)
  - `72cda4a222` vulkan: add chunked GDN replay support (#32721)
  - `922cff91e9` cuda : fuse RMS_NORM + MUL + MROPE/IMROPE and tune block size (#32500)
  - `2e779d5e70` Webui nix fix (#32645)
  - `396ed2ccea` model : Inkling 2 Mini mix() weighted sum with the scores as src0 (#32855)
  - `97bbf98fdf` ui: make Llama Chat a plain chat unless llama-server offers agent features (#32949)

### [libggml-git-hip] whisper.cpp (`ggerganov/whisper.cpp`)
* **Status**: Active (20 commits, 2 tags/releases in the last week). **14 commits since installed 12550.r4.g7fce543-1 (ref `ca19af2`).**
* **Recent Focus**:
  - `c1a240478` ci : add check for SPIRV-HeadersConfig for gpu-vulkan (#4204)
  - `3e2e46a43` ci : move ARM64 high-perf jobs to DGX Spark runners (#4206)
  - `bdcbc08e4` ci : split deploy wasm job into build and deploy (#4205)
  - `e96e4ce12` examples : add device option to whisper-bench (#4135)
  - `60fff93bc` examples : fix stereo to mono averaging with diarization (#4181)
  - `20ffd918a` ci : disable main-musa.Dockerfile from docker.yml (#4201)
  - `0d7733f7d` whisper : remove unused logits_id sort in whisper_sample_token_topk (#4187)
  - `602985ceb` whisper : clear result_all in whisper_full_parallel when VAD finds no speech (#4192)
  - `96ec4d982` ggml : revert 5922450fbce (#4200)
  - `5eaee0cc9` ci : update CUDA 11.8.0 CUBLAS version to 11.11.3.6 (#4195)
  - `258bb629a` ci : update deploy-examples-wasm workflow plugins (#4194)
  - `95b3b2f85` go : replace -fopenmp with -lgomp in cgo LDFLAGS (#4180)
  - `b5f9f6bb3` cli : fix output wts (#4183)
  - `610b7bb1f` fix: print the alignment mask size with %zu (#4167)

### [libggml-git-hip] llama-cpp-python (`abetlen/llama-cpp-python`)
* **Status**: Active (11 commits, 5 tags/releases in the last week). **20 commits since installed 12550.r4.g7fce543-1 (ref `3691546`).**
* **Recent Focus**:
  - `77fbb5d7` fix: load cached pretrained models in offline mode (#2396)
  - `74002b3a` fix(ci): install matching NVML headers for CUDA wheels (#2441)
  - `12b4de41` chore: bump version to 0.3.38 (#2439)
  - `9dd4a281` feat: update llama.cpp to f5e6915c2 (#2438)
  - `e9d42342` fix(cache): evict disk cache states incrementally in LRU order (#2400)
  - `10bd146d` fix(index): include available SHA256 hashes in wheel links (#2409)
  - `ed2a26e1` fix(server): close tokenizer config before building chat handler (#2422)
  - `4023288a` fix(cache): preserve disk cache entries on lookup (#2423)
  - `c0d5530f` fix: size Python buffers to the actual context (#2436)
  - `98c25a5b` feat: update llama.cpp to afe77e18f (#2430)
  - `7fcf2743` feat: update llama.cpp to 46eb1742d (#2426)
  - `0542f207` fix(ci): remove unsupported macOS 14 release runners (#2416)
  - `46816d22` chore: bump version to 0.3.37 (#2415)
  - `dd70c923` feat: update llama.cpp to a956a852c (#2414)
  - `05c124e3` fix(ci): use supported Python versions on Ubuntu (#2407)

### [libggml-git-hip] stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
* **Status**: Active (21 commits, 9 tags/releases in the last week). **21 commits since installed 12550.r4.g7fce543-1 (ref `532d2c1`).**
* **Recent Focus**:
  - `79dc7ca9` feat: add converter metadata to GGUF exports (#2409)
  - `ce7ef90e` feat(server): add A1111 metadata endpoints and interrupt for sdapi clients (#2349)
  - `d697a0a2` fix: keep at least one trimmed sigma in the hires refine schedule (#2361)
  - `571fc444` fix: hidream-o1-image speckle noise removal (#2407)
  - `20e2b79f` fix(lora): add in F32 when the backend rejects mixed-type addition (#2383)
  - `3b12781f` feat(server): add idle TTLs for model weights (#2406)
  - `8187e47c` ci: decouple GitHub releases from Docker builds
  - `91ed0093` fix: restore Qwen Image 2.1 prefix caching in DGL (#2405)
  - `5b80e1f2` refactor(server): use one context with on-demand model loading (#2404)
  - `6667be65` feat: support immediate LoRA merges for INT8 weights (#2403)
  - `0d71f963` fix: restore runtime LoRA tensor counts and unify automatic LoRA mode selection (#2400)
  - `bf31b9c2` fix: avoid structured binding capture for MUSA builds
  - `2c678bcf` feat: support for MOSS-Image edit LoRAs (#2203)
  - `6cd0ef1e` feat: add Diffusion Graph Language support (#2396)
  - `9e7eed71` docs(server): document browser notification on generation finish (#2318)

### [libggml-git-hip] qwen3-tts.cpp (`khimaros/qwen3-tts.cpp`)
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **0 commits since installed 12550.r4.g7fce543-1 (ref `0c8b2ba`).**
* **Recent Focus**:
  - Up to date with installed package (0 new commits).

### [libggml-git-hip] parakeet.cpp (`mudler/parakeet.cpp`)
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **41 commits since installed 12550.r4.g7fce543-1 (ref `e75de9b`).**
* **Recent Focus**:
  - `2eac2e7` fix: keep the last subsampled frame for unified mels of 8k+1 frames (#111)
  - `5ee1e3f` Add buffered streaming for the Nemotron unified ASR checkpoint (#109)
  - `4fbf4d9` feat: offline support for the Nemotron unified ASR checkpoint (#108)
  - `43dce03` feat: add an opt-in fused two-plane AVX2 kernel for five-value linears (#104)
  - `1953f6b` docs: link the parakeet-ffm Java wrapper (#100)
  - `2085b49` feat: run Phonon-2.5 packed files on a GPU backend (#105)
  - `acefbca` feat: Phonon-2.5 dense and packed CPU support (#103)
  - `5c9b0fb` fix: use 64-bit seek/tell that MSVC has in the bundle loader (#97)
  - `9a28a3c` feat: opt-in VAD run gate for the Ultra/Redux heads, and the real-recording VAD evidence (#96)
  - `2f9e8ea` docs: describe speaker embeddings from the C API
  - `f36fddc` test: cover parakeet_capi_speaker_embed_pcm
  - `e0d2d4a` feat: add parakeet_capi_speaker_embed_pcm to return a voice embedding
  - `da8bb4c` docs: the Redux trim regression was noise, keep the 0.3 default (#95)
  - `2de154c` feat: trim VAD segments to speech (default 0.3 s) and an opt-in local-confidence word filter (#94)
  - `0cca477` Update README.md by removing links and renaming section

### strata-engine-git-hip (`Niko1221/Strata`)
* **Status**: Highly Active (837 commits, 6 tags/releases in the last week). **766 commits since installed 0.2.16.r4.g58ee322-1 (ref `58ee322`).**
* **Recent Focus**:
  - `d46f5f268` test(serve): the PickSlot fixture sets slot_prompt, which _slot_prefix reads
  - `eada4591c` release prep 0.2.21: settings register regenerated after the slot-0 tie-break and the K/V reserve fix
  - `8699881ae` fix(inkling cuda): the K/V window reserve is v0.2.20's again (UNMERGED safe option, owner decides)
  - `505e6cbbe` server: with the DSpark drafter, a request prefers slot 0 unless another slot holds a real conversation (OPTION, owner decision, not for the rc)
  - `b86108d9a` release prep 0.2.21: the current pages follow the release manifest
  - `4da72cca0` release prep 0.2.21: product 0.2.20 -> 0.2.21, engine / Control 0.1.66 -> 0.1.67
  - `bf6caa2f8` test(launch): the slot-fit tests follow the dense share by compute capability (sm 8.6 keeps int8 dense, sm 8.9 and 12.0 budget BF16)
  - `38b7c8532` rc1: the probe wiring test changes the context, not the slot count, to make another placement (the key no longer holds the slots)
  - `3f57f139d` probe: the placement key no longer contains the slot count (rc1 started --draft off above 1 slot)
  - `e06542eea` fix(launch): Inkling on NVIDIA defaults to the number of slots whose K/V stays on the card, not the VRAM table's
  - `479b9bcf5` fix(inkling cuda): growing the global K/V never ends the engine; the host tail is the whole rest of the context (#6905)
  - `751d55647` fix(inkling cuda): the auto prefill chunk leaves room for the K/V that still has to grow (regression fix for faceebb50)
  - `6a6e56d55` serve: the crash-loop limit leaves a missing engine program alone (fixes serve.test_ready_timeout.SpawnFailure after 264b155dd)
  - `8653f807a` packaging: a later build-feed pass refreshes the feed folder's strata-feed-linux-aarch64.json copy (make_local_feed.py wrote it after its own pass, so a feed with the shape engines kept a stale ARM64 file)
  - `264b155dd` serve: stop starting an engine that keeps dying, and say why (#6896 #6830 #6849)

### oh-my-pi-git (`can1357/oh-my-pi`)
* **Status**: Highly Active (1342 commits, 6 tags/releases in the last week). **141 commits since installed 19.1.1.r184.g0aefd54-1 (ref `0aefd54`).**
* **Recent Focus**:
  - `8f6cd5955d2` fix(cli): make --no-tools a restricted session
  - `26702495a57` fix(ci): packed packages/tui in the tarball install smoke
  - `8c6a37f4641` test(coding-agent): realigned suites with the reactive tui rewrite
  - `79ab6884e02` test(agent): realigned filtered-reasoning tokenizer fixtures and prompt pool
  - `1e641c4853b` test(tui): skipped corpus parity suites when the corpus is absent
  - `25377ff0524` style: applied oxfmt to files that drifted
  - `a13f81949d3` fix(coding-agent): settled retired transcript blocks and git help key hints
  - `090591bfeb0` fix(coding-agent): kept same-named modules from colliding in binary chunks
  - `333aeeb14fd` fix(catalog): dropped stepfun dr-search-api and moved ai& to kimi-k3
  - `5c0f9db2e3e` chore(bazel): refreshed MODULE.bazel.lock for the current Cargo.lock
  - `74b9bf8019d` style(rust): applied rustfmt and split a long clippy doc paragraph
  - `080009b79ea` fix(shell): kept pi's detaching nohup for background jobs
  - `5af3f53b73a` Revert "Merge PR #20282: perf(coding-agent): load @babel/parser through the shared lazy loader in legacy Pi rewrites (@iliaal)"
  - `20287e5e30f` fix(coding-agent): stop --no-extensions from importing ambient custom tool modules
  - `f6dbbb9b612` fix(coding-agent): keep reading project installs written under a relocated PI_CONFIG_DIR

### pocket-tts.cpp-git (`VolgaGerm/PocketTTS.cpp`)
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **0 commits since installed 0.1.0.r18.ge801e7d-1 (ref `e801e7d`).**
* **Recent Focus**:
  - Up to date with installed package (0 new commits).

### python-bitsandbytes-rocm-git (`bitsandbytes-foundation/bitsandbytes`)
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **1 commits since installed 0.50.2.r2.g83364904-1 (ref `83364904`).**
* **Recent Focus**:
  - `a616886` Cache the hipBLASLt int8 matmul algo per problem on ROCm (#2100)

### python-gptqmodel-rocm-git (`ModelCloud/GPTQModel`)
* **Status**: Highly Active (665 commits, 5 tags/releases in the last week). **1990 commits since installed 7.3.2.r31.g7df3d1e83-1 (ref `7df3d1e83`).**
* **Recent Focus**:
  - `376196a5` tests: finish the test-double and hook updates from #6041 (#6043)
  - `79f1349a` fix(torch): decode a wide activation in its own dtype (#6042)
  - `fcccca65` tests: make host and CPU assumptions explicit in fixture oracles (#6040)
  - `ad5790f5` fix(deps): raise the gguf and sentencepiece floors to the supported releases (#6038)
  - `60ff2a79` tests: pin eager Torch SSM/DeltaNet kernels for CPU forwards (#6039)
  - `c3512d10` fix(rocm): shim __expf and audit HIP-native intrinsics (#6037)
  - `5e7d8675` fix(loader): fall back to the selected checkpoint path and normalize the quant method (#6036)
  - `05c2045e` fix(compile): declare eager-only Humming kernels and avoid fullgraph graph breaks (#6032)
  - `c4b3e046` fix(triton): build nvfp4 and TT block-float kernels through the shared JIT wrapper (#6033)
  - `2a2066f9` fix(ports): leave quantized projections in eval and make the KDA gate length-invariant (#6035)
  - `6f9684df` tests: keep test doubles out of kernel selection and refresh stale expectations (#6041)
  - `9286dd22` fix(inkling2_loop): route calibration through the shared VLM dataset contract (#6034)
  - `ab915dc2` fix(avx512): correct the AWQ int4 GEMM fake-tensor width (#6031)
  - `36aa55b2` fix(ldexp): launch on the operand device, not the current one (#6030)
  - `be48f4cc` fix(kernels): keep derived caches out of model state and enforce the dtype lock (#6029)

### signal-cli-rest-api-git (`bbernhard/signal-cli-rest-api`)
* **Status**: Active (3 commits, 2 tags/releases in the last week). **26 commits since installed 0.101.pre.r1.gebb7c1d-1 (ref `ebb7c1d`).**
* **Recent Focus**:
  - `7d6f745` Parse attachment data URI parameters as MIME parameters
  - `893be5e` Keep attachment files in their temporary directory
  - `0442827` updated swagger documentation
  - `7635897` updated signal-cli to v0.14.10
  - `39319d2` Terminate group docs: drop the groups v2 detail
  - `605bada` Add endpoint to terminate (end) a group for everyone
  - `d6e1ff2` Exit if JSON_RCP_RECEIVE_MODE is set in non-JSON-RPC mode
  - `090d9b1` Shorten the critical section
  - `2cb7ad4` Reduce the level of unimportant logs
  - `801b015` Refactor JSON RPC receive mode into an enum
  - `53fa038` Minor style fixes
  - `955f78f` Parse the payload as manual only in manual mode
  - `68ca010` Fix double subscription in the on-start receive mode
  - `39489e3` updated signal-cli to v0.14.9
  - `8990c1f` write jsonrpc2.yml atomically

### vllm.cpp-git-hip (`mudler/vllm.cpp`)
* **Status**: Highly Active (93 commits, 0 tags/releases in the last week). **3121 commits since installed 0.0.2.r829.g7481a2e-1 (ref `7481a2e`).**
* **Recent Focus**:
  - `28007b445` fix(MODEL-TEXT-kolibri-1-1): cover the sparse refusal and correct layer count
  - `c5af7acbd` feat(MODEL-TEXT-kolibri-1-1): parse and place Kolibri-1.1 layer plumbing
  - `6b492258e` docs(MODEL-TEXT-kolibri-1-1): specify U2 dense prefix and shared KV
  - `885498ad4` records(CI-FLAKINESS-AND-LINK-FIXES): correct the DeviceAvailable guard evidence
  - `d4ed89841` fix(CI-FLAKINESS-AND-LINK-FIXES): shard the thread lane and retry only runner deaths
  - `ed7ce3069` docs(CI-FLAKINESS-AND-LINK-FIXES): specify the sanitize-cpu thread resilience fix
  - `9104388e0` records(NEW-CANDIDATE-PORTS): record the exact olala gate and Finding 3 disposition
  - `372e6ba09` fix(NEW-CANDIDATE-PORTS): make the masked olala porting fixes unit-detectable
  - `92ea7d3a8` docs(MODEL-TEXT-kolibri-1-1): record U1 outcome and complete marker list
  - `f3cd90f8e` fix(MODEL-TEXT-kolibri-1-1): refuse 1.1 GGUFs in the kolibri1 arm
  - `73332eeec` docs(MODEL-TEXT-kolibri-1-1): specify U1 walk and arch-collision guard
  - `0f73f3434` Kolibri-1.1 assessment: enumeration, delta, oracle landscape, refusal audit
  - `9f35b3245` feat(NEW-CANDIDATE-PORTS): olala W2e — keep-quant decode for the q6_k, q5_k_m and q8_0-safe2 arms
  - `66a241902` spec(NEW-CANDIDATE-PORTS): W2e plan — olala keep-quant decode for the three quantized arms
  - `00a796cb7` test(NEW-CANDIDATE-PORTS): prove the W2d-2 cache write and record the exact token gate

### python-optimum-amd (`huggingface/optimum-amd`)
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **4 commits since installed 0.1.0.r63.gf36a96b-1 (ref `f36a96b`).**
* **Recent Focus**:
  - `f38230d` 🔒 Pin GitHub Actions to commit SHAs (#189)
  - `3020ff1` Bump doc-builder workflow pin (#186)
  - `00cb2b2` Pin GitHub Actions to commit SHAs (#183)
  - `bdd598a` chore: enable Dependabot weekly GitHub Actions bumps (#179)

### smg (`lightseekorg/smg`)
* **Status**: Highly Active (1408 commits, 0 tags/releases in the last week).
* **Recent Focus**:
  - `bf42a13df` feat(gateway): state an encode-mode retry's output limit on gRPC (#8286)
  - `9e9e9b66b` perf(policy): read the spec in force through a thread's own reference (#8348)
  - `bd8cc79e8` feat(policy): hold a pair to the worker its request names (#8377)
  - `5002880f2` feat(policy)!: place an encode item on the ring its caller lends (#8362)
  - `371babcdd` feat(policy): run a capped sessions rule on a pair's two sides (#8332)
  - `29b376613` fix(policy): hold a request to its rule's workers past unready picks (#8376)
  - `ecb099bb0` fix(policy)!: read a JSON policy spec one way in every build (#8365)
  - `ef0b6ae4e` docs(policy): record the kept load report in the design's decision 12 (#8384)
  - `4dfdb9b2d` refactor(policy): remove the store's derivation of encode classes (#8373)
  - `8e9c43fae` refactor(policy)!: mark the types no caller builds non-exhaustive (#8287)
  - `286457bae` feat(policy): open a load stream to a gRPC worker with no event stream (#8356)
  - `c5533712f` fix(policy): sum a worker's resident tokens without a wrap (#8354)
  - `4636b3049` refactor(policy): derive no pair over one side and check by_place (#8374)
  - `ca296e38e` feat(policy)!: state a controller's two overload defaults at its start (#8322)
  - `a06805492` fix(worker): keep an engine without rank loads one plain worker (#8164)

### tei-rocm (`huggingface/text-embeddings-inference`)
* **Status**: Active (5 commits, 0 tags/releases in the last week). **66 commits since installed 1.9.3-6 (ref `v1.9.3`).**
* **Recent Focus**:
  - `71acf3f` Preserve the character budget for uneven input pairs
  - `d6bf408` Apply FlashBert dtype checks on the IPEX path
  - `8ccc6ae` Fix ONNX past_key_values head size for GQA models
  - `e233957` Define ROCM_HAS_FA_VARLEN on non-ROCm backends
  - `077f24e` Fix loading GTE models with native Transformers configs
  - `ea547d3` Document Prometheus metrics and scraping (#968)
  - `6d15a36` Apply sigmoid to multi-label classifier scores (#983)
  - `0afbf3f` Document the real default of truncate in the OpenAPI schema (#967)
  - `4b8b7b7` Mask padding in SPLADE pooling of padded BERT and DistilBERT batches (#981)
  - `73f017b` Fix left padding in Qwen3 raw token embeddings (#975)
  - `fa58ad5` Fix padding in raw Candle token embeddings (#973)
  - `184878d` Fix token embeddings for ONNX exports with sentence output (#977)
  - `ef0203a` Fix gRPC RerankStream never returning a response (#980)
  - `56b0f1c` Redact --api-key in the startup log (#966)
  - `da9a9ce` Support a separate HTTP metrics port (#678)

### python-optimum-rocm (`huggingface/optimum`)
* **Status**: Stale (0 commits, 0 tags/releases in the last week).
* **Release Status**:
  - ✅ Up to date
  - Upstream Latest: `2.3.0` | PKGBUILD: `2.3.0` | Installed: `2.3.0-2`

### python-peft (`huggingface/peft`)
* **Status**: Active (17 commits, 1 tag/release in the last week).
* **Release Status**:
  - ✅ Up to date
  - Upstream Latest: `0.22.0` | PKGBUILD: `` | Installed: `0.22.0-1`

### python-pocket-tts (`kyutai-labs/pocket-tts`)
* **Status**: Active (3 commits, 0 tags/releases in the last week).
* **Release Status**:
  - ⚠️ **Newer release available: `4.0.1`**
  - Upstream Latest: `4.0.1` | PKGBUILD: `2.1.0` | Installed: `2.1.0-1`

### python-infinity-emb (`michaelfeil/infinity`)
* **Status**: Stale (0 commits, 0 tags/releases in the last week).
* **Release Status**:
  - ⚠️ **Newer release available: `0.0.80`**
  - Upstream Latest: `0.0.80` | PKGBUILD: `0.0.75` | Installed: `0.0.75-3`
<!-- END_DETAILS -->

