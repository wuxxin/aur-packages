# Full change listings per git source

Complete, unfiltered commit lists for each update window (the curated digest lives in [curated-changes.md](curated-changes.md)). Append a new section per window; never rewrite older ones. Baselines: exact pins where the installed build encodes them (llama.cpp pkgver, Strata tags); otherwise the mirror tip immediately before the window start date.

## Window: 2026-11-14 → 2026-11-18 (`12383.r1.g3549c27` → `12522.r0.g2cbfc3c`)

### llama.cpp — 138 commits

```
2cbfc3cf34 2026-11-18 mmalpe-nv: [CUDA] : Add SKU-aware FP16/BF16 accumulation precision gating for NVIDIA GPUs (#30672)
6f311d7ad6 2026-11-19 Masashi Yoshimura: webgpu: (fix CI) allow the FA mask to be broadcast over the Q batch (#32535)
ff6b8d1761 2026-11-18 Aman Gupta: ggml-cpu : use all threads for large GET_ROWS (#32514)
98d67c8d53 2026-11-18 varun: model:add Zaya1 8B (Zyphra) (#32071)
387395aa8d 2026-11-18 Aleksander Grygier: ui: install @ggml-org/llama-brand from npm (#32544)
a693a5f66f 2026-11-18 Aleksander Grygier: ui: llama-chat publish drops the registry check, bin paths without ./ (#32543)
b069e526de 2026-11-18 Jai Patel: gguf-py : fix tensor offset overflow in GGUFReader (#32495)
ffc87c3a79 2026-11-18 Aleksander Grygier: ui: soften the action card border and show the split-button divider in dark mode (#32538)
10f173b253 2026-11-18 Emanuil Rusev: ui: hide Models and MCP behind settings, off by default (#32527)
97069ff6c4 2026-11-18 Aleksander Grygier: ui: run Llama Chat with npx @ggml-org/llama-chat (#32524)
bba8408821 2026-11-18 Gaurav Garg: Add LLAMA_MOE_RANDOM_ROUTING=1 for benchmark-only random expert selection (#29539)
48a32194ee 2026-11-18 Xuan-Son Nguyen: server: fix transcription prompt for v1/realtime (#32507)
6da36139e8 2026-11-18 Aleksander Grygier: ui: run the Storybook deploy on HF Jobs, with a token that can write the Space (#32525)
61f182fcde 2026-11-18 Daniel Bevenius: unicode : add continuation check lambda (#31070)
03ec5b4326 2026-11-18 losewayy: cuda : fuse NORM + MUL (+ ADD) (#32454)
7144124a5b 2026-11-18 Daniel Bevenius: vocab : extract bpe_rank loading into function (#30962)
43bd7a2a42 2026-11-18 Ruben Ortlam: vulkan: add bfloat16 support to various ops (#32202)
65758d01f5 2026-11-18 Aleksander Grygier: ui: Storybook follow-ups: generated DESIGN.md tokens, shared helpers and one Llama Mono (#32523)
a300a9c334 2026-11-18 Ryn Wang: cuda : increase Pascal DP4A MMQ I tile for J=64 (#31352)
4577932fab 2026-11-17 Ravi Panchumarthy: ggml-openvino: expand model support, optimize NPU,GPU and memory usage (#32172)
398f00d657 2026-11-18 Johannes Gäßler: CUDA: use MMQ for MoE on V100 (#32504)
9e93cd8001 2026-11-18 Aleksander Grygier: ui: a Storybook for Llama UI and Llama Chat (#32485)
aaa807c568 2026-11-18 Pascal: cuda: decode the conv2d patch indices with fastdiv (#32492)
401563f10e 2026-11-17 Hongqiang Wang: vulkan: run rms_norm with a runtime loop count on Qualcomm (#30824)
52975342ff 2026-11-18 Xuan-Son Nguyen: server: slot_sched: fix lora and recurrent (#32434)
3574df84b7 2026-11-18 Xuan-Son Nguyen: mtmd: support tiny-voca (#32427)
2e53a0bab7 2026-11-17 thelittlefireman: ggml-cuda: hip: Tune stream_k algo and mmq configs to use stream_k on AMD GCN (#30022)
744c68cd14 2026-11-17 Aleksander Grygier: ui: publish @ggml-org/llama-ui from CI, and release 0.4.0 (#32480)
307e3f1551 2026-11-17 Xuan-Son Nguyen: mtmd: add kokoro tts support (#32413)
9048bad8d6 2026-11-17 Pascal: cuda: use the implicit GEMM conv2d path for F32 kernels (#32482)
a9d43ecc30 2026-11-17 shaofeiqi: opencl: add A7 Q5_K non-MoE binary kernel (#31002)
8c16babba5 2026-11-17 James Prevett: mtmd: Add support for Qwen3-TTS' ICL/reference mode (#32438)
ad9d9e8f50 2026-11-18 Aman Gupta: qwen4exp : fix graph reallocation from the n-gram table scale (#32483)
955c4e8ee5 2026-11-17 eddiechen: server : return 400 when grammar and ignore_eos are on (#32377)
10152bc4a0 2026-11-17 karan: ggml-cuda: disable quantized matvec fusion on all Pascal GPUs (#32239)
8777c0c833 2026-11-17 anujj: Title: CUDA: few-row MMQ for MUL_MAT_ID (#32065)
918076a635 2026-11-17 Emanuil Rusev: ui: turn the live markdown preview off by default (#32469)
ebc9fb933e 2026-11-17 Giorgio Sarno: CUDA: use block reductions for whole-row pool_1d (#31855)
8b8ca4c98e 2026-11-17 Aman Gupta: ggml : decode F8_E4M3 to fp32 without ldexpf (#32477)
08a9b35893 2026-11-17 Marcus Tillmanns: llama : keep the k-pool layout prefix on sequence edits (#32137)
acad5e405c 2026-11-17 Hiroyuki Ikegami: vocab : speed up PLaMo-2/3 tokenizer table build (#32249)
d3064fddce 2026-11-17 Aman Gupta: convert : fix FP8 qwen4exp checkpoints (n-gram table scale, block-scaled FP8) (#32476)
7f106b5459 2026-11-17 Aleksander Grygier: ui: Llama UI design system: tokens, surfaces and fonts (#32468)
d92ea9bb12 2026-11-17 Xuan-Son Nguyen: mtmd: support Minimax-Music3 (#32435)
8d1599fca1 2026-11-17 Xuan-Son Nguyen: chat: add tts_dict for kokoro G2P template (#32397)
054a1babf3 2026-11-17 Gaurav Garg: Rotate  K/V read order for better L2 cache hit rates (#32407)
513ad7ae07 2026-11-17 Emanuil Rusev: ui: turn conversation tabs off by default (#32402)
67cf8967eb 2026-11-17 Aleksander Grygier: ui: move Llama Chat to SvelteKit 3 and its built-in service worker (#32463)
4df3f2959c 2026-11-17 cherry77-cloud: qwen3next : apply output projection weight scale (#32393)
a49db739fb 2026-11-17 Daniel Bevenius: cuda : raise shared mem limit only for the launched kernel (#32392)
eada89c315 2026-11-17 Titaniumtown: nix: expose a SYCL package (#31066)
8f647f1fdb 2026-11-17 Ruben Ortlam: vulkan: disable flip Flash Attention shader on AMD Windows due to a driver bug (#32415)
dde9de82cb 2026-11-17 Neo Zhang: sycl : Fix FA mkl issue: a mask broadcast over heads or batches (#31536)
e0a9118fe9 2026-11-17 Souleyman: metal : add implicit GEMM kernel for CONV_2D (#28069)
140a279874 2026-11-17 Nikhil Jain: webgpu : Implement timestep embedding (#31695)
c145db2728 2026-11-17 Takamichi Ohara: webgpu : use f32 while dequantizing to avoid FTZ (#32140)
ede6106780 2026-11-17 lhez: opencl: support f16 and non-contig f32 silu (#32319)
9214bdb554 2026-11-17 zhaoyshine: sycl: use fast division in bin-bcast kernels (#32213)
d3c3e242c1 2026-11-16 shaofeiqi: opencl: add A7 Q8_0 non-MoE binary kernel (#31003)
9581154a22 2026-11-16 Sidhartha Reddy Potu: mtmd : fix Muse Glimmer vision embedding order (#32433)
1ef8c5d684 2026-11-16 Gabe Goodhart: convert : respect max_position_embeddings for granite hybrid (#32436)
e8fbcad855 2026-11-16 Pascal: tests: print the exception message in test-llama-context (#32428)
95e837aaf1 2026-11-16 Xuan-Son Nguyen: skills: explicitly specify paths to README-dev.md (#32431)
d998c676ff 2026-11-16 Bartowski: convert: Fix inkling 2 mmproj conversion (#32430)
92192d31e4 2026-11-16 Xuan-Son Nguyen: mtmd: support YuE2-3B (#32369)
ad5cbfa911 2026-11-16 shaofeiqi: opencl: add A7 Q4_K non-MoE binary kernel (#30948)
d261e49e7e 2026-11-16 Hongqiang Wang: opencl: fix three defects of the bin flash-attention prefill path (#32110)
4ddf2b9470 2026-11-16 Aldehir Rojas: chat : implement inkling parser (#32381)
4303cd94ae 2026-11-16 Xuan-Son Nguyen: contributing: mark agents.md and code-review as required (#32416)
c7518dbec5 2026-11-16 Beinsezii: MMVQ: Tune ne11 Gate for RDNA3_5 (#32308)
a68c6136bb 2026-11-16 Xuan-Son Nguyen: mtmd: support fish audio s2 (#32330)
3a7660371d 2026-11-16 Aleksander Grygier: ui: move the web UI to ui/apps/chat and call it Llama Chat (#32032)
e8698ac163 2026-11-16 Shubham Roy: fix:- Misc. bug: Settings/Tools is lying about tool picks inside a ch… (#32223)
7804be0634 2026-11-16 Rudransh Shekhar: arg : allow up to llama_max_devices() configs for --tensor-split and --fit-target (#13293) (#31435)
ef6bc6f367 2026-11-16 Xuan-Son Nguyen: jinja: impl scope-chain key lookup (#32396)
a06044b934 2026-11-16 Niklas Wenzel: llama : deprecate old batch API (#32306)
62a6d3a302 2026-11-16 Niklas Wenzel: llama : migrate to `llama_batch_ext` (#32356)
ef3848f9d7 2026-11-16 Jeff Bolz: vulkan: Support split_k for conv3d. (#29929)
47fe133318 2026-11-16 uvos: HIP/CUDA: enable GDN mma kernel on CDNA (#31327)
301db63370 2026-11-16 Ruben Ortlam: vulkan: fix Nvidia fp32 FA shmem overflow, disable shmem staging if it takes too much memory (#32244)
a001af915e 2026-11-16 BlivionIaG: hip: add gfx1013 to rdna1 (#32236)
164ab018f9 2026-11-16 Pascal: webgpu: support per-head flash attention masks (#32394)
5cb9516798 2026-11-16 Georgi Gerganov: readme : fix line endings
8bfd64b5ac 2026-11-16 Georgi Gerganov: readme : update (#32382)
e1925b3695 2026-11-16 Xuan-Son Nguyen: jinja: support json sort_keys=true (#32366)
95db855bce 2026-11-16 Georgi Gerganov: ci : use vX.Y.Z tags as docker tags (#32388)
1d2e880bad 2026-11-16 miyan: vulkan : fix 32-bit compilation (#32275)
adf554d239 2026-11-16 Pascal: vulkan: make the radix top-k tie selection deterministic (#31931)
6b01a4767f 2026-11-16 Ruixiang Wang: CI: trigger spec dec testing for relevant PRs (#32281)
f477c1b90a 2026-11-16 liminfei-amd: cuda : fix MUL_MAT_ID abort with odd src0 columns on AMD (#32385)
21fa9c043f 2026-11-16 Titaniumtown: kv-cells: avoid an O(n_cells) scan per sequence removal (#32380)
a946eb541a 2026-11-16 Pascal: server: answer reasoning_effort levels the template rejects with 400 (#32332)
05db09a4d3 2026-11-16 thelittlefireman: ggml-cuda: fix MoE regression on HIP with #29948 (#32344)
9fba51d2c9 2026-11-15 Beinsezii: convert: fix ripple dflash2 NoPE metadata (#32363)
b4c0e00a4f 2026-11-16 Xuan-Son Nguyen: jinja: add 4 missing features (#32352)
1719dbb0ee 2026-11-15 Evan Huus: server : skip MCP discovery for router children (#32359)
fc504f91d8 2026-11-15 Xuan-Son Nguyen: mtmd: support higgs v3 STT and vibevoice-ASR (#32329)
18b74fa41d 2026-11-16 Seungjun Bae: model : read qwen3vl output head size from the tensor (#32349)
7ae3c6b231 2026-11-15 Xuan-Son Nguyen: mtmd: add zonos3-mini TTS model (#32020)
f4d0673917 2026-11-15 Xuan Son Nguyen: Revert "jinja: add 4 missing features"
a681a53b60 2026-11-15 Xuan Son Nguyen: jinja: add 4 missing features
75fd7f9ec9 2026-11-15 Xuan-Son Nguyen: docs: move per-model TTS to /docs, refer it from other pages (#32304)
a68799c609 2026-11-15 Xuan-Son Nguyen: model: support MiniMax-M3.1 (#32301)
56fd8a375f 2026-11-15 Roshan Kumar: server : ignore empty stop strings (#32093)
b54752df40 2026-11-15 Saejin Kim-Heinert: ggml-cpu: add x86 VNNI Q2_0 dot product (#26348)
900f01ba09 2026-11-15 uvos: CI/HIP: update fattn symbol names in hip-quality-check (#32331)
de32b268c4 2026-11-15 Anton Sokolchenko: Support DFLASH2 for Recursive Ripple-65B-Preview (#31904)
4e5116f476 2026-11-15 eddiechen: server : fix output_config.effort being dropped in /v1/messages (#32321)
278a89cb78 2026-11-15 uvos: CUDA/HIP: Refactor the use of _sync warp primitives (#31617)
dd099a6bf3 2026-11-15 Xuan-Son Nguyen: chat: fix inkling 2 begin/end of image tokens placement (#32294)
73f53317eb 2026-11-15 Xuan-Son Nguyen: vendor: sync stb_image (#32305)
429460dc0e 2026-11-15 Xuan-Son Nguyen: server: refactor, add server_slot_sched, prompt running hash (#32154)
58a4a6b49c 2026-11-15 Aayan Karmali: server : clear slot cache when the global lora config changes (#30367)
5a4afd8077 2026-11-15 Ed Addario: tests: Fail `test-backend-ops` and exit with error status 1 when missing and/or unsupported types and/or unsupported backends are provided in the command line (#30279)
6d3568e31d 2026-11-14 shaofeiqi: opencl: add A7 Q6_K non-MoE binary kernel (#30949)
e574a17b06 2026-11-15 Tarek Dakhran: model : metal : workaround fusion for LFM3 (#32296)
5c008e0008 2026-11-15 Piotr Wilkin (ilintar): feat: add Inkling 2 support (text + vision) (#32217)
9f26fe11c7 2026-11-15 IsNot: common : reject out-of-range grammar_triggers type instead of aborting (#30835) (#31478)
cf9a9957da 2026-11-15 Srijan Keshri: server : Fix connection reuse after streamed responses (#30492)
dca216ad63 2026-11-14 Pranav Dhinakar: hexagon: add TIMESTEP_EMBEDDING HVX kernel (#32228)
f8cc5774e7 2026-11-14 Niklas Wenzel: memory : fix non-consecutive position warning for M-RoPE (#32287)
acf5d54562 2026-11-15 Aaron Teo: llamafile: introduce more Q0 quant support for s390x (#32203)
3e41ae69db 2026-11-14 Yuri Khrustalev: llama : allocate the tensor staging buffer from the CPU buffer type (#31438)
3bc612fe23 2026-11-14 Richard Palethorpe: vulkan: Explicitly include SPIRV-Headers (#31416)
d8f30a5b6d 2026-11-14 Ruben Ortlam: vulkan: optimize prompt processing Flash Attention for RDNA3 and RDNA4 (#31323)
e964175653 2026-11-15 Kartik Sirohi: cuda : keep columns in registers for cooperative softmax (#28982)
d20426bbbe 2026-11-14 Jeff Bolz: vulkan: optimize matrix multiplication for narrow N (#31990)
19f31e61b0 2026-11-14 Ruben Ortlam: vulkan: use GPU copies on UMA with uncached memory on Intel (#32024)
07037ba133 2026-11-14 Nicolas Mowen: sycl : optimize mtmd image processing (#32109)
0cc522e45d 2026-11-14 Tarek Dakhran: chat : allow undeclared tool calls in LFM2 tool-call grammar (#32164)
f08bca8a46 2026-11-15 Takamichi Ohara: docs : add OpenVINO backend to ops matrix (#32259)
3c311796f2 2026-11-14 Alen Požun: chat : allow tool calls inside reasoning blocks for Ministral-3 (#32271)
8b4ac2496c 2026-11-15 Alex: common : fix infinite recursion in debug build for peg parser dump (#32282)
1ae047c926 2026-11-14 lhez: opencl: fixes for q4_k mv oob access, f16 swiglu_oai, cpy with strided dst, batched group_norm and bf16 sigmoid (#32251)
1c2adc75f6 2026-11-14 Cristian Adam: chat : allow Gemma4 tool call during thought (#32232)
a956a852c9 2026-11-15 miyan: Fix ctz64 on 32bit (#32273)
c6c0ec6d5c 2026-11-15 Jhen-Jie Hong: hexagon: fix fa no-mask tail (#32243)
d0764c5ee2 2026-11-15 Aman Gupta: qwen2vl : apply FFN weight scales (#32241)
```

### Strata — 736 commits

```
c77572806 2026-11-16 Niko1221: Drafting Off in the app: a model saved with Off loads after a restart, and the Models screen shows the saved choice (0.2.15 release test)
15c14f6c4 2026-11-16 Niko1221: app Load: a Drafting choice made on the Models screen is kept for the next start (0.2.15 release test)
2a3e33b8e 2026-11-16 Niko1221: app install: with no engine on the PC yet, the engine comes before setup, so pictures stay on (0.2.15 release test)
e39a52e33 2026-11-16 Niko1221: Version 0.2.15 / Control 0.1.61: app and Terminal 0.2.15, Control 0.1.61; every engine package stays 0.1.60 (the v0.2.14 files, carried by absolute url)
1b4018870 2026-11-16 Niko1221: launch: a drafter the person chose stays chosen, the way Off does
4746b6846 2026-11-15 Niko1221: update: a test start that misses a system library names it and keeps the engine's output
fdfca1d9d 2026-11-15 Niko1221: update: --backend amd on a PC with an NVIDIA and an AMD card picks the AMD card's package
b2d08647c 2026-11-15 Niko1221: app: Drafting Off fetches no draft layer; the offline note only when no drafter runs
1637559fd 2026-11-15 Niko1221: drafting: the tuned-drafter lookup applies the update's accepted feed sequence
d8278a0c0 2026-11-15 Niko1221: launch: a restart with no Drafting word keeps a saved "auto"
1a5c6dd19 2026-11-15 Niko1221: packaging: bundle libatomic.so.1 in the Linux AMD packages; check imports against the base system
78eab90f9 2026-11-16 Niko1221: chat: an agent's question notifies like an approval does (#5617)
1aabfb1ce 2026-11-16 Niko1221: serve: a declared boolean tool argument written True / False is the boolean (#5979)
5ae85c5ff 2026-11-16 Niko1221: web page: the About card's "MTP drafts up to N tokens" only when the MTP drafts (#5080)
e72c1939a 2026-11-16 Niko1221: launch: a key that only the Access step's highlight made goes again on "This computer only" (#5812)
d4786f483 2026-11-16 Niko1221: runtime: a start waiting for its owner reads an empty state file as not there yet (#5601)
2d8a32dc6 2026-11-16 Niko1221: update: the test start resolves paths of a removed Control version first (#5681)
ece3cedc1 2026-11-16 Niko1221: chat: a parked message is sent only from the chat that is also the active one (#5806)
3cf22f5ef 2026-11-15 Niko1221: serve: a stop without --shutdown-timeout refuses new requests while the engine closes (#6055)
63cef0a78 2026-11-15 Niko1221: monitor: Energy since start counts the GPUs that report power (#6012)
b9b752d8e 2026-11-15 Niko1221: [GUI] the app never starts a llama.cpp llama-server
d748168dc 2026-11-15 Niko1221: tests: the wizard's status-line check follows guidedStatusText; the Stop test waits for the install loop (DL99)
f697ea50f 2026-11-15 Niko1221: install progress: steps 6 and 7 keep the parts but give no download figure (DL99)
ad13d5992 2026-11-15 Niko1221: setup wizard: say why it waits when the files are in but the engine isn't ready (DL99)
be73f45be 2026-11-15 Niko1221: snapshot workflow: the Windows runner gets twice tools/check's 900 s for the config snapshot
38ac68ad6 2026-11-15 Niko1221: install progress: 100% once every file is in, and the file check shows its own figure (DL99)
5bacf18e7 2026-11-15 Niko1221: install progress: the picture reader counts by its real figure, and the setup wizard says setup's own step (DL99)
4434fb5f6 2026-11-15 Niko1221: app first run: Qwen3.6 downloads before its engine is in, and a failed install no longer cancels the engine download (DL99)
ac153b0a2 2026-11-15 Niko1221: feed install gate: a Mac run config is checked for the Metal engine's in-place read, not --resident-budget-gib
6cc3adb9c 2026-11-15 Niko1221: setup on a Mac (app mode): a model whose list entry has no draft layer says so on a Mac that streams too
88d404026 2026-11-15 Niko1221: test_dit_rope: the recorded hashes are glibc's; every C library gets a float-by-float check
01a1edea4 2026-11-15 Niko1221: py-tools on a Windows checkout (CRLF): the image gate's data stays LF, two hash tests start from LF
fe7d852d8 2026-11-15 Niko1221: cmake-cpu on MSVC: three CPU tests that only built or ran on Linux and macOS
baf16363b 2026-11-15 Niko1221: release manifest: the Control 0.1.60.1 packages of the 0.2.14.1 update
3af562d54 2026-11-15 Niko1221: progress words: step 6 with nothing to prepare claims no preparation
d94ab5e27 2026-11-15 Niko1221: release manifest: the Control-only update (terminal_version 0.2.14.1, control_version 0.1.60.1, engines 0.1.60); UPDATES.md example lines follow
2ad883b61 2026-11-15 Niko1221: Control 0.1.60.1 / Terminal 0.2.14.1: version bump for the Control-only drafter fixes (app stays 0.2.14, engine packages stay 0.1.60)
51543fd4b 2026-11-15 Niko1221: progress words: "Preparing the draft layer" only when the draft-layer step runs
3dcdb99a7 2026-11-15 Niko1221: launch: say once when the draft layer cannot be downloaded offline
1821f298d 2026-11-15 Niko1221: launch: Drafting Off on a Mac fetches no draft layer
09b603886 2026-11-15 Niko1221: prefill fused experts: the down-rotation, FP16-down and P1A state per host thread
4d3e390b2 2026-11-15 Niko1221: launch: the start's safety net fetches the drafter it falls back to
4ba852d03 2026-11-15 Niko1221: tests: the 12 GB class without the MTP layer starts the DFlash2 drafter on disk
c426db8e8 2026-11-15 Niko1221: launch: the plan after a saved Off says Off
1f0ace2d1 2026-11-15 Niko1221: drafting: one drafter per install, never none unless Off was chosen
68a2916b7 2026-11-15 Niko1221: launch: Auto tells setup the drafter the start runs (12 GB card, IQ3_S)
9dcebebcd 2026-11-15 Niko1221: Settings register: STRATA_KFD_QUIET lists the unregistered arena for gfx1103 only
c1446aaa5 2026-11-15 Niko1221: Settings register: STRATA_KFD_QUIET_NOREG names the Radeon 780M class
5450e4344 2026-11-15 Niko1221: Integrated gfx11 under Linux: the unregistered expert arena only on the Radeon 780M class
40721b084 2026-11-15 Niko1221: Settings register: add the five gfx11 / gfx1151 switches the scan finds
76e4d7040 2026-11-15 Niko1221: test_uma_drop_guard: the GPU-shares line is looked for without its draft tag
05718a08f 2026-11-15 Niko1221: Integrated gfx11 under Linux: keep the arena's new rules inside the Linux HIP build
d7cc382ed 2026-11-15 Niko1221: launch TUI: the Drafting step shows Off when the draft layer is off
6069c9d0c 2026-11-15 Niko1221: Integrated gfx11 under Linux: two more first-request allocations made during the load
c3f6978b1 2026-11-15 Niko1221: Integrated gfx11 under Linux: the prompt path can keep its own buffers instead of lending cache slots (off by default)
8d1fadf92 2026-11-15 Niko1221: Integrated gfx11 under Linux: the expert arena is not registered with the driver by default
f420fc71c 2026-11-15 Niko1221: launch: Drafting Auto after Off starts with the drafter again
64e95049a 2026-11-15 Niko1221: prefill: the fused trellis prompt kernels are the default on Windows gfx1151
f5f28ae74 2026-11-15 Niko1221: kfd_quiet_test: build under -Wall -Wextra -Werror
f73fa7410 2026-11-15 Niko1221: Integrated gfx11 under Linux: pageable copies staged by the HIP runtime
59375eb06 2026-11-15 Niko1221: Integrated gfx11 under Linux: a stop by signal drains the GPU before the process ends
f9932c6ae 2026-11-15 Niko1221: Integrated gfx11 under Linux: no GPU work right after the big load allocations
477831fb6 2026-11-15 Niko1221: prefill: Windows gfx1151 with the fused trellis set: floor 64, --short-read keeps 64
6bb186c27 2026-11-15 Niko1221: prefill: gfx1151 can take the fused trellis prompt kernels (STRATA_PF_TQ_G1151=1, off by default)
745473a6a 2026-11-14 Niko1221: capability table: the version line names the packages carried over at an earlier version
3e401e97f 2026-11-14 Niko1221: serve: two more log lines lose their draft tag
49b61d0d4 2026-11-14 Niko1221: prefill: the two-chunk equal minimum is 5,400 tokens (a prompt of 10,800 tokens or more takes the equal cut)
fe8040c4d 2026-11-14 Niko1221: docs: the Strix Halo and AMD HIP performance pages say the engine is built without llama.cpp's MMQ kernels by default
d6fd26186 2026-11-14 Niko1221: Version 0.2.14 / engine 0.1.60: the v0.1.60 line in the setup.py version history; release.json names the carried 0.1.59 SYCL and linux-aarch64 packages
2514e0d16 2026-11-14 Niko1221: generate: the arm64 CPU expert kernels line loses its draft tag
bc4026239 2026-11-14 Niko1221: prefill: the two-chunk equal minimum is 5,500 tokens (segments of 11,000 tokens or more take the equal cut)
3cf99f840 2026-11-14 Niko1221: prefill: two equal chunks take the equal cut from 5,700 tokens each (three or more stay at 6,144)
81016158e 2026-11-14 Niko1221: test: the release manifest test holds for a release without a hotfix part (0.2.14) as well as with one (0.2.13.1)
38f63bc59 2026-11-14 Niko1221: Version 0.2.14 / engine 0.1.60: Terminal and app 0.2.14, Control and the engine packages 0.1.60
58aafad15 2026-11-14 Niko1221: metal: stub for kv_unstage_to_host so the Mac engine links again
f40f8caca 2026-11-14 Niko1221: Build the engine without llama.cpp's MMQ kernels by default
74e0ad55b 2026-11-14 Niko1221: prefill: keep today's cut when the equal chunk would be short (under 6,144 tokens at a chunk of 8,192 or more)
036da7383 2026-11-14 Niko1221: prefill: g_p1a_x16 defined and set in HIP builds only
fcf206cd3 2026-11-14 Niko1221: prefill: g_p1a_h_bytes defined and set in HIP builds only
eca58c648 2026-11-14 Niko1221: prefill: p1a_takes_pair returns false outside HIP builds
1ed9c5c38 2026-11-14 Niko1221: strata-q36: context fit check counts the staging pair in the build without MMQ
83cc5f35b 2026-11-14 Niko1221: prefill: P1A sizing order checked in debug builds; STRATA_PF_P1A_L2 read on HIP only
3d302a600 2026-11-14 Niko1221: prefill: P1A prompt experts on by default on Windows gfx1151
7aa7c8238 2026-11-14 Niko1221: prefill: gfx1151 prompt experts with F16 activations and F16 H behind STRATA_PF_P1A=1
13363bdb7 2026-11-14 Niko1221: prefill: --peer-device keeps the fused prompt kernels in a build without MMQ
2f01a4e37 2026-11-14 Niko1221: docs: settings page regenerated
8aec2625d 2026-11-14 Niko1221: tests: cast ignored CUDA / HIP return values to (void)
57488e20f 2026-11-14 Niko1221: register: regenerate on the batch 20 head (history field of the setting read in home_cpus.hpp)
7a9f8d2ad 2026-11-14 Niko1221: platform: correct the home CPU set comment
72e1970ef 2026-11-14 Niko1221: tests: fit_out_rule_test records the RAM copy's 96-slot ring on a 12 GB card
ad8d5250a 2026-11-14 Niko1221: register: regenerate on the batch 20 head (read lines of nv_defaults.cpp, prefill.cpp and generate.cpp moved by the start-up line change)
24501f817 2026-11-14 Niko1221: register: regenerate on the batch 20 head (the memory-node and equal-chunk merges: new reads in generate.cpp, STRATA_AUX_CPUS and STRATA_PREFILL_EQUAL read as strings, the NUMA switches also read in the GPU build)
d3b686a7e 2026-11-14 Niko1221: settings register: add STRATA_NUMA_CARD
ad37f204c 2026-11-14 Niko1221: docs: the elastic reader's VRAM ask at higher picture limits
62d2b4dc1 2026-11-14 Niko1221: STRATA_KV_HOST_DMA: register and docs say it is on by default on NVIDIA, off on AMD and Intel Arc
29173b3db 2026-11-14 Niko1221: engine: start-up lines of a build without MMQ no longer name MMQ kernels
c754158f9 2026-11-14 Niko1221: register: regenerate on the batch 20 head (STRATA_KV_HOST_DMA is now also read in the CUDA build; read lines of prefill.cpp moved)
643e681fe 2026-11-14 Niko1221: register: regenerate on the batch 20 head (read lines of generate.cpp moved by the expert cache shrink fix)
465c729a2 2026-11-14 Niko1221: register: regenerate on the batch 20 head (read lines of prefill.cpp and generate.cpp moved by the small-card walk change)
9e4ff8aaa 2026-11-14 Niko1221: serve: the elastic reader's VRAM ask follows its image limit
b9c9484dd 2026-11-14 Niko1221: prefill: size the RAM copy's lend region for the tail-0 auto chunk
a17d2f910 2026-11-14 Niko1221: prefill: size the auto prompt chunk for tail-free layouts when the equal cut is on
a171bba3f 2026-11-14 Niko1221: cuda_spill_baseline: the NVFP4 instances on sm_75
29045f352 2026-11-14 Niko1221: vision: Pascal cards also take F16 inputs for the GPU tower's BF16 matrices
ed7c0e8a3 2026-11-14 Niko1221: register: regenerate on the batch 19 head (read lines of generate.cpp, expert_source.cpp, setup.py and split_engine.py moved by the container memory merge)
a05edc880 2026-11-14 Niko1221: register: regenerate on the batch 19 head (read lines of generate.cpp moved by the K/V grow fix)
271262826 2026-11-14 Niko1221: register: regenerate on the merged head (history fields of the Turing settings, read lines of moe_fused_iq.cu)
fb2cff5e9 2026-11-14 Niko1221: vision: turn the GPU tower's BF16 weights into F16 on the GPU
467dca493 2026-11-14 Niko1221: vision: the GPU tower holds BF16 matrices as F16 and writes their inputs as F16
63df8c897 2026-11-14 Niko1221: vision: no 16-bit input rounding in the CPU tower by default; the GPU gate reads against float32
29147556b 2026-11-14 Niko1221: engine: background copies honour the process's CPU set
716ebae14 2026-11-14 Niko1221: engine: run on the graphics card's NUMA node on two-node machines
51e5e7adc 2026-11-14 Niko1221: prefill: read long prompts in equal chunks on one GPU in a build without MMQ
9a779fb40 2026-11-14 Niko1221: setup: compare RAM and the expert arena in one unit for the low-RAM choice
bde58068a 2026-11-14 Niko1221: Revert "expert arena RAM check: optionally leave the engine's own mappings out"
388a1554f 2026-11-14 Niko1221: expert cache: evict the slots a part-way shrink lost
5e3bae3ab 2026-11-14 Niko1221: register: regenerate on the batch 19 head (read lines of prefill.cpp moved by the stream_all_min() guard)
7104c8b8e 2026-11-14 Niko1221: prefill: equal-chunk cut rule for long prompt segments, with its unit test
d301e6665 2026-11-14 Niko1221: prefill: a build with MMQ keeps the old text of stream_all_min()
dcc11fb74 2026-11-14 Niko1221: kv_grow_refused_test: a full card, when asked (--full-card)
652f5fbd3 2026-11-14 Niko1221: generate: the elastic K/V grows from new VRAM when the expert cache cannot give it slots
f0356cb25 2026-11-14 Niko1221: prefill: copy the prompt's new K/V cells to the host copy by DMA on CUDA
7078b829a 2026-11-14 Niko1221: register: regenerate on the batch 19 head (read lines of prefill.cpp moved; moe_fused_iq.cu reads STRATA_PREFILL_NVFP4 in the NVFP4 kernel choice)
6afa7d37b 2026-11-14 Niko1221: Terminal tools: read a container's memory limit as the RAM size
9800a9925 2026-11-14 Niko1221: settings register: add the two container memory switches
50460f3c8 2026-11-14 Niko1221: cmake: build the quant layer's own tests in the CPU check preset
667533760 2026-11-14 Niko1221: expert arena RAM check: optionally leave the engine's own mappings out
6b42777ff 2026-11-14 Niko1221: cmake: do not build prefill_decode_golden for an architecture list below sm_75
434663b1b 2026-11-14 Niko1221: expert arena RAM check: do not credit shmem or locked pages in a container
f36f8168f 2026-11-14 Niko1221: memory guard: do not credit the engine's own mapped file pages
e02647b74 2026-11-14 Niko1221: memory guard: credit active file cache under a container's limit
81ac7c8ef 2026-11-14 Niko1221: setup: read the container's memory limit as the RAM size on Linux
e2f9db84f 2026-11-14 Niko1221: tests: check the bench's blob layout table against strata::quant::type_info, not ggml
14a2349c9 2026-11-14 Niko1221: register: regenerate (STRATA_PF_FUSED_SM75_IQ, read lines of moe_fused_iq.cu moved)
bc10fc892 2026-11-14 Niko1221: tests: the expert paths bench never changes a scale byte when it makes each expert's blob
f1d2467b5 2026-11-14 Niko1221: prefill: size expert matrices from Strata's own type table
79ce2d388 2026-11-14 Niko1221: prefill: the "prompt pieces" start-up line names the floor in force
cb5f22414 2026-11-14 Niko1221: fused experts: Turing tile rule, 128 rows from above 56 rows an expert for the i-quant gate/up
45f4570f8 2026-11-14 Niko1221: packaging: a recipe for the Windows NVIDIA engine package
f415f67ab 2026-11-14 Niko1221: prefill: the prompt-kernels start-up line names the floor in force
60ad5a1d5 2026-11-14 Niko1221: packaging: build strata_kq only when the build tree has it
8044b9441 2026-11-13 Niko1221: prefill: the plain pack takes a floor of 1,536 tokens on a discrete CUDA card in a build without MMQ
4e4888ddc 2026-11-13 Niko1221: Small-card rule: tell a build without MMQ by a flag its start-up initialiser sets
453566100 2026-11-13 Niko1221: Layer-major prompt walk: take the fused kernels in a build without MMQ
e95ba413c 2026-11-13 Niko1221: The small-card prompt rule ignores a STRATA_PF_FUSED that a build without MMQ set itself
fb7dee4e5 2026-11-13 Niko1221: prefill: the CPU share's limit no longer raises the long-prompt floor on the plain pack in a build without MMQ
46dac4cef 2026-11-13 Niko1221: cuda_spill_baseline: the known violations on sm_75
b933674ed 2026-11-13 Niko1221: Start-up prompt-kernel line: count NVFP4 layers on the staged fused entry
29b7e480c 2026-11-13 Niko1221: fused experts: the other i-quant gate/up formats (IQ2_S, IQ3_XXS, IQ4_XS, IQ2_XXS, IQ2_XS) on Turing
8120f6801 2026-11-13 Niko1221: pf_wmma_parity: skip, with its reason, the formats whose tile needs more shared memory than the card allows
7fc188c0b 2026-11-13 Niko1221: fused experts: IQ3_S gate/up with IQ4_NL / Q2_0 down on Turing (sm_75)
5a6d637c6 2026-11-13 Niko1221: platform_memory_test: report "skipped" with the reason when the system refuses to lock the region
3f0f7deff 2026-11-13 Niko1221: check_cuda_spills: sm_89 baseline for the prefill, qwen35, mmq and pf_own libraries
82aeb32b2 2026-11-13 Niko1221: Prompt path: NVFP4 layers take the staged fused group entry below the stream floor
2f4e1dcae 2026-11-13 Niko1221: Expert paths bench: NVFP4 / NVFP4 row
cf9d86fba 2026-11-13 Niko1221: Fused prompt experts: NVFP4 gate/up and down on the int8 kernels
b90297368 2026-11-13 Niko1221: verify_batch_parity: take the toolkit arguments of the PLE rule from the engine's own call
0faeb9281 2026-11-13 Niko1221: prefill_fused_iq_test: --bits-staged, byte identity of staged and unstaged kernels
4fc954b0b 2026-11-13 Niko1221: register: regenerate on the batch 17 head (doc mention line numbers of docs/UNSLOTH_Q4.md moved)
567e75ad7 2026-11-13 Niko1221: docs: UNSLOTH_Q4 fidelity note, drop "with the BF16 read" from the AMD gap sentence
1d2d8ab1c 2026-11-13 Niko1221: register: regenerate after the f-i8-share and f-q2n-own merges (batch 17 candidate)
d0de6cb07 2026-11-13 Niko1221: docs: UNSLOTH_Q4 no longer says setup writes STRATA_HC_Q8
1d633aadf 2026-11-13 Niko1221: prefill: a build without MMQ reads chunks of 64 tokens or more on the fused kernels for a trellis pack on a CUDA card that runs them
90731f26f 2026-11-13 Niko1221: verify_batch_parity: skip the PLE post-ops step where the engine switches them off
11e0176bb 2026-11-13 Niko1221: check_cuda_spills: the sm_89 allowance of the kernels that keep a stack frame
36292e233 2026-11-13 Niko1221: register: notes for the 54 Intel-engine settings of f-sycl-prs, read from the code (separate branch off the batch 16 candidate)
9e52144fc 2026-11-13 Niko1221: CPU pool: read the tightest cgroup CPU quota up to the mount's root
86203d19a 2026-11-13 Niko1221: pool_cores_test, pool_tasks_test: do not assume one NUMA node
12cd82a53 2026-11-13 Niko1221: native_expert_parity: start ggml-cpu before comparing against its dots
f1d504478 2026-11-13 Niko1221: register: regenerate after the f-gyro-floor 970a92972 and f-bw-hcq8 607535270 merges (batch 16 candidate)
607535270 2026-11-13 Niko1221: docs: the Q8_0 hyper-connection read is the default on NVIDIA for UD files
866130069 2026-11-13 Niko1221: register: regenerate and give the 54 Intel-engine settings of f-sycl-prs a status, owner and note (batch 16 candidate merge fix)
0cb155066 2026-11-13 Niko1221: tests: cover the Q8_0 hyper-connection default and the file check behind it
970a92972 2026-11-13 Niko1221: prefill: the start-up line about prompt kernels drops its [DRAFT] tag
2c388837f 2026-11-13 Niko1221: generate: no Hadamard-fold warning on gfx1201
fc66df986 2026-11-13 Niko1221: spec: the table the learning stretch writes is used by the next start at once
23c02a7f7 2026-11-13 Niko1221: spec: the learning stretch of STRATA_DRAFT_COSTS_LEARN=1 starts a new busy run at every request
f4accc5f4 2026-11-13 Niko1221: drafting plan: say what parallel slots draft, as the server does
43ccf6b66 2026-11-13 Niko1221: Qwen3.6 fused expert kernels: gfx12 parity test for the UD-Q4_K_XL pairs
e17d7a828 2026-11-13 Niko1221: server: say what parallel slots draft
5410b3bc0 2026-11-13 Niko1221: Qwen3.6 engine: fused prompt experts on gfx12 (HIP), default in a build without MMQ
493b1f1c8 2026-11-13 Niko1221: tests: prefill_fused_iq_test pair statistics printf had a real line break in its format string
dd81e9b84 2026-11-13 Niko1221: Fused HIP expert kernel: K-quant down rows walk their 256-value super-blocks
ced106040 2026-11-13 Niko1221: strata-q36: in a build without MMQ, set STRATA_PF_FUSED=1 unless the user set it
3204685e4 2026-11-13 Niko1221: tests: prefill_fused_iq_test no longer fails a layer on the worst row of fused against MMQ; pair statistics are printed instead
289dd66fc 2026-11-13 Niko1221: prefill: a build without MMQ runs the native Q2_0 pack's Q2_0 / Q2_0 layers on the fused kernel (CUDA sm_80 and newer)
12a7a9d34 2026-11-13 Niko1221: register: give STRATA_DRAFT_COSTS_LEARN and STRATA_WINDOW_WARM a status, owner and note (batch 15 merge fix)
1ade2c8bc 2026-11-13 Niko1221: Intel Arc engine: keep the prompt-layout interface in step with the shared header
9c4b7943a 2026-11-13 Niko1221: prefill: the start-up line counts a Hadamard-folded layer on the FP16 path below the floor
685186efc 2026-11-13 Niko1221: prefill: a build without MMQ reads chunks of 64 tokens or more on the fused kernels for a trellis pack on a gfx12 card
e41b329aa 2026-11-13 Niko1221: Start two requests at once with DFlash2 drafts on one large Blackwell card
e106b4c86 2026-11-13 Niko1221: SYCL fused_gr: the GrMulti layout assert states the merged size exactly
7385fea6b 2026-11-13 Niko1221: prefill: a build without MMQ reads chunks of 64 tokens or more on the fused kernels for a plain (non-native) expert pack
9b812ad02 2026-11-13 Niko1221: tests: share_own_rule_test includes <initializer_list>
4eff16309 2026-11-13 Niko1221: tests: native_i8_parity runs the int8 kernel on a layer with a carved-out CPU block
9d53a1a8d 2026-11-13 Niko1221: prefill: a layer the CPU share took experts of keeps the staged fused entry and the int8 kernels in a build without MMQ
d259bf553 2026-11-13 Niko1221: SYCL fused_gr: the layout assert of PR #3153 accepts the two bools the #4185 port added to GrMulti
1b11a76e8 2026-11-13 Niko1221: draft-cost table: on by default on Metal only; CUDA and HIP keep live costs
f71bd0394 2026-11-13 Niko1221: prefill: HIP build without MMQ also turns on the Q8_0, Q6_K and trellis fused kernels
b2114b4ec 2026-11-13 Niko1221: Qwen3.6 engine: prompt experts on our int8 kernels where MMQ is not available
f66a48b9d 2026-11-13 Niko1221: int8 expert kernels: Q5_K / Q6_K as down formats, Q8_0 as gate/up
f331970d9 2026-11-13 Niko1221: strata-q36: in a build without MMQ, set STRATA_PF_FUSED=1 unless the user set it
216af487d 2026-11-13 Niko1221: Turn the per-card prompt switch rule on by default for NVIDIA sm_86 cards
22246a338 2026-11-13 Niko1221: docs: regenerate SETTINGS.md after the merges (the way-back count is 68)
944850163 2026-11-13 Niko1221: spec: a real draft-cost price is the median of its 16 rounds, the monotone guard lowers an outlier; the window warm-up runs before READY
84e11a773 2026-11-13 Niko1221: spec: warm every verify window width once before the first request; log text of a taken-over table
70ef6d873 2026-11-13 Niko1221: prefill: a build without MMQ prints one statement about its prompt kernels
c55e0f829 2026-11-13 Niko1221: prefill: a build without MMQ no longer reserves full-size FP16 expert buffers in a fused layout
75d929ebf 2026-11-13 Niko1221: prefill: on a Tesla P100 a build without MMQ keeps the FP16 prompt path from the stream floor up
bb0476d0a 2026-11-13 Niko1221: Raise the default CPU-share limit on gfx12 cards with the fused kernels from 1,536 to 2,304 tokens
dd404b382 2026-11-13 Niko1221: Add a debug switch that reuses a lent loan by chunk alone
832d83c7a 2026-11-13 Niko1221: Correct two unit rows of the tail rules
71f3c6db6 2026-11-13 Niko1221: Size the lent prompt buffers' MMQ tail from the request's own last chunk
62b4a5e93 2026-11-13 Niko1221: Rules for sizing a lent fused layout's MMQ tail from the segment
4e818231a 2026-11-13 Niko1221: spec: log line of a size calibrated without a learned cost says "real", not "0.00 ->"
1e5d817a2 2026-11-13 Niko1221: prefill: a build without MMQ no longer prints the staged-entry line in MMQ's words
8b225dcb2 2026-11-13 Niko1221: spec: a machine with no draft-cost table builds one from its normal requests, no learning stretch
302f7d039 2026-11-13 Niko1221: prefill: correct the floors quoted in the share ratio note
995fde04e 2026-11-13 Niko1221: prefill: note the measured share ratios on the switch-point rule
ce414cb9e 2026-11-13 Niko1221: prefill: a build without llama.cpp's MMQ takes the staged fused entry for short chunks on every card class; the start-up line says what runs
b32583330 2026-11-13 Niko1221: serve: a held draft-cost table leaves the CPU prompt share and the PCIe share live too
5f68ad342 2026-11-13 Niko1221: spec test: a size keeps collecting real rounds after the held table is used
379e966a5 2026-11-13 Niko1221: Serve: refill the park pools between requests, not during one
60d2a301a 2026-11-13 Niko1221: Park pools: upkeep only while the engine is idle (rule and tests)
669b34a32 2026-11-13 Niko1221: spec: a held table is used after 100 requests even when a size is never reached
5938e506d 2026-11-13 Niko1221: spec: a table that is not fully calibrated yet is held back, live costs decide meanwhile
1886f8e21 2026-11-13 Niko1221: kernels: declare i8_expert_takes before the rule that uses it; the rule test includes initializer_list
f70653363 2026-11-13 Niko1221: kernels: chunks under the long-prompt floor can take the int8 expert kernels when the card's layout is the fused one
7f8c92f07 2026-11-13 Niko1221: kernels: a build without llama.cpp's MMQ takes the int8 expert kernels by default on every card
cca88a011 2026-11-13 Niko1221: native_dense_price_test: write the hyper-connection rows of the fixture pack as real BF16 rows
79606603f 2026-11-13 Niko1221: kernels: the 8-entry slices of the int8 expert kernel are on for tile 2; the few-rows limits move to the crossings with them
d71da59b2 2026-11-13 Niko1221: spec: sizes not yet calibrated follow the sizes that are
c3a861156 2026-11-13 Niko1221: spec: a fixed draft-cost table is calibrated against real rounds, size by size
83b893a54 2026-11-13 Niko1221: kernels: the int8 expert kernel covers gate/up Q4_K, Q5_K and Q6_K and down Q5_1
a8d49b421 2026-11-13 Niko1221: tests: native_i8_parity runs every tile-2..4 case a second time with 8-entry slices and requires the same bits
ab7da2784 2026-11-13 Niko1221: kernels: the tile-2..4 int8 expert kernel can run 8-entry slices with two weight rows per thread (STRATA_I8_N8=1)
5d26d6f4b 2026-11-13 Niko1221: spec: a learning stretch can time a lookup-type window in a round that has no proposal
ffbdccc83 2026-11-13 Niko1221: prefill: layers with few rows per expert take the grouped kernels in the int8 prompt path
65035696a 2026-11-13 Niko1221: kernels: the rule of the few-rows route for the int8 prompt path
f3ebb1368 2026-11-13 Niko1221: spec: restore the CLI loop's observe_probs line
bcbaf72dd 2026-11-13 Niko1221: spec: a learning stretch times window sizes in the rounds where they count, on every round
d877f150a 2026-11-13 Niko1221: prefill: scale the research switch-point rule per card
e84392acc 2026-11-12 Niko1221: prefill: research switch STRATA_SWITCH_POINT, the walk of a chunk by estimated cost
c43347d09 2026-11-13 Niko1221: spec: a learning stretch times window sizes past its proposals with filler rows
71fbb6067 2026-11-13 Niko1221: Regenerate the settings register after the pipelined-split pricing revert
e474c27bf 2026-11-13 Niko1221: Layer split: price a pipelined two-stage split as the sum of the stages again
1e50a146e 2026-11-13 Niko1221: spec: a learning stretch measures the window sizes it can pick
0ce77eaf8 2026-11-13 Niko1221: tests: the K-quant line test no longer reads STRATA_DEFAULTS before the one-argument check
15a4be9c7 2026-11-13 Niko1221: spec: the draft-cost table learns from the first seconds of a busy run
5bc07c47a 2026-11-13 Niko1221: tests: include <initializer_list> in the loan rule test
925d6fb05 2026-11-13 Niko1221: snapshot: the config goldens carry the new draft-vocabulary line
b637627a3 2026-11-13 Niko1221: prefill: size the prompt loan from the walk a piece takes
d6a4e8448 2026-11-13 Niko1221: Regenerate the settings register and docs/SETTINGS.md
3e28250e8 2026-11-13 Niko1221: Docs: the dense-weight trim is the default with a layer split
4f84787d6 2026-11-13 Niko1221: nvidia: the start-up line about K-quant experts prints only when the loaded model has them
210bf9410 2026-11-13 Niko1221: Layer split: do not warn about under-pricing of a few MiB
706df9b50 2026-11-13 Niko1221: kernels: keep the int8 kernel's aligned typedef out of the MSVC host pass
fba925b67 2026-11-13 Niko1221: drafting: read the operating system's name through sysinfo, not the platform module
c5e4e5109 2026-11-13 Niko1221: docs: settings page regenerated from the register
7d7590f40 2026-11-13 Niko1221: docs: settings page regenerated from the register
336b8089f 2026-11-13 Niko1221: docs: the DGX Spark's table sets six speed defaults, with the K-quant fused kernels; the QUANTS.md row and the register note name the Spark
12839812c 2026-11-12 Niko1221: kernels: keep the int8 kernel's aligned typedef out of the MSVC host pass
0b3364d41 2026-11-12 Niko1221: Layer split: price a later stage's Q8_0 hyper-connection rows and the PLE key
a30269021 2026-11-12 Niko1221: kernels: the int8 expert kernel takes Q2_0 as gate/up too (the Q2_0 pack)
e447c5a6e 2026-11-12 Niko1221: kernels: the int8 expert kernel covers gate/up IQ4_XS and IQ1_M and down Q5_0 and Q8_0
787cac036 2026-11-12 Niko1221: kernels: the int8 expert kernel's smallest tile fits 48 KB of shared memory for every covered format
191202132 2026-11-12 Niko1221: Layer split auto: credit the trim's freed VRAM to CUDA0 only, not to the later stages
b069d1f99 2026-11-12 Niko1221: prefill: the int8 expert groups are collected by a header of their own, not by MMQ's gather
10e3399f0 2026-11-12 Niko1221: prefill: STRATA_DUMP_MOE_LAYER=all writes the MoE input of every layer of the first chunk
c326eede6 2026-11-12 Niko1221: tests: the expert paths bench runs real rows and shows how the difference to MMQ spreads
374098cb6 2026-11-12 Niko1221: kernels: the int8 expert kernels keep their activation scales in FP32, as MMQ does
bde9faeb9 2026-11-12 Niko1221: prefill: put the int8 counter back where its variables are in scope
e521524f3 2026-11-12 Niko1221: docs: Strix Halo prompt-piece speedups of the staged entry and of the way back, from one build
74f14aed4 2026-11-12 Niko1221: prefill: put the int8 count block and the residual dump back where they belong
d7ae86fcf 2026-11-12 Niko1221: setup: --draft-vocab latin, and the help and docs say the file follows the computer's languages
a8db0bff3 2026-11-12 Niko1221: models: the known-set header match accepts the second shard of a split set
18fce038c 2026-11-12 Niko1221: drafting: a renamed copy of a known model set gets that set's drafter settings
d49d151b2 2026-11-12 Niko1221: drafting: pick the draft vocabulary by the computer's languages when none was chosen
82744a47a 2026-11-12 Niko1221: tests: the expert paths bench prints each path's difference to MMQ's output
ab35aff9b 2026-11-12 Niko1221: prefill: STRATA_I8_COUNT prints, per prompt chunk, which routed entries ran on the int8 kernels
116cdf2a3 2026-11-12 Niko1221: serve: --short-read defaults to 24 where the staged fused entry reads short pieces
75d91db5e 2026-11-12 Niko1221: prefill: the staged group entry for layers with no MMQ tile is the default on Windows gfx1151
2f1b77b26 2026-11-12 Niko1221: Layer split: do not count the PLE weights as freed by the trim
196ac8b01 2026-11-12 Niko1221: NativeDense::release(): take back the HC scratch pointers and the packed-Q8 keys, as the destructor does
7c76ce4f1 2026-11-12 Niko1221: One GPU: do not print the "--trim-stage-weights needs a layer split" line unless the flag was given
4c39e8624 2026-11-12 Niko1221: Layer split: STRATA_STAGE_TRIM=0 still turns the trim off, and the short-card spill walk keeps its rule
7e9bf8c8f 2026-11-12 Niko1221: PLE: use the model file's hash constants again, and keep the row-range check
c77b8ef08 2026-11-12 Niko1221: settings register: regenerated after the two K-quant merges
9783e09f9 2026-11-12 Niko1221: prefill: the RX 6000 series (gfx1030 / gfx1031 / gfx1032) reads its prompt experts on our own int8 kernels by default
c8461ce39 2026-11-12 Niko1221: kernels: the int8 expert parity test skips what a device does not cover; the call reports what it asked for
dcb9a1dd0 2026-11-12 Niko1221: docs: settings page regenerated from the register
8d7f997d4 2026-11-12 Niko1221: The Radeon 780M on Linux reads its 16-bit prompt GEMMs FP16 in and out by default
563e0fa03 2026-11-12 Niko1221: prefill: the hyper-connection up-mix runs on the FP16 matrix-core builtin when the prompt runs FP16 in and out
db1cf2dc6 2026-11-12 Niko1221: prefill: STRATA_PF_STAGED_FO=1 says once on stderr when a layer without an MMQ tile takes the staged group entry
37f0d8c68 2026-11-12 Niko1221: prefill: research switch STRATA_PF_STAGED_FO=1, the staged walk's group entry for layers with no MMQ tile
ba15b58bd 2026-11-12 Niko1221: prefill: the DGX Spark takes the fused prompt kernels for K-quant experts by default
dd015b8c3 2026-11-12 Niko1221: drafting: decide DFlash2 by what the model file is when its name is not one setup writes
3a4763217 2026-11-12 Niko1221: prefill: the int8 expert kernel joins the prompt path's expert groups behind its research switch
3c561bade 2026-11-12 Niko1221: settings register: git stamps of STRATA_UMA_PIN_CAP
d1ec6f039 2026-11-12 Niko1221: prefill: the staged 40-79 SM class takes Flash-Next's K-quant experts on the fused kernels by default again (STRATA_PF_FUSED_SM40=0 and STRATA_PF_FUSED_KQ=0 give MMQ back)
5d5498270 2026-11-12 Niko1221: docs: settings page regenerated from the register
00807c9b3 2026-11-12 Niko1221: [Engine] Strix Halo: the RAM cap with several requests at once has a way back and speaks only when it cuts
b5dfe5bea 2026-11-12 Niko1221: [Terminal] A start that stopped for lack of memory with several requests at once says what to lower
3a2558169 2026-11-12 Niko1221: [Engine] Strix Halo: cap the pinned RAM copy of experts when --batch slots pin their K/V
df723eb5a 2026-11-12 Niko1221: prefill: the K-quant default stays on the cards with 80 or more SMs; the 40-79 SM cards keep MMQ unless STRATA_PF_FUSED_KQ=1
4d958fbdb 2026-11-12 Niko1221: nv_defaults, docs: the start-up line about K-quant experts says what happens on the card; the QUANTS.md row names the fused kernels
f33e9fa7b 2026-11-12 Niko1221: prefill: wording of the fused-only floor line and of its Strix Halo settings row
9e3a36714 2026-11-12 Niko1221: prefill: Flash-Next's K-quant experts are read by the fused kernels by default on the NVIDIA cards the i-quant default takes (STRATA_PF_FUSED_KQ=0 turns it off)
d4b9aa91e 2026-11-12 Niko1221: prefill: the hyper-connection up-mix kernel is skipped when the prompt runs FP16 in and out
2248e6361 2026-11-12 Niko1221: prefill: Flash-Next's K-quant pairs take the 128-row tile on sm_86-class cards with 80 to 99 SMs, and the two Q8_0-down pairs on sm_120 cards with 100 to 149 SMs
6239e233a 2026-11-12 Niko1221: prefill: fused-only layer sets read chunks of 64 tokens or more on the streamed walk (Windows gfx1151)
ca38bf15d 2026-11-12 Niko1221: kernels: research int8 expert kernel gets a 128 x 128 tile variant and a shared-memory limit check
4e69597fc 2026-11-12 Niko1221: kernels: research int8 expert kernel gets a cheaper dot loop, a sign table and a branch-free activation stage
69394994a 2026-11-12 Niko1221: Integrated Radeon GPUs on Linux read long prompts on Strata's own int8 expert kernels by default
8ce488608 2026-11-12 Niko1221: Small-card prompt path: keep the switch helper out of the CUDA kernel headers
0d91daa8b 2026-11-12 Niko1221: kernels: research int8 expert kernel gets cheaper scale multiplies and a prefetch that overlaps the dot loop
9e491df8e 2026-11-12 Niko1221: prefill: the Qwen3.6 K-quant pairs take the 128-row tile from 112 rows an expert up on sm_86 cards with 80+ SMs
5d5122fd5 2026-11-12 Niko1221: kernels: research int8 expert kernel stops spilling registers (sub-block loop not unrolled); bench times each tile size
9187ef658 2026-11-12 Niko1221: WIP, not gated: integrated gfx11 on Linux takes the fused int8 prompt experts by default
f123a0d00 2026-11-12 Niko1221: kernels: native_i8_parity runs its memsets on the kernel's stream; bisect switch for the research kernel
fe67f7fbe 2026-11-12 Niko1221: kernels: unfinished research kernel native_expert_i8 (int8 dot-product tile kernels), behind a switch that is off
e1ae7d613 2026-11-12 Niko1221: tests: time one prompt layer of experts on every prompt path, and the dense prompt GEMMs with FP16 io off and on
6d7a183f0 2026-11-12 Niko1221: Small-card prompt path: the native fused expert kernels run by default (CUDA)
3860b43a4 2026-11-12 Niko1221: prefill: the Qwen3.6 engine takes the fused prompt kernels by default on the cards the Flash-Next default rule takes
b9bd40181 2026-11-12 Niko1221: tests: time one prompt layer of experts on every prompt path, and the dense prompt GEMMs with FP16 io off and on
b1db4ab8e 2026-11-12 Niko1221: metal: the Metal engine links again; two prompt-path entry points had no Metal stub
2fdee4aeb 2026-11-12 Niko1221: fused prompt kernels: the sm_86 rule class takes compute capability 8.0 and 8.9 as well
a269d4c82 2026-11-12 Niko1221: cuda_spill_baseline: one sm_86 entry moved with the K-quant staging commit (64 -> 72 bytes of stack)
6d8e42886 2026-11-12 Niko1221: integrated gfx11 on Linux: the owner's wording is final, the [DRAFT] marks come off the two log lines and the register note
0ee263992 2026-11-12 Niko1221: integrated gfx11 on Linux: the engine gives the model files' cached pages back while and after it reads the expert arena
8f6393a37 2026-11-11 Niko1221: integrated AMD GPU under Linux: wait until the kernel has stopped moving the registered arena before READY
0a17fb99e 2026-11-11 Niko1221: integrated gfx11 on Linux: the registered expert arena asks for no transparent huge pages
4e9dde87e 2026-11-12 Niko1221: gpu_pause_time: the comment above the between-requests line states its wording as approved
f55afa152 2026-11-12 Niko1221: serve: log a driver GPU pause that happens between requests (AMD on Linux)
6f1613cc1 2026-11-12 Niko1221: cuda_spill_guard: a per-architecture baseline of the known violations
02020478b 2026-11-12 Niko1221: server: drop the thinking-hold check on an engine's "multi" attribute
0d6308de6 2026-11-12 Niko1221: [Engine] Tesla P100: the FP16 prompt path with few-row experts is the default instead of MMQ
ef0fb17ab 2026-11-12 Niko1221: prefill: the staged fused path is the default on sm_86 / sm_120 cards with 40-79 SMs (STRATA_PF_FUSED_SM40=0 turns it off)
ab38d9298 2026-11-12 Niko1221: package_terminal: the import probe writes no bytecode into the bundle
46b3013f9 2026-11-12 Niko1221: Run the conversation cache and park pool tests in the CPU check build
56a659967 2026-11-11 Niko1221: [Engine] gp100_prompt_default_test: include <initializer_list>
62b6a47ea 2026-11-11 Niko1221: [Engine] Tesla P100: the rule for the FP16 prompt path with few-row experts as the default (not switched on yet)
af5803e4b 2026-11-11 Niko1221: [Engine] Prompt FP16 path: few-row experts on the quantized grouped kernels (research switch, off)
88a19ed64 2026-11-12 Niko1221: prefill: weight staging for the Q4_K and Q5_K gate/up kernels (the K-quant fused path stays opt-in; no default changes)
13eedf552 2026-11-11 Niko1221: serve: the #4677 stop bound on every backend, not only HIP
df485b41c 2026-11-12 Niko1221: prefill: the fused kernels are the default for IQ2_XXS / IQ2_XS gate/up on sm_86 / sm_120 cards with 80+ SMs
0471cc10b 2026-11-12 Niko1221: prefill staged walk: the batched group entry is the default on CUDA builds, opt-in on HIP builds
33648fef1 2026-11-12 Niko1221: serve: a decode window that finishes after the server's STOP is dropped whole
a96d13e1a 2026-11-12 Niko1221: prefill: the Q5_K and Q6_K down projections of the Qwen3.6 fused kernels join the weight-staging rings (K a multiple of 256: UD-Q4_K_XL's 41 layers)
98e21c171 2026-11-12 Niko1221: prefill: a failed weight-staging check takes the unstaged kernel for that launch instead of ending the process
77e1dd777 2026-11-12 Niko1221: tools: cuda_spill_guard lists the Qwen3.6 copy of the fused prompt kernels (fused_q36::native_kernel)
f68943534 2026-11-12 Niko1221: prefill: weight staging for the Q8_0 gate/up and down, the Q6_K gate/up and the Q5_0 down kernels, and the 128-row tile for the Q6_K / Q8_0 gate/up class on sm_86 with 40+ SMs
7bc09fadf 2026-11-12 Niko1221: prefill: Q5_K and Q6_K down projections on the fused kernels for Qwen3.6 (UD-Q4_K_XL's 41 layers), behind the same opt-in
ef371eba8 2026-11-12 Niko1221: park pools: the segment pool is min(2 GiB, a quarter of the cache) (measured: 55K-token park 283 ms with 1 GiB, 117 ms with 2 GiB)
01e21ef20 2026-11-11 Niko1221: engine: the park pools are on by default (a diagnostic switch turns each off), sized from the conversation cache
9f0056e41 2026-11-11 Niko1221: tests: give the MMQ tests' scatter-permutation and identity row-id tables the margin too
e4138c1c4 2026-11-11 Niko1221: tests: size MMQ row-id tables with the margin helper
697b6d67a 2026-11-11 Niko1221: prefill: size the DeepSeek MTP draft step's MMQ row-id table with the margin llama.cpp's kernels read past it
14dd746f6 2026-11-11 Niko1221: prefill: size the dense MMQ row-id table with the margin llama.cpp's kernels read past it (STRATA_DENSE_MMQ=1)
a041fd038 2026-11-11 Niko1221: qwen35: give MMQ's row-id table the margin llama.cpp's kernels read past its end
afaaa7737 2026-11-11 Niko1221: test: the Qwen3.6 one-layer test takes UD-Q4_K_XL's K-quant pairs (skipped until the build covers them) and sizes MMQ's row-id table with its margin
d7f7d9677 2026-11-11 Niko1221: qwen35: give MMQ's row-id table the margin llama.cpp's kernels read past its end
e0e2f4c07 2026-11-11 Niko1221: qwen35: the fused prompt kernels are opt-in for Qwen3.6 (STRATA_PF_FUSED=1), MMQ stays the default
5aa7f1d88 2026-11-11 Niko1221: serve: a pass without a hold gets the caller's own sampler object; the hold key is classified for the split engine
07cf3f4af 2026-11-11 Niko1221: segment pool test: workers, the filler and a shrinking thread at the same time
971bff01a 2026-11-11 Niko1221: strata-vision: `auto` picks Strata's own CPU picture reader on x86 CPUs without AVX2 too (no more exception for the scalar, SSE4.1 and AVX tiers)
5f0ae5b55 2026-11-11 Niko1221: tests: the retry tests' fake clock belongs to the test's own thread
018f0d659 2026-11-11 Niko1221: serve: the budget's passes hand the engine the caller's own sampler; the hold is classified for the split engine
9f15c32d7 2026-11-11 Niko1221: prefill: the 128-row tile on sm_86 cards with 40-79 SMs for the Q6_K / Q8_0 gate/up class above 112 rows an expert
3c5b55fd6 2026-11-11 Niko1221: packaging/build_hip_linux.sh: the BUILD.json no longer asks for the removed DSV41 setting
93834ddf8 2026-11-11 Niko1221: prefill: the fused Gyro-S trellis kernels are the default on compute capability 8.6 cards with 80+ SMs (HELD for the owner's word, not merged)
8f4a2e0af 2026-11-11 Niko1221: engine: STRATA_PARK_SEGPOOL_MIB, a research switch for the segment pool (off unless set)
ab3712569 2026-11-11 Niko1221: park trace: no AnonHugePages read (it walks the 47 GB expert mapping, ~0.5 s a read, inside the park's own times)
e00baa4ab 2026-11-11 Niko1221: cmake: the two new one-layer tests link the prompt-kernel library of the build, and the group test is an MMQ-build test
3a61182bb 2026-11-11 Niko1221: qwen35: prompt experts of Qwen3.6 on the fused int8 kernels where they cover a layer's formats, MMQ for the rest, the older grouped kernels as the fallback
bd5c4604f 2026-11-11 Niko1221: test: the fused prompt kernels at Qwen3.6's expert shape (2048 / 512), one layer against the reference, the int8 model and MMQ
0e159244d 2026-11-11 Niko1221: prefill: the fused prompt kernels again for Qwen3.6-35B-A3B's expert shape (n_embd 2048, n_ff 512), a second compile of moe_fused_iq.cu in its own namespace
6aba6d5fb 2026-11-11 Niko1221: conversation cache: the pool's idle bytes count against the budget and go back first
b0c818ad7 2026-11-11 Niko1221: conversation buffer: segments come from the segment pool when one is installed
e04c4c931 2026-11-11 Niko1221: conversation segment pool: an arena behind an OS interface, with a unit test (not used yet)
117473f64 2026-11-11 Niko1221: strata-vision own CPU tower: the SSE4.1 tier takes its exp from the C library (the scalar tier's), so its output equals the scalar tier's byte for byte
dc435d2dd 2026-11-11 Niko1221: park trace: page faults, huge-page bytes, vector addresses and K/V buffer sizes per park (STRATA_PARK_TRACE only)
b92075d92 2026-11-11 Niko1221: serve: the thinking budget's hold on --batch engines (BGEN slots)
f73297a96 2026-11-11 Niko1221: prefill: research switch STRATA_PF_FUSED_SM40=1 (off): sm_86 / sm_120 cards with 40-79 SMs take the fused kernels by default for the staged-gate pairs
3b3c41e40 2026-11-11 Niko1221: serve: the NVIDIA picture reader stays loaded by default on Linux on Arm (the DGX Spark class)
d622bbb42 2026-11-11 Niko1221: prefill: the 128-row tile rule takes a launch whose gate/up kernel is staged, whatever its down (IQ3_S / Q2_0 pair and its siblings)
14ef1be89 2026-11-11 Niko1221: prefill: weight staging for the IQ3_S pack's fused kernels (gate/up IQ3_XXS, IQ3_S, IQ4_XS; down IQ4_NL), and a 128-row tile rule for staged launches on sm_86 / sm_120 cards under 80 SMs
e14d4e370 2026-11-11 Niko1221: prefill: STRATA_PF_FUSED_Q6K=1 on gfx12 - Q6_K gate/up + Q8_0 down on the fused kernels (HIP, opt-in)
e93b90250 2026-11-11 Niko1221: image: gfx1200 / gfx1201 fast attention on by default in the image DiT code (STRATA_QI_GFX12_ATTN=0 turns it off)
e22f397d0 2026-11-11 Niko1221: test: the fused prompt test judges a build without MMQ against the int8-rounded model, with a ceiling per format class
f3608ce31 2026-11-11 Niko1221: prefill: STRATA_PF_FUSED_Q8GU=1 on gfx12 - Q8_0 gate/up + Q8_0 down on the fused kernels (HIP, opt-in)
ac0be5ee2 2026-11-11 Niko1221: prefill staged walk: the fused groups launch over larger batches of experts
a95046690 2026-11-11 Niko1221: serve: bound the GPU reader's context retries by time (18 s) as well as by count (12)
5a9d6f559 2026-11-11 Niko1221: [Engine] MTP drafter prompt pass: FP16 GEMMs by default instead of Q8_0 MMQ
4c8faae99 2026-11-11 Niko1221: engine: keep the picture reader's room in the reserve in the resident RAM mode
4efb5e8cb 2026-11-11 Niko1221: serve: the on-demand picture reader holds no room back before the first picture (NVIDIA)
f5d3b45c5 2026-11-11 Niko1221: tools/vision/own: the fused attention is the default on gfx1151 (STRATA_VIT_FA=0 turns it off)
6d65761c4 2026-11-11 Niko1221: picture reader: allow 12 retries of the GPU context start (was 8)
9a56a3625 2026-11-11 Niko1221: generate: name the CPU expert pool on arm64 in the start log line
ac306afb2 2026-11-11 Niko1221: DeepSeek out: the docs and READMEs (owner approved the drafts 11-11 16:00)
77c344bdd 2026-11-11 Niko1221: serve: the picture guard inside the replaced-reply rule; its log line marked [DRAFT]
041591f1d 2026-11-11 Niko1221: prefill: STRATA_PF_FUSED_TQ=1 on gfx12 - the Gyro trellis pairs on the fused kernels, Hadamard-folded layers included (HIP, opt-in)
be101072b 2026-11-11 Niko1221: serve: the thinking budget's hold (GEN hold=N:ID), so the wrap-up pass continues from the live session
b90d38aa8 2026-11-11 Niko1221: serve: start the GPU picture reader again after a CUDA context failure on a Linux Arm machine with shared memory
b673750df 2026-11-11 Niko1221: prefill: the prompt path of an engine built without MMQ (Strata's own kernels, else FP16)
e2bf2e451 2026-11-11 Niko1221: build: -DSTRATA_MMQ=OFF builds the engine without llama.cpp's MMQ prompt kernels
3feffd597 2026-11-11 Niko1221: prefill staged walk: a short chunk's groups on the fused kernels (the gathered-group entry)
24e9d3ba8 2026-11-11 Niko1221: picture reader: retry a failed GPU context start on a shared-memory GPU (Linux CUDA only)
af825339a 2026-11-11 Niko1221: tools/vision/own: the gfx11 fused attention, tuning round 1 (still off by default)
a5104df5b 2026-11-11 Niko1221: engine: the shared-memory page drop only in a Linux CUDA build, its line only when pages were given back
5e41f6984 2026-11-11 Niko1221: serve: no park of the reply a request replaces
7d4f78242 2026-11-11 Niko1221: serve: the #4677 stop bound on every backend, not only HIP
9ae901303 2026-11-11 Niko1221: prefill layer-major walk: a group's experts on the fused kernels where the card's rule takes them
66c2e81be 2026-11-11 Niko1221: prefill fused: one entry for the experts of one gathered group (group_bounds) + its parity test
c5c26171e 2026-11-11 Niko1221: prefill: STRATA_PF_FUSED_Q8D=1 on gfx12 - the Q8_0 down behind an i-quant gate/up on the fused kernels (HIP, opt-in)
d3d4d1612 2026-11-11 Niko1221: engine: the page-drop line is a [DRAFT] for the owner's wording; STRATA_UMA_DROP_PAGES in the settings register
317918f45 2026-11-11 Niko1221: DeepSeek out: test_launch_engine_first no longer depends on the box's graphics card
8bb2669c0 2026-11-11 Niko1221: STRATA_OWN_CPU_QUANT default ON on arm64
d3851f104 2026-11-11 Niko1221: CPU pool gate/up rows: load both dot results after the two calls, one at a time
81429a023 2026-11-11 Niko1221: tools/vision/own: a fused attention kernel for gfx11 (WMMA), behind STRATA_VIT_FA (off by default)
301f78b32 2026-11-11 Niko1221: DeepSeek out: three tests that still counted the DeepSeek pieces (final head run p1006-20261111-1211-e297)
454305361 2026-11-11 Niko1221: prefill: the fused prompt kernels are the default on compute capability 8.6 cards with 80+ SMs (IQ3_S pack formats)
6b32d91c5 2026-11-11 Niko1221: cmake: test targets prefill_decode_golden (CUDA) and hip_prefill_decode_golden (HIP)
57c90a686 2026-11-11 Niko1221: prefill: decode-digest test for the fused prompt kernels' weight decode (same file on CUDA and HIP)
0991006d2 2026-11-11 Niko1221: strata-vision own CPU tower: SSE4.1 and AVX kernel tiers for x86 CPUs without AVX2
3220dbc0e 2026-11-11 Niko1221: engine: a shared-memory GPU with every expert resident gives the model file's cached expert pages back
1ef77c47f 2026-11-11 Niko1221: DeepSeek out: fixes from the test run of the feed commit (p1004-20261111-1150-5a61)
6e4afbbc9 2026-11-11 Niko1221: serve: repeatable output also fixes the decode PCIe share: PcieAuto's settled value is stored with the draft cost table
b47591e74 2026-11-11 Niko1221: DeepSeek out (5b, app): a remembered DeepSeek model is skipped at the host's start, not cleared; nothing is written
0c83610e5 2026-11-11 Niko1221: strata-vision own tower: no AVX2 code outside the CPU-checked kernel tiers (a CPU without AVX2 could hit an illegal instruction)
f41c6330b 2026-11-11 Niko1221: DeepSeek out: fixes from the first full test run of commit 4
8fef680c0 2026-11-11 Niko1221: image: strata-image --plan / --te-mode, measurement switches for the memory rows of smaller cards (step 5)
888ded122 2026-11-11 Niko1221: tools/vision/own: on gfx1151, products with F16 results and float32 accumulation by default
4f66847b4 2026-11-11 Niko1221: DeepSeek out (7b, feed): build-feed carries the last feed's DeepSeek engine packages over, frozen (owner: "Keep frozen")
f1fce3286 2026-11-11 Niko1221: DeepSeek out (7/7): no DeepSeek engine is built, packaged, signed or put into a feed; the two DeepSeek docs pages say so
c6f84f281 2026-11-11 Niko1221: DeepSeek out (6b, Metal): the rest of the DeepSeek Mac code
e5806740a 2026-11-11 Niko1221: DeepSeek out (6/7): the DeepSeek engine's sources, tests, lab and CMake go
efa9d6dbe 2026-11-11 Niko1221: DeepSeek out (5/7): the desktop app without DeepSeek; a DeepSeek model in the list says where its files are and is not loaded
dd96b5318 2026-11-11 Niko1221: DeepSeek out (4/7): setup, `strata launch`, `strata update`, Settings > Engine and the model catalog without DeepSeek
4cd85d082 2026-11-11 Niko1221: prefill: the expert helpers that need no ggml-cuda move to moe_helpers.cu (strata_pf_own)
5bb8d1851 2026-11-11 Niko1221: prefill: Strata's own prompt kernels in a library of their own (strata_pf_own)
5369576ff 2026-11-11 Niko1221: DeepSeek out (3/7): the server no longer carries the DeepSeek code paths
865d3ed4d 2026-11-11 Niko1221: tools/vision: Pascal P100 (compute capability 6.0) takes our picture reader under auto, also with F16 reader files
ba11522ea 2026-11-11 Niko1221: tools/vision/own: on Pascal the larger attention score chunk (32M) for F16 reader files too
c76edff0a 2026-11-11 Niko1221: DeepSeek out (2b): the owner's approved words for D2-D6 (11-11), the [DRAFT] marks removed
12355203d 2026-11-11 Niko1221: DeepSeek out (2/7): every way a DeepSeek model can still come in is refused in plain words, and its config is never written
5d5029be4 2026-11-11 Niko1221: DeepSeek out (1/7): strata_control/retired.py, how a DeepSeek config, name, folder or file is recognised, and its words
8fdf701f8 2026-11-11 Niko1221: pool_rows_bench: the CPU pool's own row functions against ggml-cpu, no model
3f55acfa5 2026-11-11 Niko1221: settings register: STRATA_QI_GFX12_ATTN, the gfx12 attention test switch of the image DiT code
8499137ac 2026-11-11 Niko1221: tools/vision/own: HIP products with a 16-bit result and float32 accumulation, behind switches (off by default)
e85fd8795 2026-11-11 Niko1221: tools/vision: Strix Halo (gfx1151) takes our picture reader under auto, also on Windows
da5e33842 2026-11-11 Niko1221: CPU pool gate/up rows: read the gate dot's result before the up row's call
5fdb9aa4a 2026-11-11 Niko1221: netpolicy: a refused feed host is remembered for 6 hours by the launch's automatic check
6ccf276d2 2026-11-11 Niko1221: [DRAFT] locales: the French picture reader strings keep the French typography (a typographic apostrophe, a no-break space before ;)
2b9df3fe7 2026-11-11 Niko1221: launch: a typed --gpu list means the same in every home; the help line says who picks Main
5abd50c1a 2026-11-11 Niko1221: tools/vision/own: hipBLASLt for the HIP tower's products, behind switches (off by default)
087454e9b 2026-11-11 Niko1221: apps/host tests: the host-level switch tests account for the picture reader row (the fixture's run configs read pictures), and one more host test: choosing llama.cpp's reader writes STRATA_VISION_TOWER=mtmd and Strata's own again gives back the same file
b94c2931f 2026-11-11 Niko1221: setup: the alternative picture-reader mark also keys on the file's change time
1fdb3b224 2026-11-11 Niko1221: [DRAFT] locales: the picture reader's label, options and help line in the app's other eight languages (zh, ja, de, es, ru, pt, ko, fr)
92a2d99c8 2026-11-11 Niko1221: settings: "Picture reader" in Expert settings (app: Native engine settings > Image reading; Terminal: the Advanced table): Strata's own (recommended) or llama.cpp's
4f61dae53 2026-11-11 Niko1221: serve: the picture reader's READY line names the reader; when Strata's reader did not start and llama.cpp's took its place, the server says so once
0771e3555 2026-11-11 Niko1221: Downloads: a plain sentence when the drive is full, over quota or read-only
03e687ace 2026-11-11 Niko1221: AMD Linux: show how long the driver paused the GPU (stall report and request line)
dffa10490 2026-11-11 Niko1221: Launch wizard: keep every Save choice on an 80x24 screen for any storage path
adfcf9028 2026-11-11 Niko1221: image gate tools: run_strata_image.py runs strata-image over the gate set like run_set.py runs sd-cli (step 5, piece 3)
3c2dc2f13 2026-11-11 Niko1221: image: strata-image, a test program that makes a picture with no stable-diffusion.cpp or ggml in the process (step 5, piece 2)
ce64edfe7 2026-11-11 Niko1221: image: the steps between the image parts as stable-diffusion.cpp makes them (step 5, joined program, piece 1)
935165402 2026-10-28 cobra91: Trimmed reload: reset the process-wide layer range before each stage reloads
7f57e4c24 2026-10-28 cobra91: Per-card weight trimming on --layer-split auto, from Hardin22's Strata-DualGPU (d9ff514), rebased onto main
59e075881 2026-11-11 Niko1221: tools/vision: our picture reader is the default (owner 11-11: "Our tower, the other selectable"); llama.cpp's mtmd reader stays selectable and takes over by itself where ours was measured slower or does not start
f9a09885c 2026-10-28 cobra91: Layer split: keep the draft head's room out of the last card's cache (from Strata-DualGPU)
b1b8b8d3d 2026-10-28 cobra91: Split search: price a pipelined two-stage split by its slower stage (from Strata-DualGPU)
27108a4f2 2026-11-11 Niko1221: docs: STRATA_RESIDENT_PIN=0 also covers the automatic RAM copy
c28474dc4 2026-11-11 Niko1221: automatic RAM copy: two lines in the owner's wording of 11-11 morning
9e19948ff 2026-11-11 Niko1221: split: the golden dot test draws its q8_1 scale and sum in a fixed order (same inputs under g++ and clang)
9b4cedd08 2026-11-11 Niko1221: image: the latent's VAE input and the 8-bit picture as stable-diffusion.cpp makes them (step 5, part 3)
89b4d9f1f 2026-11-11 Niko1221: image: initial noise in our own code (step 5, part 2)
6edd6f21a 2026-11-11 Niko1221: image: PNG writer of our own, stored deflate blocks (step 5, part 4)
8ee4250e5 2026-11-11 Niko1221: image: Turbo sampler in our own code, byte-identical to stable-diffusion.cpp (step 5, part 1)
18795cfdb 2026-11-11 Niko1221: image: strata-dit-step --f16-resident, a measurement switch (D4)
bb5f308b9 2026-11-11 Niko1221: image: DiT kernels write the GEMM inputs as f16 directly (D4, second piece)
1705c8b9f 2026-11-11 Niko1221: image: Qwen-Image-2.1 DiT step without ggml, and the strata-dit-step test program (D4, first piece)
09d67a33d 2026-11-11 Niko1221: image: own DiT GEMMs for the native Qwen-Image-2.1 runner (D1+D2, test builds only)
9495b503b 2026-11-11 Niko1221: prefill: the trellis fused path declines a geometry whose H row would not fit (opt-in STRATA_PF_FUSED_TQ=1)
691fa1c45 2026-11-11 Niko1221: prefill: Hadamard-folded Gyro trellis layers take the fused prompt kernels (opt-in, STRATA_PF_FUSED_TQ=1)
cadeb1f63 2026-11-11 Niko1221: net: a download whose .part file cannot be written fails at once again, not after five minutes
45f138d81 2026-11-11 Niko1221: prefill: the Hadamard-folded down of the Gyro trellis experts on the CUDA fused prompt kernels (opt-in, STRATA_PF_FUSED_TQ=1)
465fcbbc9 2026-11-11 Niko1221: net: a local download source that cannot be opened fails at once again, not after five minutes
ff301f11e 2026-11-11 Niko1221: prefill: the Gyro trellis experts (TQK6 / TQK7, TQ2_T) on the CUDA fused prompt kernels (opt-in, STRATA_PF_FUSED_TQ=1)
eb92671d6 2026-11-11 Niko1221: nv_defaults: sm_86 no longer turns STRATA_ADAPT_NOWAIT on (option 2; WAITS FOR THE OWNER)
2ce881de5 2026-11-11 Niko1221: server: repeatable output on by default (WAITS FOR THE OWNER; do not merge before his word)
6a56a44a2 2026-11-11 Niko1221: prefill, serve: the CPU prompt share is learned once and kept in the draft cost table file (opt-in)
54f9cc3c0 2026-11-11 Niko1221: tools/vision/own: the CPU tower's attention streams less (V packed per head, 96 query rows a task, a one-vector tail tile); bit-identical; STRATA_VIT_PROF stage times
9b242bb5b 2026-11-11 Niko1221: Image generation, DiT: Qwen-Image-2.1's token positions and RoPE table in our own code, byte-identical to stable-diffusion.cpp's (not used by any build yet)
384e336f7 2026-11-11 Niko1221: Image generation gate tools: dit_ref.py, a numpy reference of one Qwen-Image-2.1 DiT call (test-only), and stage hooks for the DiT's inputs and RoPE tables
c915680bd 2026-11-11 Niko1221: prefill: register-lean Q6_K gate/up loads on the CUDA fused prompt kernels (opt-in STRATA_PF_FUSED_Q6K=1, same bits)
666bef70a 2026-11-11 Niko1221: Image generation, text encoder: our own Qwen2 tokenizer, prompt-weight parser and template, ids identical to stable-diffusion.cpp's (not used by any build yet)
c25a71c6c 2026-11-11 Niko1221: serve: a draft cost table is learned after 1,000 timed rounds, not 1,500
a32d1b368 2026-11-11 Niko1221: server: by default --draft-costs goes only to an engine seen to have it
38f164d00 2026-11-11 Niko1221: data: settings register for the fixed draft costs (STRATA_SPEC_FIXED, STRATA_SPEC_FIXED_TABLE) and the moved lines
bb21ee1f5 2026-11-11 Niko1221: server: pass --draft-costs <file> when "draft_costs" is on (off by default for now)
4c999bcde 2026-11-11 Niko1221: serve: --draft-costs FILE learns this machine's draft cost table once and then fixes it (opt-in)
4079483b6 2026-11-11 Niko1221: spec: fixed window costs, a plain-mean cost learner and the table file for the draft policy (default unchanged)
aaf8c52a8 2026-11-11 Niko1221: Image generation, text encoder: weight decoders write 8 values per thread with one 16-byte store (same bits, about 2.2x faster)
44c4224d2 2026-11-11 Niko1221: Image generation, text encoder: weights uploaded through pinned chunks, and a streamed mode for cards under 14 GiB (test program only)
878ddd852 2026-11-11 Niko1221: split: stored reference digests for the decode dots (qdot_golden.txt) and their check without ggml (split_qdot_golden)
f68367446 2026-11-11 Niko1221: Image generation, text encoder: Strata's own Qwen3-VL text encoder on CUDA / HIP, test program only (no build or product path uses it)
1cb8b6a0d 2026-11-11 Niko1221: Image generation, text encoder: GGUF weight decoders to f16 rows on CUDA / HIP (not used by any build yet)
cacaa6643 2026-11-11 Niko1221: tools/vision/own: the Qwen vision tower on a Mac's GPU (Metal)
6f041b336 2026-11-11 Niko1221: prefill: Q6_K gate/up with a Q8_0 down on the CUDA fused prompt kernels (opt-in, STRATA_PF_FUSED_Q6K=1)
794092c46 2026-11-11 Niko1221: strata-q36: say a context the card cannot hold before the allocation fails (#5715)
1fea75a42 2026-11-11 Niko1221: App: Qwen3.6's context estimate from the catalog's own figures (#5715)
d663e0c63 2026-11-11 Niko1221: Image generation gate tools: te_ref.py, a numpy reference of Qwen-Image-2.1's text encoder (test-only)
9651f8c4f 2026-11-11 Niko1221: prefill: Q8_0 gate/up with a Q8_0 down on the CUDA fused prompt kernels (opt-in, STRATA_PF_FUSED_Q8GU=1)
2f1f915aa 2026-11-11 Niko1221: tests: serve/winjob.py's two process starts are on the spawn-site list
fe62b42c6 2026-11-11 Niko1221: prefill: Q8_0 down behind an i-quant gate/up on the CUDA fused prompt kernels (opt-in, STRATA_PF_FUSED_Q8D=1)
9e8502b76 2026-11-11 Niko1221: Qwen3.6: recommend the context that fits the card, and say it before the start when it does not (#5715)
ebe1fcc9b 2026-11-11 Niko1221: Qwen3.6: one figure for the conversation memory per token and the card's fixed share (#5715)
56630caca 2026-11-11 Niko1221: Image generation: images "vae_decoder" switches sd-cli to Strata's own VAE decoder (CUDA / HIP builds; default stays stable-diffusion.cpp's)
4aa298595 2026-11-11 Niko1221: split: the memory-lock log lines are final (owner's wording of 11-11), placeholder markers removed
40334701c 2026-11-11 Niko1221: expert cache and RAM copy: the free-memory line and the automatic RAM copy's lines in the approved wording
ca9c53c1f 2026-11-11 Niko1221: robustness: the stall report's prompt lines and the Windows resume error in the approved wording
feaa928f9 2026-11-10 Niko1221: resident RAM copy: STRATA_RESIDENT_PIN also for the automatic copy; its clamp line names no flag
5d87c4d8e 2026-11-10 Niko1221: serve (Windows): a child is in the kill-on-close job before it runs, so what it starts at once is too
b38d9f898 2026-11-10 Niko1221: tests: the running-engine stand-in no longer depends on the system's sleep
92f7e8198 2026-11-10 Niko1221: tests: the CPU parity tests skip only their bit-equality leg in older-CPU builds
711a7e937 2026-11-10 Niko1221: engine: the stall report asks the prompt path's compute stream whether its work is done
cfe755e7a 2026-11-10 Niko1221: launch: the worker thread's last calls to the screen are guarded like the others
07df43732 2026-11-10 Niko1221: tests/quant/golden_x86.txt: the oracle's reference, and comments that state the contract
bbf97633c 2026-11-10 Niko1221: serve: the STOP of a request that ends early never raises, whatever state the engine's pipe is in
a215f95d5 2026-11-10 Niko1221: quant_parity: a gate leg against stored reference digests, the live ggml compare for information
f88ea5bb0 2026-11-10 Niko1221: tests: the refused-port checks of the network tests allow Windows' own refusal time (lane 15)
a7f384efe 2026-11-10 Niko1221: setup and the plan accept an Unsloth mmproj-F16.gguf the person already has as the Flash-Next picture reader (lane 15, item 7)
70bfa88d6 2026-11-10 Niko1221: tests: no test reaches the network (lane 15)
2d2773239 2026-11-10 Niko1221: quant_parity: the same test inputs under every compiler
e77c407b8 2026-11-10 Niko1221: net: the first-run screen shows the waiting line in the stage text's element (lane 15)
be9d5f509 2026-11-10 Niko1221: net: --model-path no longer fails on a folder Strata cannot write to, and writes nothing beside the person's model files (lane 15, item 5)
4c0626849 2026-11-10 Niko1221: net: updates, components, the draft layer and the other transfers follow the one network rule (lane 15, item 2)
34ae0dcc0 2026-11-10 Niko1221: docs: the Windows install line carries a time limit (lane 15)
54002e83f 2026-11-10 Niko1221: net: install.ps1 gives up on a silent server and keeps a slow download (lane 15, item 6)
84069c4fd 2026-11-10 Niko1221: docs: the Linux and Mac install line carries a connect and a total limit (lane 15, W12)
c5d4e5172 2026-11-10 Niko1221: net: install.sh's fetch() gives up on a silent server and keeps a slow download (lane 15, item 3)
0988d0c67 2026-11-10 Niko1221: net: the launch plan says what the start will do with --data-dir and with a picture reader that is not the pinned file (lane 15, item 4)
fd40eb0fd 2026-11-10 Niko1221: net: setup's downloads and launch's model step say what they wait for, and a silent host fails in about 44 s, not 320 s (lane 15, item 1)
cc4f2dfe3 2026-11-10 Niko1221: netpolicy: one rule for network calls on install, update and launch (connect 12 s then 30 s, one retry, host memory per run, 60 s stall, 5 min give-up, waiting line after 5 s)
97b14b6b0 2026-11-10 Niko1221: Image generation, VAE decoder: faster open - the file read in parallel parts, every weight converted straight into one staging buffer over the image program's threads, one device allocation and one copy
dedb0b1be 2026-11-10 Niko1221: split: the host-read tables are locked as far as the machine allows (PLE table first), never a failed start
9257f5f03 2026-11-10 Niko1221: split: memlock.hpp, locking the host-read tables as far as the machine allows, with its unit test
bd3c30f53 2026-11-10 Niko1221: Image generation: sd-cli with Strata's VAE decoder builds for HIP (HIP_ARCHITECTURES on the library defined before enable_language(HIP)); build_variant.py keeps build_sd.py's ROCm environment
cab47f3d2 2026-11-10 Niko1221: Image generation, VAE decoder: f16 headroom for the block-4 shortcut (fixed shift 11), GEMM blocks on the picture's pixel grid (row bands byte-identical on HIP too), and no broken picture on a non-finite value
5b6396fda 2026-11-10 Niko1221: prefill: 128-row fused tile from 119.9 rows an expert on sm_120 cards with 40 to 79 SMs; pick_ww's rule as a tested pure function (CUDA, same output bits)
7ee50cc8c 2026-11-10 Niko1221: split: price each stage's prompt loan on its own card (#5722)
e008709d7 2026-11-10 Niko1221: expert cache: a failed free-memory query is said with its error, not passed off as 0 free (#5708, part)
e09b23383 2026-11-10 Niko1221: Image generation: the VAE decoder always takes the row-band path (coordinator 11-10: one path for small and big cards); the one-pass decode stays as the reference the byte-identity gate compares against
9f56c1f04 2026-11-10 Niko1221: test_setup_download: the killed-download test no longer depends on timing, and covers the one-stream path as well
7545928ff 2026-11-10 Niko1221: launch --plan names the Main card the start will make: one function for the card order
bbf2a5476 2026-11-10 Niko1221: Image generation: the VAE decoder's small-card path, the same bytes as the one-pass decode in less memory (owner decision 11-10, option A); off unless asked for
8c71c4927 2026-11-10 Niko1221: conversation cache: an evicted parked conversation gives its RAM back to the system (#5697)
de57c8396 2026-11-10 Niko1221: calibrate: build the engine arguments with the engine program, as the server does (#5720)
b7713cf42 2026-11-10 Niko1221: setup: a build folder whose CUDA toolkit changed drops the cached CUDA paths (#5717)
379a2465d 2026-11-10 Niko1221: Image generation: sd-cli gets Strata's VAE decoder behind --model-args strata_vae=1 (tools/image/sdcpp_vae/apply.py, CUDA / HIP builds only; nothing calls it yet)
3a1e3cc64 2026-11-10 Niko1221: setup: bare_auto_is_32768 follows the engine's rule for compute capability 7.0 too
c7c78ed4f 2026-11-10 Niko1221: NVIDIA: a bare --prefill auto takes the 32768 chunk ceiling on compute capability 7.0 (Volta) single cards too
f7d8aa28e 2026-11-10 Niko1221: Image generation: Strata's own VAE decoder for Qwen-Image-2.1 (src/image/vae, CUDA; HIP from the same source through hip_compat), not wired into anything yet
750a72650 2026-11-10 Niko1221: test_bench_stop: a failure of the child-and-its-child test says which check it is and what survived
d7611e03c 2026-11-10 Niko1221: Image gate: a numpy reference of Qwen-Image-2.1's VAE decoder (vae_ref.py), as stable-diffusion.cpp 2988060 runs it for one picture
4d76d7278 2026-11-10 Niko1221: test_winjob: the failure message no longer calls an exited process "NOT the process held"
26c3b6441 2026-11-10 Niko1221: test_winjob: hold the child and grandchild by handle, and say which process is left on a failure
dbb2d168c 2026-11-10 Niko1221: When the GPU reader did not start for any other reason, the summary says pictures are read on the processor
7e8206b50 2026-11-10 Niko1221: The picture reader's need in the sentences is its whole need at its image limit, not the one allocation that failed
c53e45a35 2026-11-10 Niko1221: The picture reader falls back to the processor in every mode instead of ending the launch
78eaaf1b0 2026-11-10 Niko1221: A picture reader that cannot start for lack of GPU memory is reported as that, with the card, the size and the next step
4cce1ee4d 2026-11-10 Niko1221: The picture reader's READY pipe: one deadline, stray lines kept and logged, a printing reader is never killed
38ad0bcbd 2026-11-10 Niko1221: The product never starts a debugger: every child it starts gets GGML_NO_BACKTRACE=1
42d502a06 2026-11-10 Niko1221: Snapshot driver: a command run in the test process does not change the environment the engine's is compared with
fccdb48a3 2026-11-10 Niko1221: Tests for the image noise switch: the exact sd-cli argument list with the switch off, the merged model-args string, the refusal for a build without the generator, the build stamp and rebuild decisions; run_set.py --noise for the gates
4b9682183 2026-11-10 Niko1221: Image generation: the noise switch. images "noise": "strata" (default "sdcpp", nothing changes) adds strata_noise=1 to sd-cli's --model-args, merged with the native runner's; setup --image-noise on (hidden) builds sd-cli with the generator and stamps the build, only then, so nobody compiles again unasked; a config that asks for it with an sd-cli built without it fails with a plain message and one next step
55b3fc77a 2026-11-10 Niko1221: Image gate: the sampler contract (numpy float32 euler and flow scaling, bit for bit against sd.cpp's final latent), a test for the noise patch and stream, and build_variant --noise
a9f27d068 2026-11-10 Niko1221: Image generation: Strata's noise generator for sd-cli (off unless --model-args strata_noise=1), tools/image/sdcpp_noise
480883606 2026-11-10 Niko1221: Image gate: the stage limits as constants, each with the sd.cpp floor it was set from, and a checker for compare.py / stage_cmp.py results
abf297b35 2026-11-10 Niko1221: Image generation gate harness and Strata noise generator (test tools only)
083b1ac82 2026-11-10 Niko1221: prefill: 128-row fused tile from 112 rows an expert on sm_120 cards with 100 to 149 SMs (CUDA, same output bits)
79740c23c 2026-11-10 Niko1221: prefill: 128-row fused tile from 159.9 rows an expert on sm_120 cards with 80 SMs and up (CUDA, same output bits)
7726f80cb 2026-11-10 Niko1221: test_cfg_paths, test_component_start: the starts give the stub server 60 s, not 15-20 (a pass still returns as soon as it is ready; on a Windows PC with about 330 processes and a non-elevated account a start took 16 s against a 15 s wait)
8bbd64e97 2026-11-10 Niko1221: parallel-chats test: the scratch folder's removal retries (a chat save that landed while it was being removed failed the teardown with ENOTEMPTY on a macOS runner)
82ab8ac76 2026-11-10 Niko1221: test_recipes: the interrupted run is found by excluding the two known runs, not as the newest by file time (three runs in one tick of a coarse Windows clock came back in any order)
79d529cc7 2026-11-10 Niko1221: procs.orphans_of on Windows: names first, a command line only where the image name can be the engine's file (reading every command line took 4-9 s per server start on a Windows PC with about 280 processes and a non-elevated account; now 0.1 s warm, 2 s cold)
3e1fcaaf6 2026-11-10 Niko1221: serve: the HTTP server binds without a host name lookup (http.server's server_bind asks getfqdn, which stalled 35 s per start on GitHub's macOS runner; nothing reads server_name)
42e97db85 2026-11-10 Niko1221: test_runtime: the start, restart and verify waits give the stub server 60 s (operations 80 s), not 10-20 (a pass still returns as soon as it is ready; on a Windows PC with about 280 processes and a non-elevated account, the server's leftover-engine scan alone took 4-9 s and the budget ran out)
35ad5b471 2026-11-10 Niko1221: test stubs: mcp_fake_server and cutserver bind without the getfqdn lookup (they run as fresh child processes)
c7b446fa8 2026-11-10 Niko1221: test_setup_feed_models TerminalAndApp: the table's Strata reads a fixed NVIDIA PC, not the card of the PC the tests run on (on a PC with an Intel Arc card, install_plan went down the Intel path)
50c753f5d 2026-11-10 Niko1221: host tests: assert-private reads the DACL through .NET File.GetAccessControl and compares it by SID (Get-Acl's module did not load in Windows PowerShell under a PowerShell 7 parent; SDDL writes the runner's built-in Administrator as the alias LA)
b250bc78a 2026-11-10 Niko1221: test_drafting_tuned: a same-size rewrite moves the file clock on before the marker check, as test_drafting_selector_q4 does (same tick on Windows kept mtime_ns)
ea6826cc8 2026-11-10 Niko1221: test_setup_golden: the config a run wrote is the new or changed file, not the newest time (same clock tick on GitHub's Windows runner picked the config placed before; setup wrote the named size)
e906e7e97 2026-11-10 Niko1221: test_strata_mcp: the fake model server binds without http.server's getfqdn lookup (a fresh child on GitHub's macOS runner did not answer within 30 s)
13e7188cc 2026-11-10 Niko1221: images: the answer's background says what the picture is: "transparent" also when a picture kept its alpha because it could not be put on white (the logged fallback), "opaque" for a white or an RGB sd-cli picture (_flatten reports whether the returned PNG has an alpha channel)
3a0916c5e 2026-11-10 Niko1221: docs/IMAGES.md: the background request field, the answer's background and strata.flatten_s, and the picture on white (the API's PNG is no longer byte for byte sd-cli's unless background is transparent)
631b28030 2026-11-10 Niko1221: images: pictures are put on white by default. Qwen-Image-2.1 decodes RGBA and leaves some backgrounds transparent over a flat key colour; the server now composites each picture on white and returns an 8-bit RGB PNG (flatten_png: zlib 6, every chunk other than IHDR / IDAT, sd-cli's "parameters" text above all, copied byte for byte; 0.12 s median, 0.22 s max per 1024-1536 picture with Pillow, 0.62 / 1.09 s on the zlib + numpy fallback). background: "transparent" keeps sd-cli's PNG unchanged; opaque / auto / none give the white one; other values are refused. A PNG that cannot be rewritten goes out unchanged with one log line. The response carries background and strata.flatten_s
88fc47ccf 2026-11-10 Niko1221: tools/vision: `--tower auto` uses our GPU tower on every CUDA class when the reader starts with --max-tokens above 1,024 (the default GPU limit), whatever the speed: at 16,384 tokens mtmd-GPU reads 0.81 to 0.83 against mtmd-CPU (A4000 0.813, RTX PRO 5000 0.834, P100 0.834), ours 0.9996 to 0.99998, at a time cost on Pascal (P100, Qwen3.8, 16,384 tokens: 196.6 s against mtmd-GPU 129.0 s); at or below 1,024 the speed rules stay (Pascal with F16 matrices and cc 6.1 / 6.2 keep mtmd); AMD gfx1151 and Metal unchanged; own_reader_supported and prefer_mtmd take max_tokens; unit test
8079fca53 2026-11-10 Niko1221: prefill: Q5_0 down projections on the CUDA fused prompt kernels (opt-in, STRATA_PF_FUSED_Q50=1)
ea16bfd30 2026-11-10 Niko1221: images: the text-encoder time reaches /v1/status and the response again: stable-diffusion.cpp 2988060 (the pinned commit) prints "get_learned_condition completed, taking 0.70s", the pattern only read the "N ms" form some older revisions printed (from b636886, 2024-02); both forms are read now (log_figures), the fake sd-cli prints the pinned form
87d971592 2026-11-10 Niko1221: tools/vision/own: the CPU tower's elementwise kernels (GELU, LayerNorm, add, the online-softmax step) run on a raw vector type with free inline functions (VR, vr_*): __m256 / __m512 in the AVX2 and AVX-512 tiers (STRATA_KN_RAW), the old struct V through adapters in the scalar and NEON tiers; the same operations in the same order (MSVC kept the wrapper struct in memory, the rest of its CPU speed miss). GCC: outputs byte-identical old vs new on 6 pictures x 2 models on p2006 AVX-512, AVX2 and scalar and on z440 AVX2 (Qwen3.6); no weak symbols in the tier objects; unit test passes; speed new/old 0.97 to 1.00 (big1024 AVX-512 0.982, AVX2 0.979 / 0.992, scalar 1.002). MSVC not measured
1bf13cd02 2026-11-10 Niko1221: prefill: Q8_0 down behind a K-quant gate/up on the CUDA fused prompt kernels (opt-in, STRATA_PF_FUSED_KQ=1)
18027b91c 2026-11-10 Niko1221: prefill: register-lean K-quant gate/up loads in the CUDA fused prompt kernels (opt-in, STRATA_PF_FUSED_KQ=1)
58414f3ec 2026-11-10 Niko1221: split: own decode dots (src/qdot.cuh), no ggml-cuda header in the engine
e83138654 2026-11-10 Niko1221: tools/vision/own: Pascal (cc 6.x) holds BF16 matrices as F16 (cuBLAS has only a slow BF16 kernel there: 645 against 497 ms of a 1,024-token picture on a P100) and, with them, takes a 32M-score attention chunk; `auto` now reads with our tower on cc 6.0 when the mmproj's matrices are BF16 (Qwen3.8: P100 gate PASS, rule 1 min 0.999636, 0.32 to 1.00 of mtmd-GPU's time, 1,362 against 1,364 MiB) and keeps mtmd with F16 matrices (Qwen3.6: mtmd's F16-accumulating products stay faster, ours 0.75 to 1.37) and on cc 6.1 / 6.2 (not measured); STRATA_VIT_BF16_AS_F16 diagnostic
df52e70b4 2026-11-10 Niko1221: tools/vision/own: above 16,384 patches the GPU attention pads its score rows to 64 elements and takes a multiple of 64 queries per chunk (limit_7000x5000.png, 65,232 patches, on the RTX A4000: 108.1 s -> 80.3 s, 0.79 of mtmd-GPU (was 1.07), rule 1 0.999982, 3,168 MiB against 3,656; limit_4096x4096.png 0.78, unchanged); pictures up to 16,384 patches unchanged; STRATA_VIT_NPAD / STRATA_VIT_QALIGN diagnostics. HIP shares the code, not measured there
15a80a9ef 2026-11-10 Niko1221: prefill: Q4_K / Q5_K gate/up with Q5_1 down on the CUDA fused prompt kernels (opt-in, STRATA_PF_FUSED_KQ=1)
8b0988d72 2026-11-10 Niko1221: tests: K-quant gate/up pairs judged against the int8 model and FP32, not against MMQ
451d6e74c 2026-11-10 Niko1221: prefill: Q5_0 down projections on the CUDA fused prompt kernels (opt-in, STRATA_PF_FUSED_Q50=1)
96fef73d2 2026-11-10 Niko1221: prefill: IQ2_XXS / IQ2_XS gate/up fused by default on gfx12 under Linux (the IQ3_XXS class, 0.2.15; owner 11-10)
f7ce2b930 2026-11-10 Niko1221: prefill: Q5_0 down fused by default on gfx12 under Linux (UD-IQ4_XS-v31, 0.2.15; owner 11-10)
4558513fa 2026-11-10 Niko1221: tools/force_check.py: the neutral-writer gate for prompt-arithmetic changes (cut, gen-neutral, gate)
5970398ea 2026-11-10 Niko1221: settings register: STRATA_PF_KQ_OCC (the K-quant occupancy-launch trial switch of e99f83271; research, HIP only, off by default)
e985dd3d5 2026-11-10 Niko1221: prefill: K-quant fused prompt experts on the occupancy launch, trial switch STRATA_PF_KQ_OCC=1 (HIP, off by default)
49bf891e7 2026-11-10 Niko1221: make_model_release --checklist <file>: the internal release checklist by path, filled beside the repo's default notes and model card (no second copy of the public templates in a private folder); a missing file is refused before anything is written
5ce203f59 2026-11-10 Niko1221: make_model_release: the release templates (the notes and the model card) live in the repo, packaging/templates/model-release, and are the default of --templates (another folder can still be named); the templates test reads them on every box (the internal release checklist stays out of the repo)
87dfca0e7 2026-11-10 Niko1221: test_strata_mcp MacCatalog: the second temp data folder (f-0214-app's disk-short check) under the real home on macOS too
c47df69e0 2026-11-10 Niko1221: test: the phaseA-tests templates check gives --min-engine as a real case-A caller must, and first checks that without it the script refuses (078b52563 made it required; the check only runs on the owner PC, so it was not run after that)
562fa312e 2026-11-10 Niko1221: test: hermetic drafter-fetch test and no pytest tmp_path in the 0.2.14 tests (Windows gate of f-0214-app)
fd14cd685 2026-11-10 Niko1221: tools/vision/own: when the large attention chunk above 16,384 patches does not fit, the GPU towers take the default chunk instead (slower, never an error; CUDA and SYCL); STRATA_VIT_SCORES_LARGE (a diagnostic) sets the large size; checked on z440 (falls back to 106.5 s at 2,272 MiB, rule 1 0.999981) and the A750 (147.8 s, rule 1 0.999696)
e3a04c013 2026-11-10 Niko1221: test_strata_mcp MacCatalog: the temp data folder under the account's real home (pwd), not HOME, which the fake root points at a temp folder
872a7bcb2 2026-11-10 Niko1221: test_strata_mcp: the macOS expectedFailure marks come off (lane 3's zombie fix, f-0214-app, lands first: an unexpected success would fail)
b6a7915c8 2026-11-10 Niko1221: serve/test_server.py: LF line ends again (the hip_ordinal edit had written the whole file with CRLF)
0645f2ede 2026-11-10 Niko1221: tests: suites that read the box they run on (Boston, p2006, p1006, macOS)
8c593a000 2026-11-10 Niko1221: tools/vision/own: the AVX2 and AVX-512 tiers' product micro-kernels on raw __m256 / __m512 (no wrapper struct in the hot loop, for MSVC); the same operations in the same order: outputs byte-identical to the previous kernels on p2006 (AVX-512 and AVX2) and z440 (AVX2), GCC speed level (p2006 big1024 7,189 against 7,271 ms, 5 pairs)
cab87a2e8 2026-11-10 Niko1221: tools/vision/own: --tower auto keeps mtmd on an MSVC-built x86 CPU reader (owner PC, Zen 4: 33.4 s against mtmd-CPU's 18.5 s at 1,024 tokens, while the GCC build is 0.80 to 0.95 of mtmd-CPU); keyed on the compiler, not the OS; unit test; --tower own unchanged
804d2032d 2026-11-10 Niko1221: tests: a nvidia-smi that answers nothing comes first on PATH for the Python suites on POSIX, so a box with an NVIDIA card runs them as GitHub's runners do (p1004's P100: 64 stub-engine update tests failed against the stand-in packages' sm_86 code)
dd04305ef 2026-11-10 Niko1221: tools/vision/own: --tower auto keeps mtmd on AMD gfx1151 (Strix Halo), where rocBLAS ships only fallback kernels and the own HIP tower takes 1.73 to 3.03 of mtmd-HIP's time (Windows, Strix); the Pascal and gfx1151 rules are pure functions in vit_gpu.h with a unit test; --tower own unchanged
1c50fe076 2026-11-10 Niko1221: make_model_release: the plan prints the exact strata launch lines with the size name a person types (<quant>-<id> when the quant's name is a built-in size, as feed_models.py decides)
9e5030307 2026-11-10 Niko1221: feed_tool: an OPT-IN multi-threaded gzip for tar.gz packages (STRATA_PACK_THREADS >= 2: 4 MiB gzip members compressed in parallel, the same bytes for the same tree); unset, the archive is the single-stream tarfile gzip of before. Published 0.2.12 / 0.2.13 Terminals, install.sh and the 0.2.13 AppImage's Control install from such a feed (not the default until every reader is shown)
8cf002e1b 2026-11-10 Niko1221: test: drafting.test.mjs's second source check reads the first-load condition too
9e5f5a5ed 2026-11-10 Niko1221: tools/vision/own: --tower auto uses our CPU tower on Arm (NEON gate on the DGX Spark: rule 1 PASS on both models, 0.57 to 0.81 of mtmd-CPU's time on F16 and 0.08 to 0.13 on BF16); the scalar-only rule stays for x86 without AVX2 only
5abd6688d 2026-11-10 Niko1221: tools/vision/own: the NEON tier's own product micro-kernel with lane-indexed FMAs (8 x 8 tile, one vector load per A row for four k steps; the same summation order, outputs byte-identical to the previous NEON tier): DGX Spark Qwen3.6 F16 0.57 to 0.81 of mtmd-CPU's time (was 1.14 to 1.24 on the large pictures)
dcd0ac160 2026-11-10 Niko1221: tools/vision/own: the AVX2 F16 rounding passes _MM_FROUND_TO_NEAREST_INT alone to _mm256_cvtps_ph (the VEX form takes a 3-bit rounding value; MSVC C4556); GCC encoded imm 8, which the hardware reads as round to nearest too: outputs byte-identical with STRATA_VIT_REF_ROUND=1 on F16 weights
92d379070 2026-11-10 Niko1221: tools/vision/own: the Arm NEON kernel tier of the CPU tower (cpu_kernels_neon.cpp, baseline AArch64, 12 x 8 tile, on the cpu_tier.h contract; quant::Isa::Neon is the best tier on AArch64, STRATA_FORCE_ISA=scalar still forces the portable one); --tower auto keeps mtmd on Arm until the gate is accepted
d894c3168 2026-11-10 Niko1221: tools/vision/own: a larger attention score chunk above 16,384 patches on the GPU towers (CUDA / HIP 512M scores, SYCL 256M): at 16,384 tokens l620 33.4 s -> 24.8 s (0.87 of mtmd-GPU, 3,398 MiB against its 3,858), A750 147.9 s -> 118.3 s; pictures up to 4,096 tokens unchanged; STRATA_VIT_SCORES still sets one size for all
95e9b7341 2026-11-10 Niko1221: setup: the first range probe of a parallel download is tried again after a hiccup (proposal, from lane 8)
7ea172159 2026-11-10 Niko1221: strata_mcp: without /proc (macOS) an ended child that is not reaped yet is not "running"
e481f3b6b 2026-11-10 Niko1221: Control: a model whose draft layer is off keeps the server's own "without the draft layer" step; the app's first-load test shape
81f7422c1 2026-11-10 Niko1221: Desktop (Linux): the restarter closes inherited files in the new app only, not in itself
a84619034 2026-11-10 Niko1221: tests: the vision-build tests name an AVX2 CPU (a box without one, or a Mac, rebuilt the engine with an ISA floor); the feed command-line tests run setup.main() as on Linux on a Mac
e9239a87d 2026-11-10 Niko1221: tools tests on macOS: only setup.py and strata_mcp see linux (a module-level sys view), the CPU reads x86_64; the three MCP install-job tests are expected failures on macOS (a zombie child reads as running there: product bug, reported)
cdbb312bb 2026-11-10 Niko1221: test_setup_download: one stream means one stream without setup's one-byte probes (a server without ranges answers the probe with the whole file, which can still be sending when the stream starts: 2 of 10 runs on p2006)
99b3dc624 2026-11-10 Niko1221: tools/conftest.py: on macOS each tools test runs as on the Linux x86 runner (sys.platform, platform.system/machine, sysinfo.machine), not only setup.py's view; the Apple CPU read as ARM64 and strata_mcp took the Mac path
aa2a3f956 2026-11-10 Niko1221: tools/vision/own: --tower auto keeps mtmd on a CPU that has only the portable kernel tier (x86 without AVX2, Arm until a NEON tier exists), where the own CPU tower is 2.1 to 3.7 times slower than mtmd-CPU; --tower own unchanged
737ab4f26 2026-11-10 Niko1221: test: the Strix app-vs-launch reserve test compares the two engine lines with each scratch world's folder written as <ROOT>
6311744b3 2026-11-10 Niko1221: tools/vision/own: the Qwen vision tower on Intel GPUs (vit_sycl.cpp: SYCL kernels + oneMKL, the VitGpu class of vit_gpu.cu with the attention context written head by head and a 64 MB score chunk; strata-vision-sycl --tower own --gpu); gate_gpu.py reads GPU memory from Linux DRM fdinfo and reports whether our GPU tower is byte-repeatable
b56dc8acf 2026-11-10 Niko1221: tools/vision/own: the AVX2 / AVX-512 kernel files hold no standard-library code (cpu_tier.h, C headers and intrinsics only; min / max / copy / zero as their own internal helpers, expf through an out-of-line baseline function), so no inline library function is compiled with their ISA flags and kept for the whole program; outputs byte-identical on every tier
2e25954e5 2026-11-10 Niko1221: ci: a diagnostic step on the Windows host job shows what Windows PowerShell 5.1 children return under a PowerShell 7 parent (hardware probe, setup cpu_info)
f328c2cd2 2026-11-10 Niko1221: test_setup_download: a killed download may have taken the one-stream path (one failed range probe); its .part is then read as finished pieces, as setup itself reads it
78451ea77 2026-11-10 Niko1221: test: the Strix reserve field test of the hardware report no longer patches sys.platform (it broke shutil.which on Linux)
3801ec40a 2026-11-10 Niko1221: SYCL router: an fp32 router for a card without fp64 (Intel Arc A/B-series) - a model of another shape (Qwen4: top-8, 256 experts) routes through the generic router, whose double kernel the Arc runtime refused ('double' is not supported), ending the engine at its first token; a card with fp64 keeps the double kernels; the parity test covers the Qwen4 shapes and compares fp32 with double on the same inputs
8cfd842c7 2026-11-10 Niko1221: tests: pass on GitHub's macOS runners
46e84e239 2026-11-10 Niko1221: Intel Arc: a model of the signed feed starts (Qwen4 day) - the Terminal's and the app's Arc run config takes a feed qwen4exp model (Unsloth layout, its one GGUF or its shards, no Flash-Next draft layer, drafter none -> drafting off, the neutral expert profile for another shape) and a model of its own shape on its engine component (component:strata-q4-<shape>; the app's Arc setup fetches that engine first); the built-in families' configs are unchanged
078b52563 2026-11-10 Niko1221: make_model_release: --title (the model's title in the entry and the notes; default the file's general.name, as before), and case A with --write needs --min-engine instead of leaving [FILL: minimum engine version] in the entry
1f74860fa 2026-11-09 Niko1221: tools/vision/own: --tower auto keeps mtmd on NVIDIA Pascal (compute capability 6.x), where the own GPU tower is slower than mtmd (P100 gate); --tower own unchanged
ebfc6e62f 2026-11-09 Niko1221: tools/vision/own: the reference attention's query block is static constexpr (MSVC rejected acc[QB][128] with QB a const local used inside the lambda, C2131 / C3863)
b2f268403 2026-11-09 Niko1221: Shape engine: one that cannot answer strata --geometry is refused at install (owner 11-09: "it does not say which model shape it was built for" inside the approved start_failed line); the Strata engine is never asked
d4283e021 2026-11-09 Niko1221: tools/vision/own: the CPU tower rounds to 16 bits by default when the mmproj's weights are BF16 (off for F16), chosen from the GGUF weight type; STRATA_VIT_REF_ROUND=0/1 still overrides; unit test of the choice
7937614e3 2026-11-09 Niko1221: Desktop (Linux) + App: after the in-app update the update job reads done, and no old AppImage runtime is kept alive
8b92e9ace 2026-11-09 Niko1221: Packaging: SHAPE=<geometry> in the Linux engine build scripts (CUDA x86_64 and aarch64/Spark, HIP, SYCL): the engine of a model shape in one command per platform - configured for that geometry (or the header STRATA_CMAKE_EXTRA names), checked with strata --geometry, packaged with --shape, no DeepSeek engine in it; without SHAPE every command is unchanged
75a75e1a8 2026-11-09 Niko1221: Settings > Engine, shape group Use dialog: keep the two reassurance sentences after the new first one
b130a479d 2026-11-09 Niko1221: Settings > Engine: the Use dialog of a Qwen4 model shape's engine says "{model} runs on engine {version} from its next start."
77f7835a8 2026-11-09 Niko1221: SYCL engine: strata --geometry and strata --families, as the CUDA/HIP/Metal program answers them (the Intel program is its own main; without them a SYCL shape engine was installed with no geometry check)
b5dc27e38 2026-11-09 Niko1221: Desktop (Linux): the app comes back by itself after an in-app update
519c7e8c0 2026-11-09 Niko1221: Control: a feed model whose entry says drafter: none starts with no drafter, and the Terminal plans none for it
b47387548 2026-11-09 Niko1221: App: the first-run engine card also takes a newer Strata Control from the feed, and the app switches to it
af9b832fd 2026-11-09 Niko1221: App: the setup prepares the drafter Control's Auto picks for this card; the first load after it fetches a missing MTP layer
06f3beb0c 2026-11-09 Niko1221: App: an engine version that failed its test start is not "up to date"; Update engine tries it again
fdfb2db6d 2026-11-09 Niko1221: App + Control: run-config paths into a gone Control folder (AppImage /tmp/.mount_*) are repaired before updates and loads
9c09f839c 2026-11-09 Niko1221: App: exit 7 from Control's update lock is "an update is already running", and the update waits for the lock
28d669577 2026-11-09 Niko1221: Settings > Engine and strata components engines list the engine of a Qwen4 model shape as its own group, with Use and Delete
afe6c8bc1 2026-11-09 Niko1221: Strix reserve, follow-up: with no setup reserve in the run config the app takes the one setup would write (Control's setup_reserve_mib), else the floor of before
3d8762099 2026-11-09 Niko1221: setup.py: intel_control_setup's docstring no longer says gguf-py is downloaded (nothing is, since the vendored and own GGUF tools)
1f2f737e8 2026-11-09 Niko1221: test_setup_pins: the stand-in pip stamp carries this system's marker, so the Requirements tests do not depend on the Python that runs them (pyyaml missing made the stamp unbelieved)
ecccc359d 2026-11-09 Niko1221: A Models-page Load on a unified-memory chip (Strix Halo) keeps the reserve setup wrote, as strata launch does
731b40fed 2026-11-09 Niko1221: The This computer card places a unified-memory chip's model with the label's rule (carve-out only beside the RAM)
db35f7627 2026-11-09 Niko1221: test: Settings > About still shows an interrupted or failed update with no later finished one (also while a retry runs)
1eec11bd8 2026-11-09 Niko1221: Read pictures unticked holds across a restart on a model set up without the picture files: a choice made with a reader present carries a marker
fb721c37d 2026-11-09 Niko1221: The version list's fit word counts a unified-memory chip (Strix Halo) only for its carve-out, as Control's fit_label does
87ec2e773 2026-11-09 Niko1221: Settings > About checks for updates again after an in-app Strata or engine update finished, so the row no longer keeps "Update available"
8c98f9fdb 2026-11-09 Niko1221: Settings > About no longer shows an update failure that a later finished update of the same component made right
0a6a5ad25 2026-11-09 Niko1221: Menus stay inside the window on WebView2 before 128 at Interface size 125% and up: the window's size is measured like the rectangles (a fixed box), not taken from innerWidth/innerHeight
beed8a517 2026-11-09 Niko1221: tests: pass on GitHub's Windows runners (CRLF, PowerShell 7 module path, classic console, coarse clocks)
8e69b84dd 2026-11-09 Niko1221: gitattributes: chat templates (*.jinja) are LF in every checkout
80cde871b 2026-11-09 Niko1221: ci: the macOS check jobs keep their logs and upload them on a failure, as Linux and Windows do
aec86299d 2026-11-09 Niko1221: tools/vision/own: vectorised 16-bit rounding for STRATA_VIT_REF_ROUND on the CPU tower (round16 per ISA tier, BF16 and F16, plus a bit-exact test against the scalar tier)
423225d87 2026-11-09 Niko1221: tools/vision/own: the CPU path of --tower own is the fast tower (VitCpu); STRATA_VIT_CPU=ref selects the float32 reference
3ea10ec5d 2026-11-09 Niko1221: tools/vision/own: CPU tower keeps its 16-bit weights as panels made once at load (a product task converts a contiguous slice, no per-task transposition: small pictures no longer slower than mtmd-CPU), conv test, speed_pairs.py alternating-pairs speed test
f5db05f10 2026-11-09 Niko1221: tools/vision/own: GPU tower speed on small pictures (short-row softmax kernel sized by row length, score rows padded to 8), STRATA_VIT_PROF stage timings, STRATA_VIT_CPU=fast switch in the reader; fork-join team: the task count carries the run tag (one task ran twice in 31 of 60 test runs), team-only test mode
cc4110ed4 2026-11-09 Niko1221: tools/vision/own: the fast CPU tower VitCpu (kernels per ISA tier, tiled online-softmax attention, fork-join team) with its unit test; STRATA_VIT_CPU=fast selects it, the default stays VitRef
cbc7c02c5 2026-11-09 Niko1221: tools/vision/own: answers_gate.py, the four questions of the Qwen3.6 run and name+round readers (STRATA_VIT_REF_ROUND=1 in the reader's wrapper)
fd1890711 2026-11-09 Niko1221: tools/vision/own: make_sve.py, one reader over pictures into a folder of embeddings
a6337406e 2026-11-09 Niko1221: tools/vision/own: answers_q36.py, the Qwen3.6 answers run (one strata-q36 engine, several readers' embeddings, any number of questions)
066c00ed3 2026-11-09 Niko1221: tools/vision/own: GPU tower STRATA_VIT_REF_ROUND=1 (diagnostic, off by default): every matrix product's result rounded to the weight's 16-bit type as ggml's GPU path hands it back
19b395ec0 2026-11-09 Niko1221: tools/vision/own: GPU gate rule 2 tolerance (ours >= mtmd-GPU - 1e-4, or >= 0.9999 against mtmd-CPU)
47b5f88fd 2026-11-09 Niko1221: tools/vision/own: GPU tower memory (chunked products, F16 scores softmaxed in place, one patch matrix), long-row softmax so no picture is refused, limit pictures and --skip-cpu for the gate, bench tool
f40c5dcb6 2026-11-09 Niko1221: tools/vision/own: HIP build of the GPU tower (one source with CUDA; CMake STRATA_VIT_OWN_HIP / STRATA_VISION_HIP), no ignored status warnings
7b7ff2164 2026-11-09 Niko1221: tools/vision/own: CUDA attention by batched cuBLAS GEMMs (F16 q/k/v, softmax kernel), the GPU gate driver (rule: own GPU vs mtmd-CPU, no noisier than mtmd-GPU, speed, VRAM)
7694bc0bc 2026-11-09 Niko1221: tools/vision/own: worst-token report in the comparison tool, a mtmd-style rounding option for the reference (diagnostic), the answers-gate driver, standalone CMake reconfigure fix
ef108d84c 2026-11-09 Niko1221: tools/vision/own: step 4, the Qwen tower on a CUDA GPU (cuBLAS GemmEx on BF16/F16 weights, float32 activations, tiled online-softmax attention), strata-vision-own for quick builds
290896d80 2026-11-09 Niko1221: tools/vision/own: step 3, the float32 CPU reference of the Qwen tower, strata-vision --tower own|mtmd|auto (mtmd stays the default), the comparison harness against mtmd
c1676778b 2026-11-09 Niko1221: tools/vision/own: step 2, picture preparation (stb decode, smart resize, Pillow-style bicubic with padding, normalise), checked bit for bit against mtmd's preprocessor
75ee0ea87 2026-11-09 Niko1221: tools/vision/own: our own vision tower, step 1: a small GGUF reader and the tower geometry read from the mmproj file
6f19a9662 2026-11-09 Niko1221: third_party/stb: stb_image.h v2.30 from llama.cpp's vendor folder (own vision tower), check_vendored takes it
504b14334 2026-11-09 Niko1221: test: the old-launcher test reads the Terminal version from strata_cli instead of hard-coding 0.2.13 (it fails on 0.2.13.1)
7c09c4a75 2026-11-09 Niko1221: pool_determinism: the pool's native rows and activation quantizers are deterministic (repeats, 1-16 threads, row splits, buffer pre-fills, canaries), 294 format pairs; ctest
ead5a32ae 2026-11-09 Niko1221: STRATA_OWN_CPU_QUANT default OFF on arm64 again (ON builds and is bit-exact; the Spark pool decode measured about 1.5% slower with it)
63ffccf10 2026-11-09 Niko1221: quant layer: MSVC fp16 conversions through the packed F16C intrinsics (no scalar _cvtsh_ss there)
9063d81bd 2026-11-09 Niko1221: quant layer: ue4m3 scale decode through a table (the NVFP4 dots were 5x slower than ggml's with ldexp); quant_bench --rows
e9b2db8e4 2026-11-09 Niko1221: quant layer: generic.hpp uses STRATA_RESTRICT (MSVC has no __restrict__)
a550fd71f 2026-11-09 Niko1221: quant layer: STRATA_OWN_CPU_QUANT defaults ON on arm64; quant_parity skips ggml-cpu flavours that are not the Neon contract; quant_bench (rows against ggml-cpu); run_oracle arm flavours
2fe91fddd 2026-11-09 Niko1221: quant layer: AVX-512 VL+VNNI build of the AVX2-contract dots (Q4_0/1, Q5_0/1, Q8_0, IQ4_NL, MXFP4), quant_bench, check_no_ggml.sh
23332c2d6 2026-11-09 Niko1221: metal: STRATA_OWN_CPU_QUANT builds the engine's CPU rows on the quant layer (OFF by default until the Mac oracle passes)
9740a0962 2026-11-09 Niko1221: quant layer: Arm NEON tier (ggml's NEON dots and Q8_0/Q8_1 quantizers ported, Arith::Neon), arm64 contraction of the Q8_K/Q4_0/dequant references, boundary-value oracle test
6213c0839 2026-11-09 Niko1221: CPU expert pool and the DeepSeek CPU lane on the quant layer: -DSTRATA_OWN_CPU_QUANT (default ON on x86, OFF on arm64), ggml-cpu out of the pool
bbbe364ba 2026-11-09 Niko1221: --mtp-q4 requantizer on the quant layer (behind STRATA_OWN_CPU_QUANT; the ggml-base path stays for the other build)
cc8c29f31 2026-11-09 Niko1221: check_vendored: ignore __pycache__ under the vendored trees (an import of gguf-py writes bytecode there)
e5af60da0 2026-11-09 Niko1221: quant layer: AVX2 and AVX tiers (ggml's x86 dots and Q8_0/Q8_1/Q8_K quantizers ported), dequantizers; bit-exact against ggml-cpu in all three flavours
8a2b0f5f0 2026-11-09 Niko1221: quant layer: type table, CPU probe, Q8_0/Q8_1/Q8_K/Q4_0 reference quantizers, Generic-contract dots for every pool type, self-checks, ggml oracle test
033cfdd8c 2026-11-09 Niko1221: strata-llama: add ggml-blas (ggml turns it on by default on a Mac)
237ecb176 2026-11-09 Niko1221: tools, setup: the preparation tools use strata_gguf / strata_quants; STRATA_GGUF_PY stays an override
f9bbeeb44 2026-11-09 Niko1221: tools: Strata's own GGUF reader/writer and quantizers (strata_gguf, strata_quants), bit-identical to gguf-py; _paths.gguf_lib()
c9af18d10 2026-11-08 Niko1221: packaging/mac/build_engine.sh: the Mac Qwen engine package from the repo, staging the quant header under both names
39c387727 2026-11-08 Niko1221: test: the NVFP4-local tools take the vendored converter
463940282 2026-11-08 Niko1221: strata-vision: llama, mtmd and ggml vendored at the pin (third_party/strata-llama); no llama.cpp download is left
e43ff9885 2026-11-08 Niko1221: release scripts, Docker, CI, Mac setup: ggml is the vendored third_party/strata-ggml, nothing passes STRATA_GGML_DIR by default
04a9fb8e5 2026-11-08 Niko1221: build_sycl_linux.sh, build_hip_gfx1103.sh: drop the FETCHCONTENT_SOURCE_DIR_STRATA_LLAMACPP no-ops
745819efc 2026-11-08 Niko1221: quant header: the text moves to strata-quant-common.h, third_party/ggml/ggml-common.h forwards to it
6f273fc27 2026-11-08 Niko1221: setup: no llama.cpp download to prepare a model or build the engine
525c0be13 2026-11-08 Niko1221: gguf-py and llama.cpp's HF converter vendored at the pin (third_party/strata-gguf-py)
aaf18a4b9 2026-10-26 glorysdj: docs: record rebased B70 IQ3 decode and default-off results
0726ef5ad 2026-10-26 glorysdj: Preserve upstream sign decoding when fast arithmetic is disabled
961f62963 2026-10-26 glorysdj: sycl: isolate opt-in mixed-IQ3 decode optimizations
cb436853a 2026-10-19 Xiangyu Tian: sycl: preview integrated Battlemage IQ2_XS inference optimizations
```

### whisper.cpp — 110 commits

```
6680804f9 2026-11-18 Daniel Bevenius: whisper : bump version to 1.9.6 (#4188)
5f9823760 2026-11-17 Daniel Bevenius: whisper: change visibility of whisper_log_internal to hidden (#4186)
8302b819f 2026-11-17 Daniel Bevenius: sync : ggml
3acf42737 2026-11-13 Georgi Gerganov: ggml : bump version to 1.0.0 (ggml/1690)
96f5e295a 2026-11-12 SaidSultani: fix(hexagon): make host build work with clang-cl on Windows ARM64 (llama/32011)
7863df10f 2026-11-12 Georgi Gerganov: ggml : prune (llama/29801)
83354b8be 2026-11-12 Aparna M P: hexagon: add Q5_0 and Q5_1 support (llama/32094)
d0f586f92 2026-11-12 anujj: Title: CUDA: few-row MMQ for BS 2-24 (llama/31533)
502583e3e 2026-11-12 Kong Jiale: ggml : route GATED_DELTA_NET to the SpacemiT RVV kernel (llama/31897)
f67cb301e 2026-11-12 sliu39: vulkan : Intel FA kernel for prefill. (llama/29357)
34971f203 2026-11-12 Marco Colombo: ggml-cpu: use the 4x4 simd_gemm tile on ARM NEON (llama/32128)
adc0dbc2e 2026-11-12 Konrad Moren: CUDA: Optimize prefil via fuse of w_s scale in epilogue MMQ for nvfp4 checkpoints (llama/26048)
602bd391a 2026-11-12 Aman Gupta: ggml-backend : prefetch only inputs computed by earlier splits (llama/32100)
d061fdf08 2026-11-12 Kong Jiale: ggml : dispatch SpacemiT Q4_1 32x256 through the HP kernel (llama/31929)
46dd746c9 2026-11-11 Titaniumtown: sycl: make oneDNN FA cache thread-safe and memoize runtime failures (llama/31138)
b41b59253 2026-11-12 Neo Zhang: sycl : fix AOT for more than 4GB (llama/31873)
bb83314cb 2026-11-12 zhaoyshine: sycl : use cached device-id in set_main_device (llama/32013)
1e4f16c5a 2026-11-11 Joseph Patricio: CUDA: add cuda debug buffer pool (llama/31919)
80a7c6b8a 2026-11-11 shaofeiqi: opencl: add bin kernel `kernel_gemm_noshuffle_q4_0_f32_32b_trans_ila_a7_bin` (llama/30947)
c7d912a7f 2026-11-12 Feiteng: CUDA: skip empty MoE tiles in MMQ stream-k fixup (llama/32067)
049bfa8e7 2026-11-11 shaofeiqi: opencl: add decomposed FA for Adreno (llama/32046)
23a073219 2026-11-11 CC: metal : prevent out-of-bounds reads in SOLVE_TRI kernel (llama/32103)
bfa2b60be 2026-11-11 Ruben Ortlam: vulkan: support batched tensor copy API (llama/31418)
d34fb5bad 2026-11-11 Tarek Dakhran: backend : re-instantiate CUDA graphs when the cluster dims of a kernel change (llama/31284)
6403b17ec 2026-11-11 fox5611: ROCm/HIP: fixed BLAS workspace instead of rocBLAS allocating one per call (llama/31838)
6ee57440a 2026-11-11 Pascal: cpu: accumulate flash attention V in F32 (llama/29810)
506d1e4a1 2026-11-11 Leon: webgpu: add PAD_REFLECT_1D support (llama/31877)
b1c11aa7f 2026-11-11 Jeff Bolz: vulkan: allow dequantized KV optimization with CM2 (llama/31526)
033c02b62 2026-11-11 figkcoci-debug: vulkan: allocate the device fault vendor binary buffer (llama/32008)
6afbdfb7a 2026-11-11 Aman Gupta: cuda : use MMVF for BF16 matrices of few rows at small batch sizes (llama/31959)
229de6945 2026-11-11 Jiří Svítil: cuda : add sm70 FlashAttention config case for DKQ=256, DV=256, ncols=64 (llama/27997)
efef05f66 2026-11-11 Sihan Yu: cuda : fattn mma head sizes 40 72 (llama/30285)
cdc15a9fd 2026-11-11 Oliver Simons: CUDA: Add OCP FP8 support (llama/28413)
63dc4822e 2026-11-11 Michael Taylor: sycl : fixed sycl CLAMP to actually support strided view (llama/31784)
dea2bc60c 2026-11-10 Daniel Bevenius: cuda : remove unused ids and type_src0 parameters (llama/32018)
6bd547bd0 2026-11-10 Georgi Gerganov: ggml : add MUL_MAT src1 precision tests and gating (llama/31896)
97010bc71 2026-11-10 Daniel Bevenius: cuda : remove unused quantize_cuda_t typedef (llama/31884)
738487fed 2026-11-10 Michael Paulauski: cuda : halve VMM pool reservation size and retry on cuMemAddressReserve failure (llama/30542)
bbea4a4ed 2026-11-10 Aman Gupta: CUDA: skip graph compat check when graph is being reused (llama/32004)
81afa8413 2026-11-10 Adrien Gallouët: ggml : fix FreeBSD Vulkan build by setting _XOPEN_SOURCE=700 (llama/31701)
e4411c5eb 2026-11-10 Aman Gupta: CUDA: move graph and concurrent stream state out of common.cuh (llama/32001)
93af40106 2026-11-10 Raul Torres: cann: fail early when checking if buffer type is supported (llama/31270)
461b02389 2026-11-10 cwriter: sycl: Add device-side MoE scheduler (llama/30156)
021f35535 2026-11-10 Ruben Ortlam: vulkan: add tiled-transpose concat shader for Qwen models (llama/30591)
0c34066b3 2026-11-10 figkcoci-debug: ggml-rpc : fail gracefully on unreachable endpoints and failed handshakes (llama/30415)
187dc2dcf 2026-11-09 Masato Nakasaka: vulkan: Divide GROUP_NORM workgroup to 2D to avoid maxComputeWorkGroupCount limit (llama/31930)
fb6db43a0 2026-11-10 Ed Addario: vulkan: Fix out of bounds reads/writes on MoltenVK (llama/31890)
013a0d05b 2026-11-09 Hongqiang Wang: vulkan: cap scalar flash attention at 8 rows for large heads on Qualcomm (llama/30829)
c5c221c50 2026-11-10 Gotya-OFFCIAL: sycl: un-gate oneDNN fused SDPA for Alchemist at head_dim=64 (llama/31574)
c0819cd08 2026-11-10 Dmitrii Panchev: hexagon: fix 64-bit FastRPC handle truncation on close (llama/30952)
dab5cff5a 2026-11-09 Aaron Teo: ggml-zdnn: accept non-zdnn tensors, invalidate compute tensors after every op (llama/31824)
b3d3eb88b 2026-11-09 losewayy: ggml : implement the backward pass for TRI (llama/30712)
07215d379 2026-11-09 ArshM17-NV: ggml-backend: don't upload inputs that are not read (llama/31419)
4a0dea60e 2026-11-09 CC: metal : prevent out-of-bounds writes to the Metal FA output buffer (llama/31662)
60b55cd28 2026-11-09 losewayy: metal : make ggml_tri select instead of scaling by the comparison (llama/30711)
6aefcadb9 2026-11-09 Sigbjørn Skjæret: opencl : include climits (llama/31935)
3bc7be4ec 2026-11-09 Aman Gupta: RPC: Improve loading times (llama/29413)
f02d30fc5 2026-11-09 Takamichi Ohara: ggml : support YaRN truncation config on openvino, sycl, vulkan, webgpu, rpc (llama/30802)
e5587e38b 2026-11-09 Titaniumtown: sycl: cache device-id (llama/31126)
456f72ec6 2026-11-09 lhez: opencl: add f32 MUL_MAT_ID (llama/31783)
e55c41d47 2026-11-09 Aaron Teo: ggml-zdnn: fix release binary not detecting backend lib (llama/31905)
25034861c 2026-11-08 Kong Jiale: cpu: enable SpacemiT IME2 MXFP4 dense repack (llama/31776)
48b176863 2026-11-08 Aaron Teo: llamafile: impl bf16 and q8_0 vxe (llama/31866)
c94eeaf4d 2026-11-08 Alexey Kopytko: ggml : update CUDA/Metal radix Top-K to make tied selections deterministic (llama/31084)
48504e33a 2026-11-08 sargentmajord: ggml-cuda : add d_state=64 fast path to SSM_SCAN kernel (llama/31818)
bd6da0dd5 2026-11-08 Leon: webgpu : add COUNT_EQUAL support (llama/31578)
1607f6112 2026-11-08 Georgi Gerganov: ggml : switch to F32 src1 in the CPU backend (llama/31854)
a1722f157 2026-11-08 Pascal: llama, mtmd: follow the reference precision of ggml_prec_set_acc calls (llama/31851)
483def276 2026-11-07 shaofeiqi: opencl: improve q8_0 and MoE small-n verification for spec (llama/31831)
93d5d6ca3 2026-11-08 Aparna M P: hexagon: support for automatic loading of libhtp without legacy env vars (llama/31781)
1512ffb7f 2026-11-08 Jesse Symons: sycl: exact rounding in CPY to Q4_1, Q5_1 and Q8_0 (llama/31465)
cb61ad5a9 2026-11-07 KyleHagy: sycl: refuse device buffers that would exceed VRAM (llama/31285)
7fe515f36 2026-11-07 Max Krasnyansky: hexagon: n_hvx and n_threads cleanup (llama/31857)
dd8508bd2 2026-11-08 Aman Gupta: llama_moe_cache: run missed experts on CPU, add tuning script (llama/30966)
5c6b1224d 2026-11-07 Michael Taylor: sycl: add f16 support for SWIGLU_OAI (llama/30857)
acfd7ab53 2026-11-07 Georgi Gerganov: metal : fix GROUP_NORM for ne03 > 1 and non-contiguous inputs (llama/31852)
79ea91d45 2026-11-07 Nikhil Jain: webgpu : Implement group norm kernel (llama/31490)
bdfde0505 2026-11-07 Jeff Bolz: vulkan: Add 'readonly' to decodeBuf declarations. (llama/31833)
8db671be7 2026-11-07 Ali F. Al-Ramadan: CUDA: fix shared memory bank conflicts in the lightning indexer (llama/31803)
07753bd00 2026-11-06 shaofeiqi: opencl: add arange (llama/31829)
8f4b3709c 2026-11-07 Yonghye Kwon: meta : raise the compute view limit for buffers with few tensors (llama/31447)
a9822e1e3 2026-11-06 Ehsan Bateni: hexagon: fuse post-norm residual add into RMS_NORM_MUL (llama/31822)
75471fb35 2026-11-06 Mark Todorovich: hexagon: conv_2d optimizations and support for conv_3d (llama/31814)
97a65f1fe 2026-11-06 lhez: opencl: support repeat for f16, i32, i16, bf16 (llama/31782)
b5bf5c178 2026-11-06 Masashi Yoshimura: webgpu: add batched tensor API (`get_tensor_n` and `set_tensor_n`) (llama/31473)
3290af876 2026-11-06 Ruben Ortlam: vulkan: detect ReBAR support, avoid BAR allocations if unavailable (llama/31658)
88bb01a0f 2026-11-06 Johannes Gäßler: CUDA: fix Maxwell build (llama/31787)
dc6aa9ac5 2026-11-05 Shawn Gu: opencl: add q6_k multi column tiled GEMV for speculative verification and refactoring (llama/31758)
9836a648d 2026-11-05 Max Krasnyansky: hexagon: Implement set_tensor_n and improve repacking/tiling robustness (llama/31744)
cbfe74e5c 2026-11-05 Zheyuan Chen: ggml-cuda: sanitize post-bias NaNs in MoE selection (llama/31005)
ab8dae27f 2026-11-05 Jeff Bolz: vulkan: Implement test-fusion interface (llama/30769)
7e416646f 2026-11-05 ManuelPDM: CUDA: use highest compiled arch in get_mmvq_mmid_max_batch (llama/31679)
a229176ba 2026-11-05 Alex-JP-93: vulkan: RDNA3/4 Large-Tile Split-K Optimization (llama/30280)
6d1cf7346 2026-11-05 Georgi Gerganov: metal : fuse DeepSeek-V4/V4.1 and GLM MoE routing (llama/31615)
6aa3d68bc 2026-11-05 Jaden_Mach: CUDA/HIP: matrix-core (MFMA) lightning indexer for CDNA2 (gfx90a) (llama/29050)
804151714 2026-11-05 Johannes Gäßler: CUDA: linearize MoE data layout for MMQ/MMF (llama/31047)
c14170c7b 2026-11-05 bri-prism: vulkan: FWHT kernels for block widths above 512 (llama/29772)
ce6a1e98e 2026-11-05 Nisbenz: vulkan : check combined K+V f16 scratch size in FA dequant path (llama/30487)
2f8569e0e 2026-11-12 Takamichi Ohara: ggml : support `truncate=false` for YaRN (llama/30206)
3901838e5 2026-11-05 Hoang Vien Duy: metal : use mul_mm for 32 <= K < 64 (llama/30982)
466798410 2026-11-05 Leon: webgpu : add MEAN support (llama/31591)
1db126cb1 2026-11-05 Alex-JP-93: vulkan: Re-enable large coopmat matmul configuration on AMD proprietary driver 26.10.1+ (llama/31587)
08352b486 2026-11-05 Pascal: metal: keep fusable node groups inside one command buffer (llama/31688)
f78c146de 2026-11-04 shaofeiqi: opencl: enable f32 and q5_k multi column GEMV by default for Adreno X2 (llama/31694)
06734424f 2026-11-04 shaofeiqi: opencl: support non-contig sigmoid (llama/31687)
32a34a38b 2026-11-04 shaofeiqi: opencl: add DSV4_HC_PRE and DSV4_HC_POST (llama/31623)
441cafe9d 2026-11-05 anujj: Title: CUDA: fuse NVFP4 gate/up matmuls and GLU in MMQ (llama/31296)
73aface4c 2026-11-04 shaofeiqi: opencl: improve decode perf with FA (llama/31633)
eb27d8f39 2026-11-04 Masashi Yoshimura: webgpu: return maxBufferSize from get_max_size and avoid whole-buffer bindings in memset/clear (llama/31348)
aba02defd 2026-11-16 Anton Melnikov: examples : bump llama.cpp version (#4173)
```

### stable-diffusion.cpp — 10 commits

```
532d2c15 2026-11-15 leejet: refactor(api): adopt opaque options, tensors, and results (#2365)
01c463a2 2026-11-15 Adam Clark: docs: Add TensorStack C# binding (#2359)
5dcfa798 2026-11-14 leejet: sync: update ggml to 1.0.0 (#2354)
394d2104 2026-11-14 losewayy: fix: trim MiniMax-H3 audio to video duration (#2350)
6201bcc7 2026-11-14 leejet: docs: standardize model guides and server documentation
f7120ceb 2026-11-14 l0caldadmin: docs: add build directory creation to SYCL build instructions (#2352)
ca4e755d 2026-11-14 leejet: docs: reorganize documentation and improve README navigation
85a0b90c 2026-11-14 leejet: docs: document Ninja builds and ccache setup
b521db48 2026-11-14 leejet: perf(hip): fuse INT8 SwiGLU quantization and enable gated residual fusion (#2353)
4b51674b 2026-11-14 leejet: perf(hip): accelerate flash attention and INT8 projections (#2351)
```

### llama-cpp-python — 3 commits

```
0542f207 2026-11-15 Andrei: fix(ci): remove unsupported macOS 14 release runners (#2416)
46816d22 2026-11-15 Andrei: chore: bump version to 0.3.37 (#2415)
dd70c923 2026-11-14 Andrei: feat: update llama.cpp to a956a852c (#2414)
```

### acestep.cpp — 4 commits

```
973517b 2026-11-17 Pascal: vae: run the conv1d as an implicit GEMM
7b75ee6 2026-11-17 Pascal: ggml: fork update for the Metal CONV_2D implicit GEMM
603e682 2026-11-14 Pascal: chore: update webui build output
603e6ed 2026-11-13 Pascal: build: format only, drop the duplicate check
```

### qwen3-tts.cpp — 0 commits

```
```

### parakeet.cpp — 0 commits

```
```

### sdcpp-webui — 0 commits

```
```

### libwebm — 0 commits

```
```


## Window: 2026-11-18 → 2026-11-19 (`12522.r0.g2cbfc3c` → `12550.r2.g9a080f44b`)

### llama.cpp — 30 commits

```
9a080f44b5 2026-11-19 Ravi Panchumarthy: ggml-openvino: fix OpenVINO CI, minor fixes and optimizations (#32590)
c7468107ef 2026-11-19 Bhargav Krish: cuda: Scatter kernel for set_n (#32489)
ac830a9cbb 2026-11-19 Andreas Kieslinger: ggml : add backend scheduler tests (#27258)
8af68d486a 2026-11-19 Piotr Wilkin (ilintar): llama: fixes for Inkling 2 attention mask (#32429)
f8caa5ea30 2026-11-19 Alexey Kopytko: metal : fix the second argument of NSMakeRange (#32602)
4db8b7638f 2026-11-19 SS1618: webgpu: add POOL_2D support (#32250)
01592dc58b 2026-11-19 Georgi Gerganov: llama : remove redundant fields from llm_graph_params (#32596)
8bf2132c3f 2026-11-19 Georgi Gerganov: readme : fix release badge (#32597)
5812201a81 2026-11-19 Adrien Gallouët: ci : fix build-opencl.yml (#32594)
41d8297fe4 2026-11-19 Pascal: metal : CONV_2D tensor API for M5, split-K for all chips (#32542)
51a77c4f24 2026-11-19 saiph: qwen3vl : set t_layer_inp for EAGLE-3 (#32589)
76f186df71 2026-11-19 Bartowski: ggml : IQ2 creation speedup through caching (#31910)
95b09b62be 2026-11-19 Adrien Gallouët: llama : remove PATH_MAX (#32557)
b5dbca1e44 2026-11-19 Adrien Gallouët: ci : use LLVM 22 (#32565)
80437488a4 2026-11-19 Aleksander Grygier: ui: cut Llama Chat's first-load JavaScript by 63%, load diagrams, math and PDFs on demand (#32555)
39039aa27f 2026-11-19 Adrien Gallouët: llama : fall back to buffered I/O on EIO (#32545)
7a4117eef9 2026-11-19 Birk Skyum: vulkan : enable MMQ with mixed signedness integer dots (#31045)
573aa89de6 2026-11-19 Jeff Bolz: vulkan: Implement stream-k MUL_MAT (#28528)
ecafc67145 2026-11-18 Daniil Sterkhov: vulkan: use floating-point zero for storage-only FP16 in DIAG/TRI (#32379)
d4f5c26049 2026-11-19 Aman Gupta: CUDA: use 64-bit dst offsets in mul_mat_q (#32374)
08c252e221 2026-11-18 lhez: opencl: allow adjusting KV padding in decomposed FA (#32522)
e4b620af19 2026-11-19 Xuan-Son Nguyen: mtmd: support voxcpm2 (#32443)
b001d7bb22 2026-11-19 En Yao: ggml : WASM Relaxed SIMD Enhancement (#19590)
0a76757469 2026-11-19 mahounairo: llama : fix sticky NaN in recurrent state (#31913)
b044890408 2026-11-18 Xuan-Son Nguyen: server: fix sleep state for v1/realtime (#32567)
78e05298f0 2026-11-19 parthod0x: model : limite: reject mudd configs that index past mudd_tap_idx on load (#32562)
785f6bac00 2026-11-18 Chenyang Li: ui : keep streaming reasoning box inside the viewport when zoomed (#31966)
edec462cc0 2026-11-18 Adrien Gallouët: ggml, ci : use llvm 22.1.8 (#32548)
4483b2b987 2026-11-18 Alessandro de Oliveira Faria (A.K.A.CABELO): vendor : update cpp-httplib-0.67.0 [no ci] (#32563)
bafa0420c1 2026-11-18 Tarek Dakhran: server : enable packing for d1-2B and d1-Omni-2B models (#32553)
```

### Strata — 609 commits (includes tag v0.2.16; Control/Terminal 0.2.16, engines 0.1.61-0.1.62)

```
58ee32277 2026-11-18 Niko1221: Supporters: round pictures, one row per level with the biggest supporters first and largest, no amounts shown (README, SUPPORTERS.md and the 7 translations)
26ae4fa2d 2026-11-18 Niko1221: Supporters: the 15 public GitHub sponsors, grouped by tier (highest first), in README, SUPPORTERS.md and the 7 translated READMEs; adds codeconduit-official, kingdonb, jaceknoga, Daisame, moruku36 and hrkgk
650ef4a91 2026-11-18 Niko1221: README and its 7 translations: the dark-mode logo points to app/host/public/brand (it still named the old apps/ folder, so GitHub's dark theme showed no logo)
19f18e103 2026-11-18 Niko1221: Docker: the image build context carries engine/third_party/strata-gguf-py (the Terminal bundle's model preparation tools; the first v0.2.16 image build stopped without it)
64524fb9f 2026-11-18 Niko1221: App: the failed-drafter line with the draft layer standing in says what the Terminal says
90225fa09 2026-11-18 Niko1221: App: the offline draft-layer note is the Terminal's new sentence
b09ffc67b 2026-11-18 Niko1221: setup: a DFlash2 drafter that is already there prints no "0.00 of 0.00 GB"
3899cfe7f 2026-11-18 Niko1221: last-run message: sentence break
cc0242cc8 2026-11-18 Niko1221: oomd room tests: run on Windows too (the drop is injected)
fe502d8c6 2026-11-18 Niko1221: strata launch: the Access step only looks at this computer; the offline check names no host (S6, S12)
43e4f52f6 2026-11-18 Niko1221: serve: probe children get no stdin
aa754707c 2026-11-18 Niko1221: oomd: free the model's file cache before the load, trim while it loads, say what happened last time
99ae410bd 2026-11-18 Niko1221: Tests: the stand-in screens of the Access and Drafting tests know the two new calls (S12, N1)
e9911105f 2026-11-18 Niko1221: Card speed child: no stdin, so it answers in 0.05 s instead of running into its 20 s limit (A9)
ada3cf4f9 2026-11-18 Niko1221: strata launch screens, round 2: disk verdicts, step counter, 80 columns, drafter lines, offline, port (N1, T10b, S1-S6, S9, S11, S12, S13)
9491a54c9 2026-11-18 Niko1221: Terminal: monitor top line and Hardware tab, sub-command help, drafter ready line (S2, S4, S7, S8, S10)
dbe88acdc 2026-11-18 Niko1221: Uninstaller: the four files left in the data folder are the app's own state and stay with it (A10)
1ba3b14d3 2026-11-18 Niko1221: First run: the host reads the PC when it starts, and the checking line says it is still working after 12 s (A9)
1249ab4d0 2026-11-18 Niko1221: Status check: ask first whether anything listens, and look at the ports all at once (A9)
d59184acd 2026-11-18 Niko1221: Setup: plain tune prompt, no 404 text on the normal engine fallback, quiet pull
3c3609212 2026-11-18 Niko1221: Offline DFlash2: the smaller prepared drafter file alone is enough
69289adbe 2026-11-18 Niko1221: Chat page: with no picture reader the paperclip hint and the picture note say so and that text files still work (A8)
30d4d09a5 2026-11-18 Niko1221: Update Strata: the app's own step never turns a finished update into a failure sentence (W-F1)
bf1295276 2026-11-18 Niko1221: Engine arch note: read BUILD.json "archs" as a string too
76512d99f 2026-11-18 Niko1221: Config snapshot world: the Arc picture rule answers for the simulated machine's system
c5cc7351f 2026-11-18 Niko1221: Config snapshot: the Linux machines' engine start carries MALLOC_ARENA_MAX=2 (P11)
d030dc039 2026-11-18 Niko1221: Config snapshot golden: Arc A750 launch starts with pictures off (T14 of FIX-TUI)
f731cd184 2026-11-18 Niko1221: Config snapshot test world: installed_engine_exe takes the backend again
9b673a4e4 2026-11-18 Niko1221: Test follows T14: an Arc with no engine installed yet gets pictures off, one whose engine carries the reader keeps them on
aeff969c6 2026-11-18 Niko1221: FIX-APP A7: the update jobs go on when the only loaded models are in state error
5e0309832 2026-11-18 Niko1221: FIX-APP A6: the same chat open in two windows: every page on a running turn gets its frames
c2b15cd97 2026-11-18 Niko1221: FIX-APP A4: the app host's /v1 serves the one loaded model whatever name the client sends
f7060ec95 2026-11-18 Niko1221: FIX-APP A5: after a Tools change the busy message names the Tools settings, not the models
ab8b5ad73 2026-11-18 Niko1221: FIX-APP A3: the first "Tune & start chatting" says it downloads the drafter, with its size
cc35a7494 2026-11-18 Niko1221: FIX-APP A1: a version card says "Already on this computer" when its files are there
79beaff7e 2026-11-18 Niko1221: FIX-APP A2: the first-run "Your model" step says it is checking while the version list loads
d8da4b984 2026-11-18 Niko1221: strata launch: fixes from the Linux test run (T14, T18, T22) and the tests that followed the new defaults
5ddeebf2b 2026-11-18 Niko1221: Update: a test start that failed because an older Control's runtime host was dead is tried again by the next plain `strata update`
55f7b69cb 2026-11-18 Niko1221: P1: the rename of a stale strata.ps1 also leaves a line in launcher-heal.log beside it, for support (an update's own test start swallows the screen line)
1151d3f8f 2026-11-18 Niko1221: P13/P14 tests: keep two setup tests off the network
0343762da 2026-11-18 Niko1221: P13: --gguf-dir without --family / --model: the files name the model, so setup does not ask "Which model?" and "Which size?"
7c11f994e 2026-11-18 Niko1221: P12: setup's tuning question defaults to No, like the Terminal's first launch
46a645f2b 2026-11-18 Niko1221: P14: setup uses the Terminal's Auto drafter rule instead of always fetching the 5 GB MTP layer
73db60a02 2026-11-18 Niko1221: P10: the installer's graphics-line test expects the clean names
89fec2d1a 2026-11-18 Niko1221: strata launch Save screen: keep the choices on screen in small windows with the new Download row (T2)
1c43e5d97 2026-11-18 Niko1221: Spawn-site inventory: P6's git symbolic-ref call and the pacer's systemctl reads
fff90b841 2026-11-18 Niko1221: strata launch screens: fixes found by the real 80x24 walk on p1004 (T2, T10)
02c4bd423 2026-11-18 Niko1221: P4: keep systemd-oomd from ending a model load on a Linux desktop (a pressure pacer around the engine start)
7f7bbf56d 2026-11-18 Niko1221: P8: setup on a Pascal / Volta card takes the feed's CUDA 12 engine package instead of compiling
c3b6ba8e9 2026-11-18 Niko1221: strata launch screens: first-impression fixes T2-T12, T14-T16, T18, T22
42a8d60da 2026-11-18 Niko1221: Terminal: the monitor's memory tiles, the host-log reason and the start-screen engine line (T1, T13, T19, T21)
2fd4e1d7f 2026-11-18 Niko1221: P6: a clone on a tag or a commit says it is on a fixed release
371834c15 2026-11-18 Niko1221: P5: keep a short UPDATE.bat in the 0.2.16 layout so an old clone's update ends cleanly
aeecf0f5d 2026-11-18 Niko1221: P11: MALLOC_ARENA_MAX=2 for the server and the engine on Linux
5696cb3f6 2026-11-18 Niko1221: P10: install.sh names every graphics card once, with clean names
5dc269cf8 2026-11-18 Niko1221: P2: install.ps1 adds its folder to the user PATH without rewriting the rest of it
630e3a3df 2026-11-18 Niko1221: P1: a typed `strata` in PowerShell is always strata.cmd (no strata.ps1 in the PATH folder)
6f6099fe6 2026-11-18 Niko1221: Windows: no Strata process may reach CPython 3.12's _wmi (the runtime host died with 0xC0000005 when WMI refuses the account)
48aa03ec4 2026-11-17 Niko1221: Metal: a finished batch window beats the serve watchdog (issue #29)
2d0b062a2 2026-11-17 Niko1221: doctor: an installed engine that failed its integrity check shows the integrity sentence, not "no engine for this PC"
017dc208e 2026-11-17 Niko1221: test_doctor_signed_engine.py: `doctor --profile` against a signed engine in a component folder of a clean home
9711739de 2026-11-17 Niko1221: docs: the aarch64 Control and engine are 0.1.62 in docs/data/release.json (strata-control-0.1.62-linux-aarch64.tar.gz, strata-engine-0.1.62-linux-aarch64-cuda-cuda13.tar.gz)
f2919b358 2026-11-17 Niko1221: Connection banner: after two failed Retries it says the background part has stopped and what helps (packaged-app walkthrough A63)
6fc8add9b 2026-11-17 Niko1221: Tasks: a line says why Run now is disabled when no model is loaded on this computer (packaged-app walkthrough A70)
03d037aa6 2026-11-17 Niko1221: Connection banner: it wraps, so the text keeps its width and Retry no longer sits over it (packaged-app walkthrough A62-A65)
b056792b5 2026-11-17 Niko1221: First run: an unreadable download list has its own words and one next step; the offline and error cards can go on without an engine (packaged-app walkthrough A10, fix 2)
872e23c55 2026-11-17 Niko1221: First run: Control's own offline words are recognised, so an offline person gets the offline card (packaged-app walkthrough A10, fix 1)
829a0cba3 2026-11-17 Niko1221: Sidebar: the model chip names the model picked from an API connection (packaged-app walkthrough A15 / A16)
f9a4df21e 2026-11-17 Niko1221: docs: the Mac packaging scripts' comments and README name the moved places (tools/packaging/feed_tool.py, tools/packaging/UPDATES.md, app/desktop/scripts/make-dmg.sh, the package's metal/ folder)
55276c09d 2026-11-17 Niko1221: Test: the French word for a code block's label is the same as the English one
6d8a84590 2026-11-17 Niko1221: Tasks: at a narrow width the header controls take a row under the title instead of running off the right edge (GUI-VIS-1117 finding 7b)
5addb33c0 2026-11-17 Niko1221: terminal/serve/test_stop_open_string.py: a tool call left open at a normal stop is never repaired into a call (soak 11-17, s005 turn 36)
bb1a9e787 2026-11-17 Niko1221: Agent: a folder blocked in Settings -> Tools is enforced from the next message, not only after the host restarts (SAFETY, 0.2.16 visual walkthrough finding 1; #5737)
bf6d911f1 2026-11-17 Niko1221: test_drafting: the last block of test_the_server_applies_it_at_every_start no longer depends on the box's GPU
f994d618c 2026-11-17 Niko1221: Languages: the engine settings texts and the Monitor's "Last:" line are translated (GUI-VIS-1117 finding 10)
b60358f27 2026-11-17 Niko1221: Chat: with no model loaded, a line under the box says why Send is grey and what to do (GUI-VIS-1117 finding 6)
6e4104fdd 2026-11-17 Niko1221: Monitor: the VRAM total is the larger of the host probe and the engine's own, and never sits below the reading (GUI-VIS-1117 finding 8)
78c188e93 2026-11-17 Niko1221: Tasks: "Run now" on the list row is enabled when a model is ready, like the one inside the task (GUI-VIS-1117 finding 7a)
0aac6edf2 2026-11-17 Niko1221: Serving: the "Tools for apps on this computer" switch is also drawn when one model is loaded (GUI-VIS-1117 finding 9b)
a26b822ca 2026-11-17 Niko1221: Language switch: a live switch redraws the chat messages, and the tool-summary lines and the code label are said in the chosen language (GUI-VIS-1117 finding 2)
252fc0c09 2026-11-17 Niko1221: First run: the Prepare page says what is already on this computer, the file check has its own title, the tuning card has no gap, 30d / 7d are translated (GUI-VIS-1117)
b3b58b4e4 2026-11-17 Niko1221: Tests: the model-deletion tests and the Terminal's pytest session never read the real Strata settings file
1d295787b 2026-11-17 Niko1221: engine: WIN32_LEAN_AND_MEAN before every <windows.h> include that does not define it (a Windows CUDA build blocker: `small` is `#define small char` from rpcndr.h)
5064fab2b 2026-11-17 Niko1221: serve/server.py: restore the changes of 18526b879 that the first fix commit dropped; the only difference from 18526b879 is the moved re-export block
b3b766983 2026-11-17 Niko1221: docs/GYRO.md: STRATA_NO_TQ_KERNELS=1 changes nothing in a default build
4b647b0bf 2026-11-17 Niko1221: docs: the engine build does not fetch or use llama.cpp; the sentences that said so are gone
cebd4489a 2026-11-17 Niko1221: tools/layout/checks/docs_paths.py: a file name in a sentence is not a hit, and an explained list for lines that are correct as written
ba971b3ab 2026-11-17 Niko1221: docs: every command and path in the user-facing pages names the moved place (terminal/tools, terminal/serve, tools/packaging, app/, engine/sycl, docs/bench-results ...)
26cfd1e0f 2026-11-17 Niko1221: tools/layout/checks/docs_paths.py: a scan of the user-facing pages for commands and paths that name a place the move took away
6e7264c88 2026-11-17 Niko1221: tests/terminal/test_scripts_run_by_path.py: the programs a checkout starts by path get past their imports from a foreign folder
4d718835c 2026-11-17 Niko1221: engine/metal/setup_mac.py, engine/sycl/setup_intel.py, engine/sycl/serve/server_intel.py: terminal/ is on sys.path again
18a50687f 2026-11-17 Niko1221: The Linux Intel Arc package bundles libz.so.1 with its notice: build_sycl_linux.sh, notices/libz.txt, and a test that every bundled system library has its notice
2c7513613 2026-11-17 Niko1221: tools/layout/split: the re-export block goes after the last statement before the first function, and the run ends with a script-mode smoke
2a20dbce6 2026-11-17 Niko1221: serve/test_server_script_mode.py: serve/server.py is started as a script, from a foreign folder, against a mock engine
e22685cbb 2026-11-17 Niko1221: serve/server.py: the re-export block of the split comes after the file's sys.path lines, so `python serve/server.py` works again
43822f4a8 2026-11-17 Niko1221: docs: the build commands configure engine/ (and engine/sycl), and build.sh's hint names engine/sycl/tools
194d068e0 2026-11-17 Niko1221: tools/layout/checks/path_scan2.py: variables joined with unquoted segments, for-loop variables, cmake -S folders, and paths that existed before the move
d68481912 2026-11-17 Niko1221: test_build_windows_bats.py: the Windows build scripts name only paths that exist, checked on every OS
119f1a4d0 2026-11-17 Niko1221: trellis/build.sh: the include folders and sources are named from the repository root as before the move
2d57d0dd8 2026-11-17 Niko1221: engine_flow.sh and update_model_flow.sh: the packaging scripts are run from the repository root
926bd1cf9 2026-11-17 Niko1221: Dockerfile.src: the engine is configured from engine/ and the Terminal is packaged with tools/packaging/package_terminal.py
42dce6453 2026-11-17 Niko1221: engine/sycl/tools/build.sh: the SYCL developer build configures engine/sycl
9e2dd798f 2026-11-17 Niko1221: build_split_cuda.sh and build_split_hip.sh: cmake configures engine/
8dedfb537 2026-11-17 Niko1221: build_windows.bat (HIP, Windows): the repository root is three levels up, the engine is configured from engine\, the readers and the zip script are in terminal\tools
3d83b4328 2026-11-17 Niko1221: Engines 0.1.62 (the same number as Control)
c341b007f 2026-11-17 Niko1221: Revert "release manifest: Control may be ahead of this release's own engines when the manifest says so (control_ahead)"
1678aff46 2026-11-17 Niko1221: docs: SUPPORTERS.md at the top level, next to README.md; a line to it under the avatars of README.md and the seven translated READMEs
0c99fcf85 2026-11-17 Niko1221: serve: a call max_tokens cut short is replayed with the parameters it has, not as a parameter called "arguments" (soak 11-17)
07f6f3218 2026-11-17 Niko1221: Version 0.2.16 / Control 0.1.62 / engines 0.1.61: app and Terminal 0.2.16, Control 0.1.62, engine packages 0.1.61
4af90108d 2026-11-17 Niko1221: release manifest: Control may be ahead of this release's own engines when the manifest says so ("control_ahead")
44d4a006a 2026-11-17 Niko1221: test_control_install: the ".." escape test climbs to a real setup.py again, and asserts it is there
6a3ddb731 2026-11-17 Niko1221: docs/media/make_figures.py: the app's icon sprite and font are read from terminal/serve/web
f25db3e05 2026-11-17 Niko1221: make-dmg.sh: the minimum-macOS check runs tools/packaging/binary_deps.py
ad1fb73b5 2026-11-17 Niko1221: build_cuda_windows.py: the engine is configured from engine/ and the packaging scripts are run from tools/packaging/
3176dfd1a 2026-11-17 Niko1221: tools/layout/checks: a second path scan for paths built from __file__, a root variable or the script's own folder
f1b70b2a9 2026-11-17 Niko1221: terminal/serve/test_commit_limit.py: the engine header is read from engine/include after the layout move (release-check fix 2, #1607)
f71bc1cb1 2026-11-17 Niko1221: Host: a taskkill of the Harness has a time limit, and every call to Control writes its start and end with the time it took (SOAK-APP 13:20 pending Unload)
cde489b96 2026-11-17 Niko1221: Models: the model card tells the person when the engine says Windows' memory limit is close and Strata may stop without a message (#1607)
8a66e8f78 2026-11-17 Niko1221: Agent: a turn that never becomes ours ends with a plain message, and a restart of the Harness waits for a chat that is starting on it (SOAK-APP 12:39 stuck turns)
7d77f51ca 2026-11-17 Niko1221: serve/server.py: 230 definitions move unchanged into serve/server_parts/ (file split, 2,498 of 11,310 lines)
4058aa782 2026-11-17 Niko1221: Layout move for 0.2.16: the top level becomes app/, engine/, terminal/, docs/, tools/ and .github/
e60613ac7 2026-11-17 Niko1221: tools/layout: the 0.2.16 layout move script, its checks and the file-split script (added before the move, no change to the product)
483778931 2026-11-17 Niko1221: tool calls: a reply cut inside an announced call carries strata_unread_tool_markup {"reason": "cut_off"} (soak l620b2)
037be4947 2026-11-17 Niko1221: Chats: a damaged or older chat file with a missing date, title or message text no longer takes the whole chat page down
5b068304c 2026-11-17 Niko1221: tool calls: a string value over 4 KB keeps its closer and the parameters after it (the scan compaction rebases the value start) (#4686)
09db599e9 2026-11-17 Niko1221: Tests: timeskip-real retries the removal of its scratch folder and never fails on the cleanup alone
c4ac57a55 2026-11-17 Niko1221: Tests: the "cannot fit even after the summary" case is sent clearly past the window's edge, so environment paths cannot flip it
cf08d5c44 2026-11-17 Niko1221: status: `strata status` runs on the standard library alone again (no rich, no textual)
17fca7056 2026-11-17 Niko1221: Tests: the host test runner passes its files relative to the host folder, so a checkout with a long path no longer fails with ENAMETOOLONG
0d23ecda3 2026-11-17 Niko1221: tune: `strata tune auto --concurrency N` judges every setting on N requests decoding at once (opt-in); a load-tuned preset is applied only to starts that run requests together (#4821)
14a702526 2026-11-17 Alex Yong: Monitor: a Mac's GPU temperature and power without root, opt-in with STRATA_MACOS_SENSORS=1 (PR #5793, #5016)
f232ad9ae 2026-11-17 Niko1221: Helpers: a Helper time limit in Settings, and a plain note on a helper that has worked over 30 minutes (#5996)
c41975671 2026-11-17 Niko1221: Docs: how to open the developer tools in the app window (#5408)
9160728c3 2026-11-17 Niko1221: Desktop: the browser developer tools are built into the Windows and Linux app and stay off unless asked for (#5408)
f1dd410a2 2026-11-17 Niko1221: Settings: a Reply width choice for the text of an answer (#5066)
79c837181 2026-11-17 Niko1221: Helpers: "View log" shows what a helper did, for every helper that did something (#5254)
0e7d5ca9c 2026-11-17 Niko1221: tune: an account of every tune is saved and `strata tune report` shows it; progress says "run N of M" (#5232, report and progress)
efdde5c31 2026-11-17 Niko1221: presets effective: say where each non-automatic setting comes from (#5351, first step)
8f5054a13 2026-11-17 Niko1221: tune, serve: a full graphics card is said as such, the failed engine's log is kept, the next engine waits for the memory to come back (#5078)
11b22a0ff 2026-11-17 Niko1221: Chat: the context popover says how much room is left before older messages are summarized (#5091)
773f2e248 2026-11-17 Niko1221: Sidebar: a New chat button on each workspace row starts a chat in that workspace (#4913)
73fb2a10c 2026-11-17 Niko1221: launch: the Delete key on the preset list asks the same question as "d" (#5819)
26e6a1783 2026-11-17 Niko1221: Hebrew: the catalog loads guic-he.json, so the 0.2.16 new-UI strings show in Hebrew
6cfa02c48 2026-11-17 Niko1221: Chat: a picture pasted or dropped while the chat is busy is not thrown away in silence (#5960)
64bbd0df0 2026-11-17 Niko1221: tests: serve/test_monitor.py waits for a request's final state instead of reading it right after the reply
f6b06df07 2026-11-17 zapabob: Tests: the overflow-recovery case checks that the retry answers the original message and that a summary ran (PR #5777)
71483db50 2026-11-17 Niko1221: UI: selected text can be seen (#5073)
b03943b21 2026-11-17 Niko1221: Models: "Use a local GGUF" keeps picture reading on when a reader is already on this computer (#4926)
7fa7deda7 2026-11-17 Niko1221: Tests: a message parked in one chat goes out once, from that chat, whatever the person does between two chats (#5806)
814d1507f 2026-11-17 Niko1221: docs: SETTINGS.md regenerated from the register (STRATA_I8_SM70 and STRATA_PF_FUSED_SM75_KQ join the rollback table; 83 -> 85 rows)
53313f795 2026-11-17 Niko1221: register: STRATA_STOP_LAYERS and STRATA_STOP_STAGES are research (#6011)
63a20e813 2026-11-17 Niko1221: register: the eight new opt-in notes carry the two-card numbers, or say "not measured here" (#5860, #5864)
1576f28e3 2026-11-17 Niko1221: drafting line: --batch-mtp on a layer split whose slots are pipelined says "none in parallel slots", as the engine runs them
d595c139f 2026-11-17 Niko1221: Chat: the collapsed "A tool call that could not run" line shows a chevron, so it reads as something that opens (follow-up to a24501c01)
f3abf9b11 2026-11-17 Niko1221: tests: setup.main() --update no longer pulls or moves files inside the test_setup_update test (a failure in any git checkout)
4619efa43 2026-11-17 Niko1221: Chat: "Number quotes", a switch that numbers several quoted passages and names who wrote each (#5993)
925906f63 2026-11-17 Niko1221: German and Portuguese: the tool-call strings use the catalog's own words (guic23, guic24)
2b6417bef 2026-11-17 Niko1221: docs: --conversation-cache-rewind-keep row (#5862); a comment in the park path says why a slot holding the conversation does not skip the park
2b1cbc7df 2026-11-17 Niko1221: Setup: "Only connect to Strata on another computer" on the first-run engine card, so setup needs no local engine (#5529)
b7d0eedfc 2026-11-17 Niko1221: Monitor: the Context fill gauge shows what fills the window, in parts (PR #4636 by thisisspartan)
b98760e5d 2026-11-17 Niko1221: Serve: the metrics carry what the context gauge needs, the reused prefix and the engine's generation (PR #4636 by thisisspartan)
a24501c01 2026-11-17 Niko1221: Chat: a tool call the model wrote as text that nothing ran is one collapsed line, not raw markup in the answer (#TOOLCALL-B follow-up)
7195c7ab8 2026-11-17 Niko1221: Test: the Monitor's GPU load label test follows the label span #4968 gave an id
5190dd665 2026-11-17 Niko1221: Monitor: #4968 revised, min and max over the newest 500 requests, time-weighted averages, plain tooltips
4fe921325 2026-11-17 奥克队长: Monitor: a model card, the Speed card's min and max, and power and temperature averages (PR #4968)
18af37321 2026-11-17 Niko1221: Agent: a reply whose tool call could not run gives the model a tool error and the turn goes on, two times at most (#TOOLCALL-B, #6032)
8639854b8 2026-11-17 bitaccesscomau: batch slots on two cards: slot runs, lookup drafts, resident copies, a turn read in its slot - each opt-in (#5864)
3635f6d8c 2026-11-17 bitaccesscomau: Test the half rule of the rewind keep (#5862)
ed76fe5b0 2026-11-12 bitaccesscomau: --conversation-cache-rewind-keep on a layer split
fe686835d 2026-11-12 bitaccesscomau: --conversation-cache-rewind-keep: skip the park when a rewind keeps the conversation live
b6d168658 2026-11-17 Niko1221: Chat: the status line says what the model does now, and nothing rotates any more (owner, 0.2.16)
4996806bb 2026-11-17 Niko1221: Hebrew: the screen title "Serving" and eleven icon names were still English
bb9a7db1b 2026-11-17 Niko1221: French: a no-break space before ; : ? ! and inside « » in every French catalog
35eab91fb 2026-11-17 Niko1221: Tests: the "refused once" recovery test leaves room for the retry, and a message that cannot fit even after the summary has its own test
0bf27a4be 2026-11-17 Niko1221: serve: a reply's token limit is a whole number on Chat and Messages, as on Responses (#4037)
99dd9f8bf 2026-11-17 Niko1221: Reapply #4141 port (macintog): the M5 difference was the m1002 gate running released kernels; with matching kernels BASE-05 is 10 / 10 (m1002-20261117-0244-e992 and your d13)
2c6e2c244 2026-11-17 Niko1221: HIP Linux: a package built against a kpack ROCm carries rocBLAS's device code and points the loader at it (#5060)
117c267e1 2026-11-17 Niko1221: Agent: /compact no longer leaves the chat "still working" (follow-up to #6070)
fbbe11f0f 2026-11-17 Niko1221: Revert #4141 port: M5 BASE-05 differs on 7 / 10, first tokens are special-token ids; back when fixed
e03d090ef 2026-11-17 Niko1221: tests/cuda/prefill_decode_golden.cu: include ggml.h for the oracle's ggml_type / ggml_get_type_traits
01a1eb935 2026-11-17 Niko1221: cmake: one adapt_async_default_test target (CMakeLists.txt:361 duplicated cmake/backends/cpu.cmake:48, d312a945b / #5814)
c78548016 2026-11-17 Niko1221: Hebrew: the 18 strings of the move-a-chat, Your rules and route-tail-skip settings (#6060, #6051, #5084)
cb275901b 2026-11-17 Niko1221: serve: a request that ends early stops only the engine it ran on, never the engine that replaced it (#5573)
b11cd8d38 2026-11-17 macintog: metal: the prompt GEMM grid follows the layer's tile, so a K-quant layer covers its whole ffn width (#4141)
9bcc20a2f 2026-11-17 Niko1221: tests/split: the 8192-row pick table is read from pf_pick.hpp (kPfPicks[]), where #5496 / #5667 moved it from engine.cu
f59ac8eaf 2026-11-17 Niko1221: Hebrew: the skipped-files line drops the glued English plural {1} (#6060)
598e70d11 2026-11-17 Niko1221: tests: the language picker lists ten languages with Hebrew (#6060)
c5bdd43b2 2026-11-17 Niko1221: tests: gr_parity checks the STRATA_HC_Q8 read with q8_inject (#3225)
737729c1c 2026-11-17 Niko1221: HIP: the persistent hc read declines int8 rows (STRATA_HC_REQ8 with STRATA_HC_PERSIST) (#5560)
8ee96a8d4 2026-11-17 Niko1221: tests: the Hebrew page is right to left and its send arrow is mirrored (#6060)
ad5074630 2026-11-17 Niko1221: Hebrew: the send arrow points the way the text runs
bf1d53001 2026-11-16 DeDuplicate: App and web page: Hebrew, right to left (PR #6060)
98ebfb3e1 2026-11-16 Niko1221: Expert settings: the route tail skip is a choice (Automatic / Off / 1-9), in the app and the Terminal (owner, 0.2.16)
fe5917a28 2026-11-16 Niko1221: setup, telemetry: two Mac fixes found by the Mac test run (M1, M2)
a76f2f136 2026-11-16 Niko1221: tests: Mac runs skip what is Linux / Windows only, with the reason (#4138 Mac follow-up)
88a882f87 2026-11-16 Niko1221: tests: the mixed-PC and engine-library cases follow the host or name their PC (#4138 Mac follow-up)
f41cd82be 2026-11-16 Niko1221: tests: the shape-engine cases speak about a Linux NVIDIA PC on a Mac (#4138 Mac follow-up)
4cf9bee16 2026-11-16 Niko1221: tests: the update-with-a-model cases follow the host engine family (#4138 Mac follow-up)
7c743ad7f 2026-11-16 Niko1221: tool calls: `<parameter name="K">` inside a `<function=NAME>` call is parameter K (#5969's third form, recovery on)
70212f629 2026-11-16 Niko1221: serve: the Intel reader counts a client open in several descriptors once on Windows too
9bb5d16b1 2026-11-16 bitaccesscomau: pipelined decode on two cards: a counted gate, a lazy draft chain, lookup runs - each opt-in (#5860)
a2ab3965e 2026-11-16 Niko1221: HIP: the head-alias spacer's free and drop_window_graphs' graph destroy discard their result explicitly (#5188 follow-up)
c5191669b 2026-11-16 Niko1221: Tests: the spawn-site list counts setup.py's update pull (fix-up of 165374a42, Q6)
54ce499ed 2026-11-16 Niko1221: sycl: Windows counts the room a page file may still grow by, in the Intel engine's own copies too (#5742, SYCL port)
cefd71248 2026-11-16 Niko1221: tests: DL99 expects the German Sie wording ("Ihr Modell ist heruntergeladen")
7fd5336c3 2026-11-16 Niko1221: tests: the agent profile test expects the gate's blocked-folder list (#5737)
7368a9d6d 2026-11-16 Niko1221: French: no-break spaces in the new 0.2.16 strings
7a06a5e74 2026-11-16 Elvis-Luo: metal: release prompt scratch buffers before workspace growth (#3527)
7ec17fa64 2026-11-16 Florian Nourrisse: metal: Context::alloc and wrap drain their own autorelease pool, so free() gives the buffer back
a1b7cd186 2026-11-16 Niko1221: cache: the RAM gate evicts nothing when even all parked conversations would not make room (#2253)
e05e6e0cc 2026-11-16 Niko1221: serve: a reply with tools that ends in tool-call markup that is no call is written again once; strata_unread_tool_markup
9dcee7083 2026-11-16 Niko1221: tests: slash-commands expects the German Sie wording ("Ihre Dateien wurden nicht geändert")
63f324dd4 2026-11-16 Niko1221: Settings: the blocked-folder field waits for an IME composition before Enter adds the folder (#5737)
f2cd2c033 2026-11-16 Niko1221: memory: Windows counts the room a page file may still grow by (#5742)
831bbd506 2026-11-16 Niko1221: memory: Windows counts the room a page file may still grow by (#5742)
cc0d0371f 2026-11-16 Niko1221: sycl: a GPU allocation above the card's single-allocation limit says so; the arena stops, an auto cache is sized to it (#5557, #5578)
6da257d80 2026-11-16 Niko1221: tools: batch_slot_park_test.py, a conversation continued after its batch slot was overwritten (#5401)
7966ebe6e 2026-11-16 Niko1221: serve (Metal): a batch slot is not parked before its overwrite (#5401)
ac2710f4f 2026-11-16 Niko1221: memory: the ZFS arcstats file is read on every system (#5519 follow-up: memory_guard_test failed on Windows)
756070beb 2026-11-16 Niko1221: Tests: the tuning-plan test's stub engine names unknown arguments, as the engine does
d80b5531e 2026-11-16 Niko1221: memory: the ZFS arcstats file is read on every system (#5519 follow-up: memory_guard_test failed on Windows)
152bc6e71 2026-11-16 Niko1221: Settings: Your rules, the person's own rules for every chat (#5084)
4a88fc266 2026-11-16 Niko1221: German: Sie in the tools catalog and the web page; a check that keeps it (owner decision 11-16)
5c342fab5 2026-11-16 Niko1221: German: Sie in the engine catalog and its generator (owner decision 11-16)
3f73ee04b 2026-11-16 Niko1221: German: Sie in the fix, tune and ui catalogs (owner decision 11-16)
554fe0cc4 2026-11-16 Niko1221: German: the app's main catalog addresses the reader as Sie (owner decision 11-16)
e977ee6d6 2026-11-16 Niko1221: Desktop shell: French in the tray and the shell prefs (0.2.16 languages check)
d77eb5a0d 2026-11-16 Niko1221: Web page: an Experts tab with the ranks the expert cache learned (#5723)
fd253804e 2026-11-16 Vitalii Parfyonov: Settings: when older messages are summarized, and what a new chat starts with (PR #4847)
985888a76 2026-11-16 Niko1221: Agent: blocked folders the assistant may not touch, in any mode (#5737)
8e5c5d10a 2026-11-16 Niko1221: Agent: Run as administrator, one command at a time, Windows asks each time (#5968)
5b089d829 2026-11-16 Niko1221: Web chat: answer from the thinking a Stop left without an answer (#5508)
85d2d56f1 2026-11-16 MegaRushX: Web chat: bring a saved chat back from its Markdown export (PR #4753)
5e587a9c4 2026-11-16 Niko1221: Web chat: the token count under an answer is a plural (1 token, Russian 1 токен / 2 токена / 5 токенов / 21 токен)
01ba9a7fa 2026-11-16 Niko1221: Chats: move a chat to another workspace from its Actions menu (#6051)
355fbceae 2026-11-16 Niko1221: tests: a HIP config beside NVIDIA cards is not sized as an NVIDIA card by the start-time fit (#5322)
374be3fdf 2026-11-16 Niko1221: Tests: damaged-chats.test.mjs keeps its storage and ends within its own time (fix-up of 4864a4daa)
ba334f333 2026-11-16 Niko1221: Chats: a storage that keeps no write does not make the first read wait forever (fix of 2068aafd7, #5422)
f8890fe16 2026-11-16 Niko1221: prefill: the Radeon 780M can take Gyro's trellis experts on the fused prompt kernels with STRATA_PF_TQ_G11=1 (#6067)
18735248d 2026-11-16 Niko1221: settings register: STRATA_PF_FUSED_SM75_KQ (the Turing K-quant fused path of 042f91a3f)
f91ca8ba9 2026-11-16 Niko1221: sycl: the arena memory reader counts the ZFS ARC above its floor too (#5519, SYCL port)
05eb785f9 2026-11-16 Niko1221: memory: the ZFS ARC above its floor counts as available RAM (#5519)
7708b7b4e 2026-11-16 Niko1221: settings register: STRATA_I8_SM70 (the Volta int8 tile rule of f-0216-tune-vt f41d35929)
e9eff1850 2026-11-16 Niko1221: metal moe: IQ1_M expert gate/up on the register-operand prompt chain (mm_gu3)
aac8a26eb 2026-11-16 Niko1221: settings register: STRATA_HEAD_ALIAS_TEST_MOVE, a test-only knob of #5188 (status research)
0ff6a85a5 2026-11-16 Niko1221: Setup: the 0.2.16 move-over renames and never copies (fix-up of 90fc7bfff, Q7)
90fc7bfff 2026-11-16 Niko1221: Setup: a clone's first run in the 0.2.16 layout carries its old state into terminal/ (MAP-0215 Q7)
165374a42 2026-11-16 Niko1221: Update: setup.py --update gets the newest code itself (git pull), as UPDATE.bat / update.sh did (MAP-0215 Q6)
c42ed6318 2026-11-16 Niko1221: memory: the ZFS ARC above its floor counts as available RAM (#5519)
6dac82609 2026-11-16 Niko1221: sycl: the INFO line reports the expert total, experts= beside expert_slots= (#5012)
2577c5f10 2026-11-16 Niko1221: --prefill-head-alias without an expert profile: the start ends with the --expert-profile error, not a SIGSEGV (NV-ALIAS-NOPROFILE)
dc58a88de 2026-11-16 Niko1221: tests: the fetch-reserve check of #5810 is skipped on a Mac
bbe17294e 2026-11-16 Niko1221: components: strata components add-build, an engine built on this computer as a local engine (#5114)
59b2fb5fb 2026-11-16 Niko1221: tests: the tuner's second engine spawn site is listed (#4652 follow-up)
46cc702ef 2026-11-16 Sergey: tests: name the PC the fake engine packages are built for (#4138)
cef9bca88 2026-11-16 Niko1221: setup: an Intel GPU built into the processor is never taken for an Arc card (#2115's safe part)
4df2fa0ac 2026-11-16 Niko1221: docs: the RX 6000 FP16 prompt default was not measured on Windows by us (#5151)
6152ed720 2026-11-16 Niko1221: engine: the INFO line reports the expert total; the qwen35moe engine reports its experts (#5012)
4df219b15 2026-11-16 Sam Nolak: conversation cache: preserve prefill-pipe plans when copying checkpoints (#5847)
be8f4d1f3 2026-11-16 Sam Nolak: conversation cache: keep checkpoint device tags when splitting stage parts (#5848)
196a32bdd 2026-11-16 Gabriel A. Devenyi: /v1/responses: tool_choice "required" and a named function force a call, as on the chat and Anthropic routes (#4835)
88c4e7939 2026-11-01 Spinoza: metal moe: instantiate IQ1_M's expert gate/up (the GSQ packs' experts)
c1fa42c13 2026-11-16 Niko1221: HIP: the RX 6000 cards read prompts with FP16 GEMMs by default (#5151)
05795a84a 2026-11-16 Niko1221: tool calls: Claude's `<invoke name="T"><parameter name="K">` dialect inside the wrapper is the call (#5969 parser part, recovery on)
30584e3da 2026-11-16 Niko1221: tests: every catalog is complete in all nine languages (0.2.16 languages check)
dca239508 2026-11-16 Niko1221: serve: the Intel reader takes GUI-1116's load rules for #5994, so its test runs against the re-export
ab3e8add7 2026-11-16 Niko1221: verify: drop_window_graphs is public, so the head-alias restore can call it (#5188)
30ce30b18 2026-11-16 Niko1221: settings register: STRATA_METAL_WRAP_PLE (#6024)
db7aca7f2 2026-11-16 Niko1221: launch: an Arc card is listed once when the shared reader already holds it
0b427a2b7 2026-11-16 Niko1221: launch: an Intel Arc card is sized from its own memory; the id table is the fallback (#5111 follow-up)
8baf90170 2026-10-20 Matthias Nott: fix(metal): wrap a Gyro file without its PLE table: the head and tail ranges only, no read-ahead of the table
042f91a3f 2026-11-16 Niko1221: Turing prompt experts: the fused kernels for the K-quant and Q8_0 pairs too (#6066)
7aaa98049 2026-11-16 Niko1221: tests: an Arc B-series beside an NVIDIA card starts with STRATA_ENGINE_BACKEND=sycl (#5111)
e04cb092f 2026-11-16 Niko1221: /v1/responses: the tools a client's own tool_search returned in this request are accepted as declared (#4621, #1917)
3fa42af43 2026-11-16 Niko1221: tests: the model folder stub borrows model_folder_trace too (#4887 follow-up)
e5f426aff 2026-11-16 Niko1221: settings register: STRATA_STOP_LAYERS and STRATA_STOP_STAGES (#6011)
d62581230 2026-11-16 Niko1221: drafting: an Intel config's /work MTP path is checked on the host (#5395)
be5a7422a 2026-11-16 Niko1221: tests: strata-sycl.sh passes a setting of 0 into the container (#4639)
028b96373 2026-11-16 Niko1221: settings register: STRATA_METAL_KEEPALIVE_MS and STRATA_METAL_KEEPALIVE_WINDOW_S (#6078)
f4eca4a61 2026-11-16 Krischan-Klug: serve: Codex's client-side tool_search, its finds declared where the search answered (#1917, PR #4621, prompt side)
4d692f450 2026-11-16 Niko1221: responses: Codex multi-agent v2 items (agent_message, multi_agent_call) are read, not refused (#4210, #5244)
d4c732f6a 2026-11-16 Niko1221: --prefill-head-alias: a head that comes back at another address drops the window graphs instead of stopping the engine (#5188)
69a8dad81 2026-11-16 Niko1221: tool calls: `<function=NAME` + line break (the `>` left out) of a declared tool opens the call (#6032 R6, recovery on)
4f7843fa5 2026-11-16 Niko1221: conversation cache: a failed K/V size estimate names its part and cause (#4384, the part kept)
9c349c45a 2026-11-16 Niko1221: tool calls: the model's empty stubs are skipped, a cut opener is dropped, a call with no readable parameter is not run (#6032 R5, recovery on)
d312a945b 2026-11-16 Niko1221: adaptive tier: a serve session does not choose the asynchronous tier by itself while STRATA_ADAPT_FETCH is on (#5814)
6339bb094 2026-11-16 Niko1221: MCP: a model that reads pictures gets the pictures its tools return, by default (#2343)
0f09a2eff 2026-11-16 Niko1221: docs: the Responses API table names Codex multi-agent v2's input items (#4210, #5244)
dcde1156c 2026-11-16 Niko1221: tool calls: a declared parameter written as the XML element `<NAME>value</NAME>` is read (#6032 R4, recovery on)
277af44e9 2026-11-16 Krischan-Klug: serve: Codex's client-side tool_search, its finds declared where the search answered (#1917, PR #4621, prompt side)
5205fc8bb 2026-11-16 Niko1221: serve: POST /load answers an engine that dies or sticks while it starts with a 503 (PR #4307, honest-answers part)
e46fd29a0 2026-11-16 Niko1221: serve telemetry: the Windows AMD reader reads only AMD adapters and only the engine's own card (#4884 follow-up)
ae9b390af 2026-11-16 Niko1221: tool calls: a body of `<arguments>` + a JSON object is the call's arguments (#6032 R3, recovery on)
3cb933d29 2026-11-16 Niko1221: responses: Codex multi-agent v2 items (agent_message, multi_agent_call) are read, not refused (#4210, #5244)
f8aad5b3d 2026-11-16 Niko1221: docs: INTEL.md Monitor readings work without root; the sampler is optional (#5988)
6ebbfdfa8 2026-11-16 Niko1221: serve: Intel Arc load and VRAM in the Monitor without root (#5988, from PR #5994)
b3e6361c5 2026-11-16 Niko1221: tool calls: damaged openers of a declared parameter not set yet are read as that parameter (#6032 R2, recovery on)
888c0db15 2026-11-16 Niko1221: update: no model test load when memory is short; an unproven engine falls back by itself (#5400)
b683a5f03 2026-11-16 Niko1221: conversation checkpoints: a layer split's stale parts go when the prompt read ends (#6011 follow-up)
dd1ddc6ea 2026-11-16 Keoian: prompt read: a Stop is seen by every stage of a layer split and between layers (#6011)
198cb95c9 2026-11-16 Niko1221: tool calls: a rejected undeclared call names the closest declared tool as a hint; nothing runs under a guessed name (#5904, #5933, #4622)
55a6dc414 2026-11-16 Niko1221: docs/MAC.md: the memory table and the streaming rule follow setup's new rule (#3983)
3c39183e1 2026-11-16 Niko1221: HIP gfx103x: no start-up tip asking for STRATA_HIP_PROMPT_F16=1 (#5151)
624cebd60 2026-11-16 Niko1221: docs/GYRO.md: Metal has decode and prompt kernels for the pair trellis (#6025)
cf5abac23 2026-10-24 Thomas Zenkel: mac_fit: setup decides resident vs streaming with the engine's rule (12 GiB beside the weights, resident_cap)
2569c79ec 2026-11-16 Niko1221: tool calls: the damaged followers end a value; a parameter's name is cut where the model ran past it (#6032 R1)
f513ad460 2026-11-16 Niko1221: Monitor: the GPU load tooltip (s9101) in reviewed ko wording (#5484)
fa01eee33 2026-11-16 Niko1221: Monitor: the GPU load tooltip (s9101) in reviewed pt wording (#5484)
b559cb8ae 2026-11-16 Niko1221: Monitor: the GPU load tooltip (s9101) in reviewed ru wording (#5484)
6acdb581b 2026-11-16 Niko1221: Monitor: the GPU load tooltip (s9101) in reviewed de wording (#5484)
4406cb7d4 2026-11-16 Niko1221: Monitor: the GPU load tooltip (s9101) in reviewed ja wording (#5484)
46801f654 2026-11-16 Niko1221: Monitor: the GPU load tooltip (s9101) in reviewed zh wording (#5484)
abcc03f29 2026-11-16 Niko1221: sycl: save and restore sessions without an MTP drafter (#1492, SYCL port)
cb5e504c8 2026-11-16 Niko1221: Language (French): the 0.2.16 translation pass of the GUI-1116 strings
4314a7565 2026-11-16 Niko1221: Language (Korean): the 0.2.16 translation pass of the GUI-1116 strings
8e246a6d1 2026-11-16 Niko1221: Language (Portuguese): the 0.2.16 translation pass of the GUI-1116 strings
28f680837 2026-11-16 Niko1221: Language (Russian): the 0.2.16 translation pass of the GUI-1116 strings
d611df3f7 2026-11-16 Niko1221: Language (Spanish): the 0.2.16 translation pass of the GUI-1116 strings
f57bb305f 2026-11-16 Niko1221: Language (German): the 0.2.16 translation pass of the GUI-1116 strings
262f2a012 2026-11-16 Niko1221: Language (Japanese): the 0.2.16 translation pass of the GUI-1116 strings
aa0d96380 2026-11-16 Niko1221: Language (Chinese): the 0.2.16 translation pass of the GUI-1116 strings
7089546a2 2026-11-16 Niko1221: Language: a test for the 0.2.16 translation pass (all languages checked)
64dde763c 2026-11-16 Niko1221: conversation cache: the SSD tier writes in the background (#5697, P2 step 2c)
3365da461 2026-11-16 bbingoCN: tune: probe the flags an engine accepts but does not document (#4652)
6e930669e 2026-11-16 ezoushen: drafting: a GPU lookup that found no card is made again, so a service started at boot gets DFlash2 (#5427)
677616cc9 2026-11-16 Niko1221: metal/tests/moe_mm_parity: accept the pair-trellis types TQP5/6/7, so their prompt kernels get a parity test (#6025)
265ccb475 2026-11-15 Matthias Nott: fix(metal): list the pair-trellis types (147-149) in the Metal quant tables so the intake tool's table matches iq_host.cpp
a7ee639f6 2026-11-15 Matthias Nott: build(metal): tqp_parity links the in-repo TQP reference when no fork checkout is given (TQP_REF_LIB entry points)
5327fc945 2026-11-15 Matthias Nott: build(metal): tqp_parity test against the pair-trellis reference (fork source or in-repo ref/tqp)
56f3e5aef 2026-10-25 Matthias Nott: fix(metal): deq_tqp reads the pair-trellis stream as 16-bit words (one 64-bit window a lane) instead of 24 byte loads: Coder-L decode 72 -> 85 tok/s
a632e75b5 2026-10-24 Matthias Nott: feat(metal): prompt kernels for the pair-trellis expert types TQP5/TQP6/TQP7
5e3541605 2026-10-23 Matthias Nott: TQP5/6/7: numpy reference decoder, fork C harness, parity fixtures from the real model
945265ee8 2026-10-23 Matthias Nott: feat(metal): decode kernels for the pair-trellis expert types TQP5/6/7 (147-149), CPU reference and expert_parity types
53d37e6f7 2026-11-16 Niko1221: docs, bench: PcieAuto on gfx103x, the measurements (#4007, #5984)
0fcfa45a6 2026-11-16 Niko1221: Metal: the #879 host scan of the logits rows as a branch-free reduction (#3287)
25c9dc514 2026-11-16 Niko1221: DFlash2 confidence: only a slot at least IQ3_S's is priced at its own size; IQ3_XXS keeps today's steps (#5700)
1b87d4d6a 2026-11-16 Niko1221: packaging: the Terminal bundle ships without pip and ensurepip's spare wheel (#5303)
bbb6e183a 2026-11-16 Niko1221: drafting: every other drafter decision takes the config's card family on a mixed NVIDIA + AMD computer (#5109)
c594b8e0d 2026-11-16 Niko1221: DFlash2 confidence: the pack's slot size covers the ISTA i-quant packs too; say so and test it (#5700)
904608ee2 2026-11-09 woodsonl: DFlash2 confidence: count slots at the pack's own slot size
d68fe3205 2026-11-16 Niko1221: bench: a run that finds no server names the address it asked (#5369, port part)
9466f6be3 2026-11-16 Niko1221: serve tests: long streamed tool arguments - same calls and streamed JSON in every piece size, time about linear (#4686)
fb3c3ea69 2026-11-16 InB4DevOps: serve/frontend: make the remaining streamed tool argument parsing linear (#4686)
620f3e034 2026-11-16 Niko1221: Revert 3fd8b4cae: the per-slot window cache did not fix STRATA_METAL_BATCH_ROWS=0
151f1d918 2026-11-16 Niko1221: procs: an engine whose parent or start time cannot be read is not called an orphan (#3789)
58d6d339a 2026-11-16 Niko1221: Revert #5918's fp16 K/V commits (82e0d2d46, 7406f8de1): --kv fp16 answers garbage on this head
188aaf7bf 2026-11-16 Niko1221: serve: the drafter is sized from the card the engine serves from on a mixed NVIDIA + AMD computer (#5109)
5c5731d0f 2026-11-16 Niko1221: serve tests: a cancelled run with no data sends no chunk, the role included (#4758 follow-up)
8426249f0 2026-11-16 Oleksiy Penkov: serve/frontend: a rewritten non-string parameter counts once with its later value; null placeholders by the declared type (#5493)
3fd8b4cae 2026-11-16 Niko1221: Metal: the slot-by-slot batch path keeps its encoded windows per slot (STRATA_METAL_BATCH_ROWS=0 answered garbage)
dc1c66d21 2026-11-16 Niko1221: docs/MAC.md: the first request after a load waits once for the prompt kernels (#5369, part 3)
b21fc065c 2026-11-16 Niko1221: tests: the missing-helper count no longer depends on this PC's graphics card
80843d373 2026-11-16 Niko1221: profiles: a missing profile that is a launch preset's name points at launch-<name> (#5369, part 2)
82e0d2d46 2026-11-13 Catalin: [Engine] Metal: saturate the fp16 K/V store and drop a non-finite cache term
7406f8de1 2026-11-13 Catalin: [Engine] honour --kv fp16 on Metal with direct-half kernels
7e53cd15c 2026-11-10 Fett2: Serve drafting: an Intel start lost DFlash2 because the check read strata-sycl.sh, not its binary (#5138 Bug 1)
c5fe0c146 2026-11-16 Niko1221: Agent: {{model_name}} names the model the chat was switched to (fix-up of d91c5cdd1, #5971)
36ca46942 2026-11-16 Niko1221: cuda12 engine packages carry sm_120 machine code; the PTX stays compute_89 (#5784)
217bc144d 2026-11-16 Dzmitry Senchankau: tests: stop the wizard-discovery test from reading the checkout's own run configs (PR #3521)
03c230a3e 2026-11-16 Niko1221: Metal: STRATA_NAN_INJECT reaches the #879 guard on the Mac, and the flagged row's position is this window's (#3287)
fc43bb769 2026-10-29 ctr-137: [SYCL] preserve STRATA_* environment values of 0 in strata-sycl.sh (#4546)
a1c56f544 2026-11-12 Catalin: [Engine] Metal: saturate the fp16 expert activations, the source of the #879 poison
3e7524e16 2026-11-12 Catalin: [Engine] Metal: barrier the fold against the window's projections so a torn read cannot seed the recurrent state with NaN
7d25cb9b1 2026-11-09 Catalin: [Engine] Metal: default the verifier's layer end so the #879 guard's gates open on the Mac
26aee8ce4 2026-11-09 Catalin: [Engine] Metal: record non-finite logits in both serve paths so #879 can end and flush a poisoned conversation
383236030 2026-11-16 Niko1221: settings register: STRATA_TEST_POOL_DELAY, the #5160 test hook (fixes settings_register.py --check after bba1a0e92)
c770de846 2026-11-16 Niko1221: tests: an old engine and a failed engine update do not end a launch (#5038)
2af552efe 2026-11-16 Niko1221: serve telemetry: the Windows AMD reader takes the first temperature the card reports (#3682, #4884)
5e965ec57 2026-11-16 Niko1221: tool calls: a parameter's type declared through anyOf / oneOf is read (#2371)
6bcc750bd 2026-11-16 Niko1221: discovery: a nest of models dirs counts as one level (PR #3528)
6a3bcc3b7 2026-11-16 Niko1221: Mac release steps refuse a binary that needs a newer macOS than the app's minimum (#4634, #4986)
e7199a026 2026-11-16 Niko1221: serve telemetry: the Monitor reads AMD cards on Windows through the driver's ADL2 (#4884, #1380)
88e6356a4 2026-11-16 Niko1221: native_dense_types_parity --head: the output head's real shape at 2, 5 and 8 columns (#6030)
bfa6315d7 2026-11-16 Niko1221: tune: strata tune auto takes an installed model by name, and --plan previews the tune (#5232)
fec06e9f7 2026-11-16 Niko1221: setup: --output jsonl, machine-readable progress for a program that installs a model (#4941)
e17d5c9c1 2026-11-16 Niko1221: setup --update: an Intel (SYCL) install reads the engine version from the engine, not the launcher (#4544, PR #4645)
6fe4c2491 2026-11-16 Momoyeyu: fix(serve): save and restore sessions without an MTP drafter (#1492)
1956aa16c 2026-11-16 Amit Tsur: chat completions: allow response_format with tools, as /v1/responses does (#4756)
99b1b27b1 2026-11-16 Amit Tsur: serve: a stalled peer does not hold a handler or the engine's turn (#4759, #2916)
f7734779b 2026-11-16 Amit Tsur: serve: send the stream role with the first response data (#4758, #2391)
6a1e6833d 2026-11-16 Niko1221: models: strata models explain NAME shows where the launch looks for a model (#4887)
f201b033f 2026-11-16 Niko1221: drafting: DFlash2 on the Coder when it is chosen by name (#5240)
fd67c5fa9 2026-11-16 Niko1221: Monitor: the GPU load card says what it measures (#5484, part 1)
33cfc83aa 2026-11-16 Niko1221: serve: fit_max_tokens never shortens max_tokens below room for an answer; below it, the context 400 (#5924 part 1)
54377532c 2026-11-16 Niko1221: HIP: iq_kernels.cu builds again (the Volta tile check is CUDA only) (#6053 follow-up)
029df1c73 2026-11-16 Niko1221: HIP: iq_kernels.cu builds again (the Volta tile check is CUDA only) (#6053 follow-up)
309e0b0c6 2026-11-16 Niko1221: telemetry: the Monitor reads an Intel Arc card from sysfs on every serve route (#5353)
ab72340ef 2026-11-16 Niko1221: drafting: no DFlash2 is planned for the Intel engine where it refuses it (#5747)
69857af16 2026-11-16 Niko1221: conversation cache: the SSD tier - evicted conversations go to disk and come back (#5697, P2 step 2b)
0d7eebeaf 2026-11-16 Niko1221: Docs: how to connect an HTTP tool server that needs a key (#5389)
019f3e2a3 2026-11-16 Niko1221: serve: before_load reads stdout and stderr apart; Windows-safe tests (#5987 follow-up)
3f83e96a1 2026-11-16 Niko1221: HIP: iq_kernels.cu builds again (the Volta tile check is CUDA only) (#6053 follow-up)
2a43d823e 2026-11-16 Niko1221: Linux window: the DMA-BUF renderer is turned off only where it is needed (#5417)
a154ac9ee 2026-11-16 Niko1221: setup / docs: the RX 6600 / 6600 XT / 6650 XT words for gfx1032 (#5174, #2784)
2b7798749 2026-11-16 Niko1221: Monitor: the host's own GPU readings fill every reading the engine lacks, field by field (#5946 #4660 #3727)
799764b4e 2026-10-17 chenxyz129: WIP gfx1032: setup ROCM_INDEXES/AMD_ARCHS/AMD_NAMES/AMD_CARDS, docs, setup test
f12b65334 2026-11-16 Niko1221: Metal: a bounded GPU keep-alive between requests, so the first command buffer after a pause does not wait (#6078)
3313dbd61 2026-11-16 Niko1221: docs: a greedy request is sent without the model card's penalties (#3295, #2940)
acc2211d3 2026-11-16 Niko1221: serve: a failed chat stream ends with the error object and [DONE], no finish_reason "error" chunk (#5633)
b9495f17a 2026-11-16 Vop3p: HIP gfx103x: PcieAuto on by default (#4007, #5984)
959689382 2026-11-16 Niko1221: Monitor: the VRAM hit rate column only when a request has one (#5484, part 2)
fcfe18e55 2026-11-16 Niko1221: Web Monitor: an empty GPU card says why, also when the GPU has a name (#5457)
4d27caa37 2026-11-16 Niko1221: Tasks: Run now works when a model is loaded in the app (#5383)
a9fbb4534 2026-11-01 oceanio: metal: pictures in batch slots, each slot rotates by its own M-RoPE table
244b41082 2026-11-16 Niko1221: HIP: the RX 6000 package covers the RX 6600 / 6600 XT / 6650 XT (gfx1032) (#5174, #5209, #4455, #4650)
ab0f20be0 2026-11-16 Gabriel A. Devenyi: Responses API: a request cancelled at the drain deadline gets 503 server_draining or response.failed, not 400 "malformed" (#4831)
3af02433a 2026-11-16 Gabriel A. Devenyi: Responses: a text.format answer cut by max_output_tokens ends incomplete with the text so far, not 502 or response.failed (#4830)
25d88c4a5 2026-11-16 Gabriel A. Devenyi: Anthropic errors: /v1/messages and /v1/messages/count_tokens answer an error in Anthropic's shape (#4834)
55ccf8556 2026-11-16 Gabriel A. Devenyi: /v1/responses: send Retry-After on a GpuBusy 503, as chat and messages do (#4833)
2e38afdfc 2026-11-16 Niko1221: Engine settings: Diagnostics shows only failures nothing has settled since (#5489)
1e5343e50 2026-11-16 Niko1221: Setup wizard: each engine card's size counts once when the host reports 0 (PR #3798 follow-up, #3727)
0266236ce 2026-11-16 Niko1221: split: the NVIDIA prompt-path pick does not count FNX_ARENA's unallocated expert slots as free VRAM (#5496, PR #5667)
b2c826738 2026-11-16 Niko1221: Monitor (web): the PCIe card shows the slowest card's link from gpu_pcie_bottleneck (#4623 / #5801 rule)
0027d210b 2026-11-16 Niko1221: tools tests: test_strata_mcp.py run directly runs all its tests (#4906)
b58d6cdfe 2026-11-02 hotocoo: [Engine] macOS builds target macOS 15.0, and the packager refuses a Mac binary that needs a newer macOS (#4634)
517e0baa5 2026-11-16 Eranicus30666: serve: put the streamed usage in its own final chunk when include_usage is requested (#2870, #5448, #5450)
3fc30c971 2026-11-16 Niko1221: Metal: --batch-mtp is left off with a warning instead of ending the engine (#5674)
2068aafd7 2026-11-16 Niko1221: Chats: two windows opened together move the browser's chats to the host once (#5422)
085860e4f 2026-11-16 Niko1221: serve: POST /load with an engine that cannot start is a 503 with the reason, not a dropped connection (#2497)
0b4d17edb 2026-11-16 Niko1221: serve tests: a refused batch admission adds no latency observation and no Prometheus success / prompt-token count (#3336)
d7ce708ba 2026-11-16 christopherrobertbrooks-tech: serve: temperature 0 stays greedy - no model-card penalties on a greedy request (#3295, #2940)
c844e3098 2026-11-16 Niko1221: serve: a chat stream the engine could not finish closes with finish_reason "error" (#5633)
7ca57d2c3 2026-11-16 Niko1221: prefill: the RX 7000 cards (gfx1100-1102) take Gyro's trellis experts on the fused prompt kernels (#6067)
937fe7115 2026-11-16 Niko1221: host tests: agent-host's readiness probe gives up on a host that never answers (#5577)
9c1a4b6e7 2026-11-16 Niko1221: App font: backticks and other spacing accents get their width back (#6068)
f59c0da97 2026-11-16 Niko1221: sycl: Prefill::release destroys only the queues the prompt path created, never the default in-order queue (#5405)
4864a4daa 2026-11-16 TheHubUser4860938: Chats: a damaged chat file has a surface and can be deleted; a newer Strata's chat is kept apart (#5809, #5421)
3ff8e6363 2026-11-16 Niko1221: Web page: the name in the header links to the project (#5510)
ee7033605 2026-11-16 LawiK974: launch, docker: --draft-vocab and DRAFT_VOCAB carry setup's draft vocabulary (#5786)
adf7324fe 2026-11-16 Joe Oghali: sm_60: the VMAD dp4a fallback's accumulator is early-clobber, so it never shares a register with an input (#4274)
cf0743747 2026-11-16 Gabriel A. Devenyi: Streams: an error after the 200 is the API's own last frame, not a second HTTP response in the body or a silent end (#4829)
200539a37 2026-11-16 Niko1221: setup: find ROCm's HIP compiler in lib/llvm/bin too (rocm-core 10.1) (#6071)
12add7952 2026-11-16 Stormace: fix(host): let the HTML preview panel use pointer lock (PR #5081)
3c48b8c07 2026-11-16 Niko1221: Metal: the PLE conv weight's load rule in a header with a GPU-free test (#5387, #5416, #5818)
d46463ab9 2026-11-05 cha: [Engine] Metal: narrow a BF16 blk.1.ple_conv1d to F16 at load
4d34b7f54 2026-11-16 Niko1221: Approval card: Approve no longer casts a shadow below its box beside Deny (#5077)
804003950 2026-11-16 Niko1221: HIP: the expdec int4 staging arrays take the aligned-after-declarator form (#5518, #5795, #5905, #4600, #4151)
e23bad99b 2026-11-16 Niko1221: strata serve: /v1's foreign-Origin check also covers an empty Origin and GET /v1 (owner 11-16)
473e92a91 2026-11-16 Niko1221: Serving API: without an API key, web pages of other sites can't use /v1 (owner 11-16)
518cec958 2026-11-16 Niko1221: drafting: a missing stock DFlash2 pack falls back to the tuned pack, not to no drafter (#5810)
cd14fd48a 2026-11-16 Niko1221: launch: run-defaults.json, user-wide server settings for every launch (#5858)
e56fb100b 2026-11-16 Niko1221: Translations: three host sentences this round shows get catalog keys; an approval card's error result is translated
a9b48530e 2026-11-16 Stormace: Chat: /compact in the chat's command menu (#5092, #5091)
ceb26f223 2026-11-16 Niko1221: Chat errors: the engine-failure sentences are in the catalogs; s9044's German uses Sie like the rest
4e645853a 2026-10-30 au70ma70n: [GUI] settings: let a long help line wrap instead of squeezing every field
ce664a958 2026-11-16 峯岸　亮: Local models: a GGUF whose window is 1K or 2K tokens can be imported and run (#4249)
a421f7dee 2026-10-29 Nyarlathoteppppp: image models: downloads honour HF_ENDPOINT like setup and the MTP fetch (#4369)
aa4bafd1d 2026-11-16 Niko1221: launch: programs on this computer read a One-address server at that address (#5917 follow-up)
a1047b7fd 2026-11-16 ruibeikaa: Monitor: an impossible PCIe traffic reading is no reading (#4713)
2ce8d8272 2026-11-16 jun76: Monitor: total power counts the cards that report it, as the energy meter does (#4430)
12121745c 2026-11-16 Hermes Agent: Models: a packaged Qwen3.8 model shows the KV format it was saved with (#5374, #5919)
25822a9cb 2026-11-16 Niko1221: monitor: reach a server on one address of this computer over HTTP, without a proxy (#5917 follow-up, #4207)
e81a74af3 2026-11-16 Niko1221: Serving API: /v1/models also says context_length, so clients need not use the engine's private port (#5893)
c6903e998 2026-11-16 吴佳浩Alben: launcher: start the bundled runtime when access(X_OK) is denied (#4312 #4309)
afc36b1de 2026-11-16 Niko1221: tests: a no_child marker that cannot be written never publishes host state (#4250)
a82132337 2026-10-27 Miquel Alsas: Native serving reports each loaded model's context window: /v1/models gains meta.n_ctx, the key the control server already uses, left out when unknown rather than 0 (#3931)
96edb9337 2026-11-16 Niko1221: conversation cache: the RAM gate stops evicting when memory does not come back (#5697)
b1aa5fc75 2026-11-16 Niko1221: Approvals: an approval the host no longer waits for ends its card instead of asking forever (#5308)
64050ffaa 2026-11-16 anon761: generate: --expert-support reports GPU expert-kernel support without a pack or a GPU (#6059)
85c949f85 2026-11-16 Justin Capella: engine: a failed prompt-read kernel check under --serve ends at once with an ERR line (#6054)
1b58c335d 2026-11-16 Momoyeyu: fix(serve): save and restore sessions without an MTP drafter (#1492)
5e29505f7 2026-11-16 Niko1221: models import / setup --gguf-dir: a Qwen3.6-35B-A3B file the Qwen3.6 engine loads is accepted as family qwen36 (#5869)
d91c5cdd1 2026-11-16 Niko1221: Agent: the assistant is told the name of the model it runs on, not only its id (#5971)
3c0300cfb 2026-11-16 Niko1221: test_cmake_script_policies: no -P script with IN_LIST is left (f-0216-ggml2 step 10)
4ea65a39f 2026-11-16 Niko1221: Goals: failing tool calls pause a goal with one sentence (#4981)
08e0a5c17 2026-11-16 HexGrimm: A new chat opened from a chat on an API model starts on that model (#5750)
d5c920128 2026-11-12 Heinz N. Gies: Wait for the chat saves before the reattach test removes its folder
dce45ccc7 2026-11-16 Niko1221: Chat: a web address written as plain text in an answer is a link (#6000)
0fc79a8a5 2026-11-16 Niko1221: Chats: a reply streamed into a big chat no longer rewrites the whole chat every second (#5923)
9314ced9c 2026-11-16 Niko1221: drafting: the DFlash2 download honours HF_ENDPOINT, read at each fetch (#5083)
1f6ed28df 2026-11-16 slyfox1186: strata_cli: the Advanced table does not call an environment setting a typing mistake (#5600 #5136)
ff3f85511 2026-11-16 Niko1221: serve: a before_load refusal answers with the command's own reason (#5987)
241dbde61 2026-11-16 Anonymous: [TUI] readiness: probe /v1/telemetry with the telemetry key when there is no API key (#4161)
577e1287a 2026-11-16 Niko1221: conversation cache SSD tier: the spill store - entries written as session files, matched, read back (#5697, #5835)
61dac9f42 2026-11-16 Shikaku: launch: keep the Settings view's values across launches; --set idle-unload writes the server's key, not an engine flag (#5371 #4985)
5a43df088 2026-11-16 lamboJw: Chat speed line: register its two live templates in every catalog, so no language shows raw {0}{1} (#4620)
a54f9dbbb 2026-11-16 Niko1221: tool calls: a parameter's type declared through anyOf / oneOf is read (#2371)
d33537215 2026-11-16 Niko1221: launch: "fit to your card" for Qwen3.6 takes setup's rule for the model and context (#5239)
3612d32b6 2026-11-16 Niko1221: launch: Qwen3.6-35B-A3B in the model list as a group of its own, as the app lists it (#5869)
a1c210144 2026-11-16 Niko1221: Chat: a closed preview panel stays closed at the next start (#5548)
32502389a 2026-11-16 Niko1221: API models: an earlier picture never stops the chat; the newest four are kept (#4311 review)
c79654b6a 2026-11-16 dan64: serve: one unknown key in .shared-settings.json no longer clears the rest (#4934 #4933)
a8a3df28c 2026-10-27 szl0834: [GUI] Preserve image messages in provider chat history
705b92319 2026-11-16 Niko1221: tune / presets: keep the 4K prompt speed as pp4k and the long prompt's apart, so a recheck compares like with like (#5324)
f5c07ddfd 2026-10-29 lamboJw: serve telemetry: each card's PCIe link and traffic in "gpus"; the machine's link is the narrowest card's
4aaec72f8 2026-11-16 Niko1221: Monitor: the card the engine runs on when the config names none and its environment picks one (#4640)
ac4d569bc 2026-11-16 Niko1221: Serving: a switch per model, "Tools for apps on this computer", off by default (#5661)
02deda130 2026-11-16 Niko1221: conversation cache SSD tier: one folder per engine process, dead ones cleaned, and its budget (#5697, #5835, #6034)
7f6757c67 2026-11-16 Niko1221: Serving API: a model's MCP tools only for a keyed client of this computer that the person opted in (#5661)
03b402dad 2026-11-16 Niko1221: Int8 prompt kernels on Volta: the same products on the FP16 tensor cores for long prompts, bit-identical (#6053)
92373a464 2026-11-16 Niko1221: Delete a model: a read-only file or an empty read-only folder no longer leaves the pack behind (#4089)
beff6c2b0 2026-11-16 Niko1221: settings register: STRATA_I8_SM70 (the Volta int8 tile rule of f-0216-tune-vt f41d35929)
97211fe0e 2026-11-16 Niko1221: native helpers: one versioned contract, explicit opt-in, exact fallback; the GGUF preflight helper uses it (#5961 #5978)
16fac56ad 2026-11-16 Niko1221: Time Skip: a chat's second trial keeps its Stop when the first trial ends (#4611)
9f8fafa0f 2026-10-29 The Undercouch Studios: apps/host: a Time-skip trial drops its poll, entry, chat pointer, model choice and ended promise
0f6994f52 2026-11-16 Niko1221: SYCL Monitor: an Intel load that cannot be measured yet is unknown, not idle; the old sampler fills gaps (#5994 review)
88787f851 2026-11-16 Rob Riggs: SYCL Monitor: Intel readings without root or a helper service (#5994)
e907a56ea 2026-11-16 Niko1221: Agent: a cloud model's maximum output is no longer reserved for every reply, so compaction does not start after 4K tokens (#5011)
88b5ca6d0 2026-11-16 Niko1221: [Docs] the MMQ build path is gone: four pages say where the old numbers and builds come from (own-stack step 10)
659ad380c 2026-11-16 Niko1221: Agent: an agent that does not answer is no longer reported as a refused mode, and the cause is logged (#5070)
3e26b4e15 2026-11-16 Niko1221: [Engine] remove llama.cpp's MMQ build path and the vendored ggml-cuda (own-stack step 10)
553a0d3bd 2026-11-16 Niko1221: setup: colour in the menus only where the terminal shows it (#5935)
5820ff60d 2026-11-16 Niko1221: launch: "One address only" - serve on one address of this computer (a second network card, a VPN) (#5917)
fa77c94ac 2026-11-16 Niko1221: Chats: a start reads only the chats saved since the index was written (#5359 review)
955a2c31d 2026-11-16 Hermes Agent: Chats: the chat files own their revisions at start, so a failed index write cannot roll a revision back (#5359)
f56ef6fe9 2026-11-16 Niko1221: serve: refused parks counted by reason in /metrics and the Prometheus text (#6081)
0df5bb13f 2026-11-16 Niko1221: Host: an adopted OpenAI-style server is asked for a model it listed, not "local" (#5574)
9c8eb61f6 2026-11-16 Hermes Agent: Tests: the host suite runs with a scratch HOME, USERPROFILE and STRATA_HOME too (#5775)
e06e5d871 2026-11-16 Niko1221: Host: a job list JSON cannot hold is logged and skipped, not thrown out of every state change (#5802 review)
e19adee7e 2026-11-16 likenparklioo: Host: a failed save of the native job history no longer stops inference or polling (#5802, #5744)
497ee681c 2026-11-15 Richard Ayotte: fix(sycl): stop relinking every executable on every build (#6042)
04acca9c1 2026-11-16 Niko1221: sycl: the start-up log names the Level Zero loader, UR adapter and SYCL runtime files in use (#5914)
71ff7c6b1 2026-11-16 Niko1221: sycl: --ple-gguf: a file whose only tensor is the PLE table is a table, not a model shard (#6026, #6013; port of 290d4f57f)
ec8a1d12e 2026-11-16 Salvatore Mendola: setup: colour the model family and size names in the menus (#5935)
3cf039689 2026-11-16 Niko1221: --ple-gguf: a file whose only tensor is the PLE table is a table, not a model shard (#6026, #5942, #6013)
70667dd72 2026-11-16 Niko1221: Approvals: Details shows the whole command the agent asks to run, not its first 600 characters (#5856)
9e4ef7ee8 2026-11-16 Niko1221: Agent: OpenAI-style servers other than OpenAI get no "store" field, so Gemini answers (#5903)
3321fe756 2026-11-16 Niko1221: launch / connect: say how to see a hidden key, and that a key that is on is checked on this computer too (#5948)
15cb96072 2026-11-16 Niko1221: telemetry: the top-level PCIe fields stay card 0's; the slowest card is named in gpu_pcie_bottleneck (#5801 #5981)
4c3470aa8 2026-11-16 Niko1221: conversation cache: a park that cannot fit is refused before anything is evicted (#5697)
3c503be7a 2026-11-16 Niko1221: Test: the store's error test follows the chat error branch of 7bcb5a69c
adafc50b5 2026-11-16 Niko1221: Agent: a model's "Tool timeout (seconds)" reaches its MCP servers in the desktop agent (#5788)
da6391c77 2026-11-16 Chak @ WCH: Agent: an MCP server's own timeout reaches the Harness as toolCallTimeoutMs (#5790, #5788)
6f807dfc6 2026-11-16 Niko1221: Start-up line: name the native output head's real GGUF type instead of "Q5_K" (#6030)
cd4b7d7ee 2026-11-16 Stuart Chapin: add the strata-gguf-preflight Rust crate (#5961)
6f5ad10c6 2026-11-16 Niko1221: tests: list the AMD test start's strata-device probe as a spawn site (#6015)
7bcb5a69c 2026-11-16 Niko1221: Errors: an engine that stops or fails while answering is said so in plain words, with its line under Details
d6e670171 2026-11-16 Niko1221: Agent: a wake that starts before the idle watch's first snapshot, and several wakes while no page is open, all reach the chat (#6070 review)
7496424a5 2026-11-16 Niko1221: Host: a link or file the opener refuses is a 400 with its reason, not a 500
98f984998 2026-11-16 Niko1221: Errors: an OpenAI-shaped error body shows its message, not raw JSON
4fc847203 2026-11-16 Jie Ren: Monitor: each card gets its own PCIe ceiling and power limit, so a card that runs narrower than it could is visible (#5801)
2c48a5698 2026-11-16 Niko1221: setup: plainer words for the parallel note when RAM rules it out (#6046)
695233185 2026-11-16 Niko1221: tools/logits_dump.py: read STRATA_LOGITS_DUMP records with their headers (#6030)
b9eff8d34 2026-11-16 Niko1221: runtime: the restart plan reports the stop phase's limit and, apart from it, the last stop's time; protocol notes (#5956 #5958 #5954)
e86074f3c 2026-11-16 Niko1221: Storage: list the DeepSeek models of an earlier Strata so their files can be seen and freed (#6048)
f830a0001 2026-11-16 Niko1221: serve: "ERR verify: the GPU stopped waiting" is a fatal engine line, like the #267 timeouts (#5160)
680a400cc 2026-11-16 Niko1221: Web chat: a picture is attached at once and keeps its original when no preview can be made; stored previews are checked (#5998 review)
a9f2de40f 2026-11-16 Guillaume PUTIER: setup: parallel counts pinned RAM and per-cell VRAM at long contexts (#6046)
b1cdaa389 2026-11-16 Niko1221: serve: a request cut off by the server stopping the engine fails (503), not "length" with 0 tokens (#6055)
289752e03 2026-11-16 MegaRush: Web chat: a small thumbnail of an attached picture rides with the name into the saved chat (#5998, #5509)
420b7fe57 2026-11-16 Milly: Agent: a reply the agent starts by itself after a background command finishes reaches the chat (#6070)
9824b2e7a 2026-11-16 Niko1221: engine test start (AMD): the engine sees only the cards its package has code for; a repeated failure says so (#6015)
2c8d300ad 2026-11-16 Niko1221: --prompt-cache-every: the periodic checkpoints sit on the resumed request's grid (#6052)
398ff4b5a 2026-11-16 Niko1221: tool_addition: system messages only, the outer shape checked, one definition per name (#6005, #5952)
5f5a35b85 2026-11-14 connorbanting03: [Engine] read tools from Anthropic tool_addition blocks (#5952)
f41d35929 2026-11-16 Niko1221: Int8 prompt kernels on Volta: the tile that keeps two blocks per SM, and the big grids read from global memory (#6053)
5480e2bad 2026-11-16 Niko1221: Int8 prompt kernels: write each group's launch record with a small kernel instead of a host copy (#6053)
6a139a1a2 2026-11-16 Niko1221: serve: a restart during a slot's release does not touch the new engine's claim (#5657, #4451)
e331637df 2026-11-09 MIDHAT NASHAR: [Engine] transfer cancelled slot claims before starting the release waiter (#5657)
7c4b55cb3 2026-11-16 Niko1221: connect --write --if-unchanged: compare the bytes the write would produce, keep an unchanged file private (#5957)
ac7c09367 2026-11-16 Niko1221: setup --prepare-pack: the step line says "model file reader ready", not llama.cpp's gguf-py
290d4f57f 2026-11-16 Niko1221: --ple-gguf: a file whose only tensor is the PLE table is a table, not a model shard (#6026, #5942, #6013)
db410c88b 2026-11-16 Niko1221: Harness: a restarted MCP server gets a new session in the desktop agent instead of failing every call (#6014)
bba1a0e92 2026-11-16 Niko1221: sycl: a GPU wait on the host that runs out fails its window instead of using stale expert rows (#5160, #5992, #6016)
6de12dc91 2026-11-16 Niko1221: launch: the Advanced step works out the engine command once per set of choices, not on every key (#5940)
443a0c330 2026-11-16 Niko1221: Models: no "Context memory" select for Qwen3.6, which has no KV-format choice (#5919)
0a26f8357 2026-11-16 l473n79c618e: feat(connect): --write --if-unchanged leaves a file that already holds the rendered content alone (#5957)
a71b0abd1 2026-11-16 Niko1221: Harness: one unreadable folder no longer blanks a whole glob / grep in the agent (#5964)
6f5382c1f 2026-11-16 Niko1221: connect --write: one order and the same side effects in both output modes (#5955)
16d2a7dfc 2026-11-16 l473n79c618e: fix(connect): make --write --output json run the write and report each file (#5955)
6ba86f961 2026-11-16 Niko1221: sycl: window_jobs_test --legacy runs the cases through the 756242554 loop and must fail (#6016)
633db39c7 2026-11-16 Niko1221: strata-q36 standalone entry: the Turing fused set-up as strata --model has it (one switch list for both entries)
21d15ebf7 2026-11-16 Niko1221: vision: gfx1151 (Strix Halo) takes F16 inputs for BF16 matrices too
d860f672e 2026-11-16 Niko1221: First run: name the card in setup's order, a discrete card before the processor's graphics (#6015)
3bd38bbaa 2026-11-16 Niko1221: test_faulthandler: the shipped Python 3.12 names no threads; a closed error output and a log file (#5921)
7b73ebf93 2026-11-13 gingertonik: serve: a native death of the server names its Python line in its own output
f0c526a81 2026-11-16 Niko1221: First run: name the card with the most memory, not the processor's graphics listed first (#6015)
066929d41 2026-11-16 fumisato407-crypto: Fields: the Enter that commits an IME conversion runs no field's action, in the app and in the web page (#6033, #5071)
d47229d5a 2026-11-16 Dmitriy: drafting: keep an explicitly selected DFlash2 file (--draft-model in user_args) (#5902)
ebc61512c 2026-11-16 Niko1221: route_prior_parity: STRATA_ROUTE_PRIOR on synthetic router rows, degenerate and rankable (#5655)
5144e8b53 2026-11-13 William Stone: Route prior: commit the biased top-10 atomically - a partly readable row keeps the router's top-10
709d0a99c 2026-11-09 William Stone: Route prior: a degenerate token keeps the router's picks instead of a sentinel expert id
511dfc8ea 2026-11-16 Niko1221: Build scripts: the picture reader takes no -DLLAMA_DIR (or GGML_*) any more
8dbfd5210 2026-11-16 sonic-netizen: Host: native Monitor rows carry the engine's hit rate and PCIe share, so the VRAM hit rate column is no longer always a dash (#6079)
ca3c58c46 2026-11-16 Niko1221: vision: the Metal reader holds BF16 matrices as F16 and writes their inputs as F16
b6ce9d479 2026-11-16 Niko1221: STRATA_CKPT_ASYNC: one owner for the checkpoint staging buffer from the join to the launch (#6075)
af44aac1d 2026-11-16 Niko1221: Desktop: the Windows and macOS app tells its host it is the app window, so links in answers open in the browser (#5072, #4721)
2b81d475e 2026-11-16 Niko1221: serve/mcp.py: a restarted HTTP MCP server gets a new session and the refused call runs once (#6014)
9eef1667c 2026-11-16 carlos: sycl: the xe spin bound follows the host: 1,000,000 reads once a stage can ask the host (#5992, bound part only)
9a3ae96c6 2026-11-16 Niko1221: tests: the start's wait for its owner's state file, model-free (#5601)
f0f39de26 2026-11-15 carlos: sycl: expert_pool_dispatch_multi reads one snapshot of ids and clears job_of exactly where it opened jobs (#6016)
5c35417bc 2026-11-16 djmarker287-code: Host: the LAN share listener passes POST /v1/responses on to the API handler (#5925)
00d0fe58f 2026-11-16 djmarker287-code: Host: a malformed JSON body on an inference route answers 400, not 500 (#5930)
347b29592 2026-11-16 Vladimir: Host: compare the model library's file IDs as BigInt so two folders with large IDs are not taken for one (#6037)
18fdeb21c 2026-11-16 Niko1221: [Engine] quant layer: the Q8_K quantizer keeps its product unfused under Clang / icx too (step 4 follow-up)
f6de3a6c6 2026-11-16 Niko1221: test_setup_stale_stamp: the ARM64 engine build is without MMQ too (f-spark-nommq)
1fc1777ec 2026-11-16 Niko1221: Docs: strata-vision is Strata's own picture reader
d2cdf854e 2026-11-16 Niko1221: Picture reader: strata-vision without llama.cpp's mtmd, llama or ggml
525ba0ea7 2026-11-16 Niko1221: [GUI] web host: remove the unused autostart.mjs and its test (own-stack step 9 leftover)
6da3a80e5 2026-11-16 Niko1221: [Engine] Intel Arc: the CPU expert pool on Strata's quant layer, no ggml in the SYCL engine (own-stack step 4)
8dadf18ad 2026-11-16 Niko1221: install.sh: install-manifest.txt with CRLF line ends reads the same
cd2b464ed 2026-11-16 Niko1221: Picture reader: remove the "Picture reader" setting and the start-up fallback to llama.cpp's reader
b55ae23e8 2026-11-16 Niko1221: strata_mcp: the engine named as a component is missing only when it is not installed
ffb11f070 2026-11-16 Niko1221: [Engine] quant format header: Strata's own, generated from its type tables (own-stack step 5)
660cddf49 2026-11-16 Niko1221: serve: the Qwen3.6 engine is not sent the VRAM command it does not have (picture reader start, POST /v1/vram)
2c0a77d9b 2026-11-16 Niko1221: Picture reader: our tower on every GPU under auto (the three mtmd rules go)
cbeac69d6 2026-11-16 Niko1221: setup on a Mac (app mode): a model whose list entry has no draft layer plans and starts with no drafter, as on Windows and Linux
f46cb8aa0 2026-11-16 Niko1221: launch: the Intel card's pack step downloads nothing, and the plan, the step line and the failure hint say so
30f28ecc9 2026-11-16 Niko1221: ctest no_mmq_symbols: a named cuobjdump look that did not run fails the test with its reason (check_no_mmq exit 3)
86c00f44b 2026-11-16 Niko1221: spark: the GB10 numbers of the build without MMQ in build_engine.sh
b9d5fb1eb 2026-11-16 Niko1221: host test turn-reattach: the temp chat folder's removal retries (a late chat-store write left it not empty on the macOS runner)
cc1c75582 2026-11-16 Niko1221: [Engine] Mac: the CPU expert pool on Strata's quant layer by default, no ggml in the Metal engine (own-stack step 3)
f154ed87d 2026-11-16 Niko1221: check_no_mmq: a look that did not run is named, and a named one fails the check
edce8fe09 2026-11-16 Niko1221: [Engine] step 1 follow-up: the HIP prompt test programs only in a build that has ggml
e93650d1e 2026-11-15 Niko1221: [Engine] step 1 follow-up: file_expert_source_test takes the type ids from Strata's table
3e528494c 2026-11-15 Niko1221: [GUI] web host: remove the llama.cpp download (POST /api/engine/binary)
9cfa8ec5b 2026-11-15 Niko1221: spark: build the DGX Spark engine without llama.cpp's MMQ
5c3541b6a 2026-11-15 Niko1221: [Engine] SYCL: delete four prompt-kernel files and the migrated header copy that no build compiles
7dc0ad0af 2026-11-15 Niko1221: [Engine] x86 CUDA / HIP builds: no ggml-base / ggml-cpu (own-stack 0.2.15 step 1)
```

### whisper.cpp — 4 commits

```
ca19af244 2026-11-19 Daniel Bevenius: ci : pin emscripten sdk version to 7.0.0 (#4160)
91c1e144f 2026-11-19 Daniel Bevenius: examples : remove explict version from test-cmake (#4172)
cb4da344d 2026-11-19 Daniel Bevenius: ci : add API/ABI check to make-release workflow (#4185)
8bf716f99 2026-11-19 Daniel Bevenius: examples : set LLAMA_TAG to commit that fixes ctz64 on win32 (#4189)
```

### stable-diffusion.cpp — 0 commits (unchanged)

### llama-cpp-python — 0 commits (unchanged)

### acestep.cpp — 0 commits (unchanged)

### qwen3-tts.cpp — 0 commits (unchanged)

### parakeet.cpp — 0 commits (unchanged)

### sdcpp-webui — 0 commits (unchanged)

### libwebm — 0 commits (unchanged)

