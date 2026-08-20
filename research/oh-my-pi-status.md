# 📦 Oh-My-Pi: 7-Day Release Activity & Module Breakdown

This document tracks releases of [`can1357/oh-my-pi`](https://github.com/can1357/oh-my-pi) published over the last 7 days (August 13, 2026 – August 20, 2026), moving chronologically from the oldest release (**v17.3.0**) to the newest release (**v17.4.0**). It focuses specifically on **Breaking Changes**, **Added** features, and **Changed** behavior per module.

---

## 🌐 Executive Summary (Last 7 Days Highlights: v17.3.0 – v17.4.0)

- **Native Multi-Model Tokenization & API Overhaul (`@oh-my-pi/natives`, `@oh-my-pi/agent`)**:
  - **Breaking Architecture Change (`v17.4.0`)**: Deprecated global token counting methods in favor of model-scoped, immutable `Tokenizer` instances (`agent.tokenizer`). All context pruning, cut points, and branch management require an explicit `Tokenizer`.
  - **High-Speed `ctok` Native Tokenizers**: Integrated native Rust/napi token counters for Anthropic Claude (`ClaudeV3`, `ClaudeV47`, `ClaudeV5`), Qwen (3.5+, 3.6+, 3.8), DeepSeek (V3, V4, R1), Kimi (K2, K3), and GLM-5 with zero-allocation JS interop.
  - **Delta Estimation**: Added provider-anchored incremental transcript token estimation (`findTranscriptUsageAnchor`, `estimateTranscriptTokens`).

- **Speculative Parallel Compaction & Seamless In-Place Handoff (`@oh-my-pi/coding-agent`, `@oh-my-pi/snapcompact`)**:
  - **Speculative Compaction (`compaction.asyncEnabled`)**: Compaction runs asynchronously in the background while the interactive session continues, instantly splicing the result when ready.
  - **In-Place `/handoff`**: Compaction and handoff now compact directly in place rather than forking separate session branches.
  - **Method Prioritization**: Introduced `compaction.methodOrder` (e.g. `[remote, snap]`), prompt-injection hardening on summaries, and transparent compaction dividers displaying exact methods and context shifts (`256K→20K`).

- **New In-Session Developer Tools & Process Supervision (`@oh-my-pi/coding-agent`)**:
  - **`/cleanse` & `omp cleanse`**: New in-session interactive checker/repair supervisor displaying a live board of checkers, subagents, and token/cost totals.
  - **`omp ps`**: Interactive monitor and supervisor for daemon-supervised background processes.
  - **Backgroundable Python**: `eval` cells can now execute asynchronously and auto-background like `bash` commands with customizable thresholds.

- **TUI & Composer Layout Redesign (`@oh-my-pi/tui`, `@oh-my-pi/coding-agent`)**:
  - **`composer.shape`**: Configurable editor frame styles (`box`, `claude` rules, `pi` rules, `borderless`) with live preview in `/settings`.
  - **Context Line Usage Gauge**: Added `statusLine.contextLine` (`percentage`, `annotated`, `embedded`) displaying active token saturation and compaction markers.
  - **Overlays & HUD**: Revamped the todo HUD with animated tree-spine progress, unified dialog panels into titled rounded boxes, and added `/models` instant type-to-filter focus.

- **Long-Context Codex Tiers, Provider Routing & Prompt Cache Policy (`@oh-my-pi/catalog`, `@oh-my-pi/ai`)**:
  - **Codex GPT-5.6 Long-Context Support**: Supported 272K+ token cost tiers on Sol, Terra, and Luna, and introduced the `extendedContext` setting + `/extended-context` toggle.
  - **Provider Enhancements**: Added support for OpenAI Daybreak Blue/Red and GPT-5.6 Cyber, GLM-5.3 (z.AI), DeepSeek V4 Pro (`low`/`high`/`max`), and dynamic Antigravity Gemini 3.7 Flash discovery.
  - **xAI Architecture Alignment**: Switched paid xAI (`XAI_API_KEY`) and SuperGrok to the OpenAI Responses API with encrypted reasoning replay, setting Grok 4.6 as default.
  - **`providers.cacheRetention`**: New protocol setting to control prompt-cache TTLs (`auto`, `short` 5m, `long` 1h, `none`).

- **Native Runtime, Shell Streaming & Tree-Sitter Acceleration (`@oh-my-pi/natives`, `@oh-my-pi/utils`)**:
  - **Progressive Line Buffering & Pipeline Concurrency**: Shell builtins (`grep`, `rg`, `sed`, `cat`, etc.) stream progressively with destination-aware line buffering; pipeline compound blocks execute concurrently without head-of-line blocking.
  - **Tree-Sitter Caching**: Bounded AST caching cuts `read` tool overhead by up to 90%+. Added `nodeChainAt` native API.
  - **`pdf-inspector`**: Integrated `pdfToMarkdown` native API, replacing MuPDF-WASM.

---

## 📅 Release-by-Release Detailed Changelog

### 🚀 Release `v17.3.0` (2026-08-13)

#### Module: `@oh-my-pi/agent`

##### **Fixed**
- Improved the manual `/shake` command to retain a small history of recent tool results, preventing the agent from losing its active working context.

#### Module: `@oh-my-pi/ai`

##### **Breaking Changes**
- Renamed `withGeminiThinkingLoopGuard` to `withThinkingLoopGuard`; the guard applies to Gemini, DeepSeek, and Grok model-id families.

##### **Changed**
- Updated OpenCode Go integration to use the official usage endpoint, removing hardcoded caps, enabling real-time credential validation, and routing multi-key pools based on rolling and weekly headroom.
- Optimized Anthropic prompt caching with rolling 5-minute breakpoints and idle refreshes to keep the prompt prefix warm.

##### **Fixed**
- Fixed Ollama chat adapter to correctly forward sampling parameters like temperature and topP to the provider.
- Fixed OpenAI agent turns ending prematurely after a web search with no visible answer, ensuring the agent continues processing the search results.
- Fixed a resource leak where completed model streams retained provider concurrency permits longer than necessary.
- Fixed image input support for qwen3.8-max and newer models when using DashScope compatible-mode.
- Fixed xAI usage reporting falling back to a stale cache when a new weekly cycle starts with 0% consumed credits.
- Fixed Together AI login validation failures by querying the authenticated models list instead of a hardcoded model.
- Fixed credential-health probes and usage fetches failing when using reference-stored API keys (such as environment variables or commands) by ensuring secrets are correctly resolved.
- Fixed Perplexity email-OTP login by preserving the session cookies required for verification.
- Fixed thinking configuration for OpenAI and Daybreak models to correctly send reasoning.effort: "none" when thinking is disabled.
- Fixed Grok runaway thinking streams bypassing the thinking-loop guard.

##### **Removed**
- Removed legacy local request-cost estimation machinery and database schemas previously used for OpenCode Go estimates.

#### Module: `@oh-my-pi/catalog`

##### **Breaking Changes**
- Removed `OpenAICompat.enableGeminiThinkingLoopGuard`; thinking-loop eligibility is derived solely from the `model.id` family.

##### **Added**
- Added first-party OpenAI Daybreak Blue, Daybreak Red, and GPT-5.6 Cyber models with full support for their documented API pricing (including long-context rates above 272K input), token limits, tools, and reasoning effort controls (off/low/medium/high/xhigh/max).
- Added calculateUncachedInputCost() to calculate prompt pricing against active context-length tiers without prompt caching.

##### **Fixed**
- Fixed Anthropic cache-write pricing to correctly honor mixed 5-minute and 1-hour TTL usage instead of incorrectly charging all writes at the 5-minute rate.
- Fixed Ollama Cloud DeepSeek V4 Flash and older reasoners to correctly apply the DeepSeek effort contract (e.g., low/high/max) instead of the generic effort ladder.
- Added a default request timeout to OpenAI-compatible model discovery to prevent stalled provider endpoints from hanging startup indefinitely.
- Fixed Anthropic cache-write pricing to honor mixed 5-minute and 1-hour TTL usage instead of charging every write at the 5-minute rate.
- Fixed Ollama Cloud DeepSeek V4 Flash (including dated/preview tags like `deepseek-v4-flash:0731`) exposing the generic `minimal`/`low`/`medium`/`high`/`xhigh` effort ladder without `max`; the `ollama-chat` transport now applies the DeepSeek effort contract (Flash → `low`/`high`/`max`, older reasoners → `high`/`max`), matching the direct API and every other host ([#8334](https://github.com/can1357/oh-my-pi/issues/8334)).
- Exposed the `low` reasoning-effort tier for DeepSeek V4 Pro on the direct API and faithful aggregator routes, matching DeepSeek's updated API contract advertising `reasoning_effort` `low`/`high`/`max` for both V4 SKUs; OpenRouter's non-Flash route still exposes only `high`, and the older V3.x/R1 reasoners remain `high`/`max` ([#8405](https://github.com/can1357/oh-my-pi/issues/8405)).
- Bounded OpenAI-compatible model discovery with a default request timeout so a stalled provider `/models` endpoint can no longer hang startup indefinitely in `resolveModelDiscoveryFallback` ([#8315](https://github.com/can1357/oh-my-pi/issues/8315)).
- Fixed Codex-discovered `gpt-daybreak-*` aliases being treated as unknown models, restoring the GPT-5.6 `low`/`medium`/`high`/`xhigh`/`max` effort ladder and its 372K fallback only when the Codex registry omits `context_window`.
- Fixed first-party OpenAI GPT-5.6 aliases to preserve wire-level `off` through generated pro aliases and to price requests above 272K input at each SKU's documented long-context rates.

#### Module: `@oh-my-pi/coding-agent`

##### **Breaking Changes**
- Removed the global `advisor.subagents` setting. Subagent advisors are now configured per agent via frontmatter or `task.agentAdvisor`. Existing configurations of `advisor.subagents: true` will automatically migrate to `task.agentAdvisor: { task: "on" }`.

##### **Added**
- Added Astral `ty` as a built-in fallback Python LSP server (`ty server`), ordered behind `pyright`, `basedpyright`, and `pylsp`.
- Added first-party Nix support, including reproducible source builds for Linux and macOS, a pinned development shell, NixOS and Home Manager modules, and offline Bun dependency support.
- Added support for per-agent advisors configured via the `advisor` frontmatter field or the `task.agentAdvisor` settings, allowing different agents to be advised by different models.
- Redesigned the `/agents` interface as a fullscreen hub featuring a scope sidebar, type-to-filter search, a pinned detail pane, mouse support, and interactive property chips for configuring agent settings.
- Prepared for the upcoming npm package rename by updating `omp update` and startup version checks to follow the `omp.rename` pointer in the published manifest.

##### **Changed**
- Updated `/usage`, `omp usage`, and the status line to display authoritative OpenCode Go quota usage directly from the official endpoint, replacing estimated costs with actual usage across three time windows (5h, 7d, and monthly).
- Documented the source-available local protocol relay and clarified that production collaboration relay binaries are not currently published.
- Enabled bounded Anthropic prompt-cache refreshes for the main agent loop while isolating advisor and side-channel requests from the shared refresh timer.

##### **Fixed**
- Fixed multiple Language Server Protocol (LSP) issues, including concurrent sessions sharing backend overlays, stale document overlays after workspace edits, incorrect transactional edit advertisements, unhandled snippet placeholders in rust-analyzer, and failing to restore overwritten targets during failed file renames.
- Fixed LSP `diagnostics` incorrectly reporting success when all language servers failed.
- Fixed Hindsight memory scoping splitting repositories across multiple scopes on case-sensitive filesystems by lowercasing the project label.
- Fixed the CLI crashing at startup with a raw `AuthBrokerError` when the configured auth broker is unreachable, replacing it with an actionable error message.
- Fixed various resource and process leaks, including idle launch brokers staying alive indefinitely, stale MCP connections leaving child processes open, and undrained stdout in DAP `runInTerminal` requests.
- Fixed custom STB-backed vision providers failing to decode WebP images by automatically detecting image formats from bytes and normalizing WebP blocks.
- Fixed command-backed provider API keys (`!command`) staying pinned to cached values after receiving an HTTP 401 error.
- Fixed the `/agents` Control Center failing to open when model overrides are configured as YAML arrays.
- Fixed session-title generation regressions by restoring plain-sentence phrasing and name-fidelity instructions.
- Fixed agent-facing prompts and system instructions mentioning tools that are absent from the current session catalog.
- Fixed manual `/shake` discarding all tool results; it now retains a small recent tail of results to preserve active working context.
- Fixed `omp install` failing validation for extensions importing legacy `is<Tool>ToolResult` event guards.
- Fixed profile aliases generated by standalone binaries invoking Bun's embedded virtual script instead of the installed `omp` command.
- Fixed `/skill:<name>` tokens in `/plan` or `/vibe` inline prompts being treated as literal text instead of executing the skill.
- Fixed long streaming `write` previews stalling the TUI by optimizing file scanning and splitting.
- Fixed the Windows console disappearing when running commands like `/stats`.
- Fixed retry-fallback selection switching to a fallback model with a context window too small to hold the current session context.
- Fixed OpenCode discovery ignoring `opencode.jsonc` files and rejecting comments in `opencode.json`.
- Fixed WSL2 startup hanging forever when the Windows interop pipe is wedged: the WSL host-home discovery probes (`cmd.exe`, `wslpath`) now run under a 500ms hard timeout and fall back to the Linux `$HOME`/`~/.omp` candidates ([#8402](https://github.com/can1357/oh-my-pi/issues/8402)).

#### Module: `@oh-my-pi/hashline`

##### **Fixed**
- Repaired mis-set replacement ranges using exact outside-row matches, indentation, tree-sitter structure, and a narrow pure-closer shape: opening comment fences and other syntax-essential edges are retained only when a parse-valid candidate satisfies those constraints; ambiguous placements are rejected.

#### Module: `@oh-my-pi/natives`

##### **Fixed**
- Fixed an issue where shell-internal background jobs (such as `yes >/dev/null &`) could survive a one-shot shell session and consume CPU indefinitely after the command returned.

#### Module: `@oh-my-pi/omptype`

##### **Added**
- Added `type.withJsonSchema(schema, json)` to wrap a validation-only schema, ensuring JSON Schema emission yields the provided `json` verbatim even when nested inside objects, arrays, or unions. Schemas with defaults or output-changing morphs are rejected to prevent transformed outputs from being discarded.

#### Module: `@oh-my-pi/stats`

##### **Added**
- Added cost-weighted `cacheSavings` metric alongside `cacheRate`, accounting for cache-read discounts and write premiums against equivalent uncached prompt costs.

##### **Fixed**
- Ensured the embedded dashboard archive is byte-reproducible by sorting entries and zeroing tar and gzip timestamps during compilation.

#### Module: `@oh-my-pi/tui`

##### **Fixed**
- Fixed an issue where repeated pane-width adjustments or terminal resizing could corrupt native scrollback and soft-wrap behavior.
- Fixed an issue where scaled OSC 66 Markdown headings (such as "Large Headings" on Kitty) would render as invisible placeholders or get partially cleared after a redraw or terminal resize.

#### Module: `@oh-my-pi/utils`

##### **Fixed**
- Optimized performance of partial JSON parsing for long streaming tool-call arguments.
- Fixed Mermaid ASCII multi-word edge labels where routed lines would show through spaces.

---

### 🚀 Release `v17.3.1` (2026-08-13)

#### Module: `@oh-my-pi/catalog`

##### **Added**
- Added dynamic Antigravity and Gemini CLI discovery support for Gemini 3.7 Flash, with low/medium/high thinking-level routing.

##### **Changed**
- Updated model metadata, context windows, pricing, and configurations in the catalog

#### Module: `@oh-my-pi/coding-agent`

##### **Fixed**
- Fixed Claude Code user discovery ignoring CLAUDE_CONFIG_DIR for configuration, plugins, MCP servers, and imported sessions.
- Fixed the status-line git branch display freezing after switching branches.
- Fixed Pi extension contexts omitting the runtime mode, which caused TUI guards to silently disable extension UI.
- Fixed extension-registered tool names being rejected by the --tools flag before extension discovery, which prevented least-privilege sessions from allowlisting plugin tools.
- Fixed omp plugin install failing with cloning errors for legacy Pi extensions whose tool schemas use legacy-typebox builders.
- Fixed omp update aborting with chmod ENOENT when concurrent update runs overlapped by using unique download temporary paths.
- Fixed the browser tool executable probe launching the user's installed GUI Chromium on Windows: the `--version` version probe from ecb22957 was Linux-scoped but ran for every platform candidate, so on Windows it could hand off to a running `chrome.exe`, open a normal browser window, then reject the candidate and fall back to cached Chrome for Testing. The probe is now confined to Linux ([#8445](https://github.com/can1357/oh-my-pi/issues/8445)).

#### Module: `@oh-my-pi/natives`

##### **Fixed**
- Fixed `omp` failing to start on a clean Windows install with `Failed to load pi_natives native addon for win32-x64 ... The specified module could not be found` (LoadLibrary error 126). The shipped win32-x64 addon linked the dynamic MSVC CRT (`/MD`) and imported `VCRUNTIME140.dll` from the Visual C++ Redistributable, which is absent on a fresh Windows install. The addon now statically links the CRT (`+crt-static` for rustc plus the `static_link_msvcrt` cc feature for its C dependencies), so the `.node` imports only core Windows system DLLs ([#8439](https://github.com/can1357/oh-my-pi/issues/8439)).

#### Module: `@oh-my-pi/omptype`

##### **Fixed**
- Fixed TypeBox adapter omitting pattern, non-URL format, and multipleOf constraints from the emitted JSON Schema.

#### Module: `@oh-my-pi/tui`

##### **Fixed**
- Fixed screen flashing in Herdr panes during transcript streaming.

---

### 🚀 Release `v17.3.2` (2026-08-14)

#### Module: `@oh-my-pi/ai`

##### **Fixed**
- Dropped unsigned thinking blocks from Antigravity Claude requests instead of sending them without a signature, preventing HTTP 400 responses when resuming sessions or switching models.
- Classified Antigravity HTTP 429 responses from structured `google.rpc.ErrorInfo` reasons (`QUOTA_EXHAUSTED`, `RATE_LIMIT_EXCEEDED`, and `INSUFFICIENT_G1_CREDITS_BALANCE`), using retry delays of five minutes or longer to distinguish rotatable quota windows from transient throttling instead of relying only on message regexes.

##### **Removed**
- Removed the Antigravity identity-prompt injection (`ANTIGRAVITY_SYSTEM_INSTRUCTION` and `shouldInjectAntigravitySystemInstruction`): Cloud Code Assist accepts arbitrary system instructions on gemini-3.x and Claude routes (verified live), and the injected stub never matched the real client's system prompt anyway. User system prompts are now sent unmodified (still tagged `role: "user"`).
- Fixed Antigravity `auto` mode not failing over to the sandbox endpoint when the daily endpoint returned a thinking-only `STOP`, which caused Advisor turns to be falsely recorded as empty-response failures ([#8480](https://github.com/can1357/oh-my-pi/issues/8480)).

#### Module: `@oh-my-pi/catalog`

##### **Added**
- Added support for the `deepseek-v4-pro:preview` model
- Added support for the `gemini-3.7-flash` model
- Added dynamic Antigravity client-version discovery from the official update manifest (darwin/arm64 channel), so version-gated models appear without a code change; `PI_AI_ANTIGRAVITY_VERSION` remains available as an override.

##### **Fixed**
- Fixed Antigravity discovery missing Gemini 3.7 Flash: Cloud Code Assist gates newer models on the client version in the `User-Agent`, and the pinned `antigravity/hub/2.1.4` was too old. The user-agent now matches the captured 2.8.0 client format (`antigravity/hub/2.8.0 (aidev_client; os_type=darwin; arch=arm64; cl=963137146)`); os_type/arch stay pinned to the darwin/arm64 reference client. Overridable via `PI_AI_ANTIGRAVITY_VERSION` / `PI_AI_ANTIGRAVITY_CL` / `PI_AI_ANTIGRAVITY_OS` / `PI_AI_ANTIGRAVITY_ARCH`.

##### **Removed**
- Removed `ANTIGRAVITY_SYSTEM_INSTRUCTION` from `wire/gemini-headers`; the Antigravity transport and web search no longer inject a fake identity prompt.

#### Module: `@oh-my-pi/coding-agent`

##### **Fixed**
- Fixed the parent TUI stalling after a subagent submits its result until terminal focus or resize wakes the event loop ([#8462](https://github.com/can1357/oh-my-pi/issues/8462)).
- Fixed `omp update` misclassifying foreign npm/bun bin aliases while preserving package-manager ownership for globally linked checkouts ([#8468](https://github.com/can1357/oh-my-pi/issues/8468)).
- Fixed `read` hashline headers collapsing nested in-workspace paths to the bare basename, which let a same-basename file at the session cwd capture a verbatim follow-up `edit` and deterministically reject it with `hash is not from this session`. Headers now retain the workspace-relative path (e.g. `[src/settings.json#0063]`) ([#8482](https://github.com/can1357/oh-my-pi/issues/8482)).

#### Module: `@oh-my-pi/utils`

##### **Fixed**
- Fixed `fetchWithRetry()` aborts during retry backoff to preserve the documented `"Request was aborted"` error contract ([#8450](https://github.com/can1357/oh-my-pi/issues/8450)).

---

### 🚀 Release `v17.3.3` (2026-08-14)

#### Module: `@oh-my-pi/ai`

##### **Fixed**
- Distinguished Gemini thought-only `STOP` responses from empty transports, avoiding repeated identical reasoning requests and duplicate Antigravity endpoint streams while surfacing the missing final output for session-level recovery.

#### Module: `@oh-my-pi/coding-agent`

##### **Fixed**
- Automatically continued Gemini turns that stopped after thinking without final output, using a bounded final-answer reminder instead of exhausting generic retries.
- Retried Gemini `MALFORMED_FUNCTION_CALL` failures when every emitted tool call was proven unexecuted, while preserving real tool-result and visible-output replay guards.
- Kept current terminal retry errors in one pinned banner with attempt context while surfacing local continuation failures instead of stale provider errors.

#### Module: `@oh-my-pi/hashline`

##### **Fixed**
- Recovered dangling range separators in hunk headers (`PUT 244.=:`, `CUT 5.=`) as single-line ranges (`N.=N`) instead of rejecting the header as an orphan payload line.
- Recovered dangling range separators in hunk headers (`PUT 244.=:`, `CUT 5.=`) as single-line ranges (`N.=N`) instead of rejecting the header as an orphan payload line.

#### Module: `@oh-my-pi/tui`

##### **Fixed**
- Fixed Gemini reports rendering their final headings and tables as one raw code block when the model emitted a lone closing Markdown fence without its opener.

---

### 🚀 Release `v17.3.4` (2026-08-14)

#### Module: `@oh-my-pi/agent`

##### **Fixed**
- Fixed Codex-compatible V2 remote compaction with an explicit `v2Endpoint` by sending the required feature-negotiation header ([#8524](https://github.com/can1357/oh-my-pi/issues/8524)).

#### Module: `@oh-my-pi/ai`

##### **Fixed**
- Fixed `omp usage invalidate` to discard stale OAuth and API-key usage snapshots, then force a cache-bypassing, per-provider serialized refresh with a broker request budget sized for the full unfiltered account batch, so upgraded subscriptions do not silently retain pre-change quota data.
- Fixed quota reporting and Cookie capture guidance for China (Beijing) Alibaba Token Plan credentials ([#8509](https://github.com/can1357/oh-my-pi/issues/8509)).

#### Module: `@oh-my-pi/catalog`

##### **Added**
- Added wire constants for Codex V2 remote-compaction feature negotiation.

##### **Fixed**
- Fixed raw `COPILOT_GITHUB_TOKEN` credentials skipping plan-specific endpoint discovery, which routed GitHub Copilot Business model requests to the personal endpoint and returned HTTP 403. The GitHub Copilot model cache is now scoped per credential, so switching the token no longer serves another account's stale endpoint for the cache TTL ([#8507](https://github.com/can1357/oh-my-pi/issues/8507)).
- Fixed the OpenRouter `deepseek/deepseek-v4-pro-0813` route silently clamping the reasoning effort to `high`: the dated SKU advertises (and accepts) the wire-exact `low`/`high`/`max` ladder, so its effort override no longer collapses to `high`-only. The undated `deepseek/deepseek-v4-pro` OpenRouter route stays `high`-only. ([#8517](https://github.com/can1357/oh-my-pi/issues/8517))

#### Module: `@oh-my-pi/coding-agent`

##### **Changed**
- Replaced the MuPDF-WASM PDF document backend with `pdf-inspector` through `@oh-my-pi/pi-natives`, preserving cached text conversion and PDF line selectors while reporting pages that need OCR.
- Restored `read <pdf>:` and `read <pdf>:<image>.png` page rendering by automatically capturing PDF pages through the headless Chromium browser tool.

##### **Fixed**
- Fixed Streamable HTTP MCP sessions being invalidated by opening the optional GET SSE stream before sending `notifications/initialized`, which prevented Figma Dev Mode MCP from connecting ([#8514](https://github.com/can1357/oh-my-pi/issues/8514)).
- Fixed the `/hotkeys` table describing Ctrl+D (`app.exit`) as "Exit (when editor is empty)" when it actually exits unconditionally and saves the current prompt as a resumable draft ([#8530](https://github.com/can1357/oh-my-pi/issues/8530)).
- Fixed Ctrl+G external editors failing to launch on Windows because Bun re-quoted the embedded `cmd.exe /c` command line ([#8544](https://github.com/can1357/oh-my-pi/issues/8544)).

#### Module: `@oh-my-pi/mnemopi`

##### **Fixed**
- Fixed `recall()` silently dropping `scope='global'` rows whenever a `channelId` filter was active: `buildWhere()` appended a redundant hard `channel_id = ?` clause on top of the `(session_id = ? OR scope = 'global' OR channel_id = ?)` visibility clause, so global rows whose `channel_id` didn't match (e.g. imported rows with `channel_id NULL`) were excluded. Channel isolation is preserved by the visibility clause alone. This made imported/global episodic memory permanently unrecallable through callers that always pass a channel (such as the coding-agent memory backend). ([#8525](https://github.com/can1357/oh-my-pi/issues/8525))

#### Module: `@oh-my-pi/natives`

##### **Added**
- Added the async `pdfToMarkdown` native API backed by `pdf-inspector`, with page numbering, page-count, OCR-needed-page, and encoding-issue metadata.

##### **Changed**
- Docker images (`Dockerfile`, `scripts/install-tests/*.dockerfile`) build the native addon through the cargo/napi-rs backend (`OMP_NATIVE_BUILD_BACKEND=cargo`) instead of Bazel: a single fixed host target gains nothing from hermetic cross toolchains, and none of those images shipped bazelisk. `OMP_NATIVE_CARGO_PROFILE` picks the profile for that path (images use `ci`, local default stays `local`).

##### **Fixed**
- Fixed the root Cargo workspace failing to load when a stale directory exists under `crates/` — e.g. a deleted crate whose directory survived `git reset --hard`. `members` no longer globs `crates/pi-*`, so a directory without a `Cargo.toml` can no longer break every cargo and Bazel build.
- Fixed Docker build contexts shipping nested build output: `.dockerignore` patterns are anchored at the context root, so bare `target/` and `dist/` matched neither `go-port/*/target` (~1.4 GB) nor `packages/*/dist` (~600 MB).
- Fixed `deviceCheckGenerateToken` aborting the whole process with `SIGTRAP` when called from a macOS session without GUI/graphic access (SSH, a launchd `LaunchDaemon`, a CI runner, a service account, a sandbox), which made every `openai-codex/*` OAuth model unusable for such accounts. `-[DCDevice isSupported]` synchronously opens an XPC connection to the per-user DeviceCheck metadata daemon, which exists only in an interactive GUI login session; without one the connection setup hits `_xpc_api_misuse` and traps before any completion handler runs, so the promise never rejects. The binding now checks the caller's security session for the `sessionHasGraphicAccess` attribute first and resolves `{ supported: false, error: … }` instead of touching DeviceCheck when it is absent ([#8353](https://github.com/can1357/oh-my-pi/issues/8353)).

#### Module: `@oh-my-pi/tui`

##### **Fixed**
- Fixed a terminal Device-Attributes reply leaking into the composer as literal text (e.g. `1;22;…;52c`) when it arrived after the startup capability-probe sentinel FIFO drained, a race made observable by the added latency of an SSH/zmx PTY chain. DA1 replies (`CSI ? … c`) and split private-CSI responses are now consumed for the whole session lifetime, not only while a probe sentinel is outstanding ([#8542](https://github.com/can1357/oh-my-pi/issues/8542)).

---

### 🚀 Release `v17.3.5` (2026-08-16)

#### Module: `@oh-my-pi/agent`

##### **Added**
- Added automatic retry support for transient provider failures during one-shot completions, allowing callers such as compaction to opt in to resilient request handling.

##### **Fixed**
- Fixed /handoff, branch summarization, and manual /compact failing outright on transient provider errors (e.g. Anthropic overloaded/429/529 responses); these operations now retry automatically instead of leaving the user's context full.

#### Module: `@oh-my-pi/ai`

##### **Added**
- Added retryable oneshot completion support (`retryTransientCompletion`) so non-agent LLM calls correctly retry on transient provider failures (Anthropic overload/rate-limit errors, HTTP 429/500/502/503/529), honoring provider-supplied retry-after timing before giving up.

##### **Fixed**
- Fixed xAI availability detection so paid-key-only setups correctly default to `xai/grok-4.5` instead of the free SuperGrok catalog; explicit `xai-oauth/…` selectors still work as before.
- Fixed xAI Responses requests sending unsupported parameters (reasoning summary, presence/frequency penalties) that some models rejected.
- Fixed Umans usage reporting incorrectly marking quota as exhausted based on raw request counts instead of actual weighted usage, and improved the usage display to show both a soft-cap warning and a hard exhaustion limit with an accurate countdown to reset.
- Fixed `omp usage invalidate` to fully clear stale usage data and force a fresh refresh, so upgraded subscriptions no longer show outdated quota information.
- Improved session recovery to correctly treat certain Cursor HTTP/2 connection errors as transient instead of ending the session.
- Fixed OpenAI-compatible streams (e.g. DeepSeek) that are cut off mid-generation being silently treated as a completed response instead of being retried.
- Fixed DeepSeek resource-exhaustion interruptions not being automatically retried.
- Fixed tool-call IDs being lost during same-model replay, which could break correlation with custom gateways.
- Fixed Kimi Code multi-account routing to prefer accounts with more available quota, respect usage-limit cooldowns, and keep consistent usage history across token refreshes.
- Fixed Anthropic custom signing-proxy conversations losing tool-search results and thinking content during replay.
- Fixed rare runaway response loops across model providers so they now fail gracefully instead of repeating indefinitely.
- Fixed xAI rejecting entire turns due to certain MCP tool schema shapes, restoring compatibility while isolating any remaining incompatible tools rather than failing the whole request.
- Fixed Alibaba DashScope/Bailian transient per-minute rate limits being misclassified as full quota exhaustion, causing unnecessary long backoffs instead of quick retries.
- Fixed Anthropic-compatible streams dropping thinking content, which broke replay of prior reasoning.
- Updated the Alibaba Coding Plan China login flow to point to the current Bailian API-key management console.

#### Module: `@oh-my-pi/catalog`

##### **Added**
- Added support for GLM-5.3 on the z.AI provider, featuring a unified low/high/max reasoning-effort ladder across all hosts, mandatory thinking mode, 1M context, and default-model status for the z.AI provider.

##### **Changed**
- Switched the paid xAI provider (xai / XAI_API_KEY) from Chat Completions to the OpenAI Responses API, aligning it with SuperGrok (xai-oauth) for prompt-cache affinity, reasoning-effort handling, and encrypted-reasoning replay.
- Changed the paid xAI (XAI_API_KEY) default model to grok-4.5.
- Changed the SuperGrok (xai-oauth) default model to grok-4.5.
- Improved reasoning continuity for xAI models by requesting and replaying encrypted reasoning content across multi-turn Responses API calls.

##### **Fixed**
- Fixed Codex Daybreak Blue and Red model discovery reporting zero token prices, which incorrectly labeled the models as free in the model picker.
- Fixed Baseten's moonshotai/Kimi-K3 catalog metadata so its low/high/max thinking levels are available.
- Fixed opencode-go/deepseek-v4-flash Responses requests sending forced named tool_choice selectors that are rejected while thinking mode is active.

#### Module: `@oh-my-pi/coding-agent`

##### **Added**
- Added Extensions tab group to settings schema

##### **Changed**
- Routed paid xAI models (XAI_API_KEY / xai/…) through the Responses API used by SuperGrok OAuth instead of Chat Completions, including reliable replay of encrypted reasoning content on follow-up turns.
- Updated the default model for XAI_API_KEY (xai) to grok-4.5, and the default SuperGrok OAuth (xai-oauth) model to grok-4.5. Automatic model selection continues to prefer paid xai/grok-4.5 when only XAI_API_KEY is set, with xai-oauth/grok-4.5 still available explicitly.
- Stopped sending presence/frequency penalties and stop sequences to xAI reasoning models such as grok-4.5, which reject them.

##### **Fixed**
- Fixed `hub` job and wait lists hiding stale running subagent registrations that have no turn in flight, ensuring they remain visible so operators can cancel them
- Fixed external thinking scratchpads running alongside native reasoning on xAI Grok 4 and other reasoning-only Responses models that reject `reasoning.effort`
- Fixed llama.cpp model discovery producing a baseUrl without the /v1 prefix for non-Qwen models, causing 404 errors on OpenAI-compatible endpoints.
- Fixed prompt caching on open-weight providers (DeepSeek, Qwen, GLM, …) so tool schemas stay cached across directory changes and midnight rollovers.
- Fixed omp --fork omitting the source session's artifact directory, so CLI-created forks now preserve artifact:// references like interactive /fork.
- Fixed long ask option labels being hard-truncated at the terminal width; labels now wrap onto indented continuation lines.
- Fixed toggling display.showTokenUsage from /settings leaving existing token-usage rows stale until the transcript was rebuilt.
- Fixed mid-run auto-compaction blocking the live loop while waiting on extension handlers, which could hang after a snapcompact or context-full pass.
- Reduced peak memory for persisted subagent revival probes by streaming large file-backed session journals instead of loading them fully.
- Improved responsiveness of streaming edit previews for large diffs by rendering only the visible tail.
- Fixed repeated /btw panels committing transient frames to native scrollback and replaying conversation history after dismissal.
- Clarified that closing browser tool sessions releases managed handles without closing pages in spawned, CDP-connected, or relay browsers.
- Fixed interrupted vibe_wait calls being reported as elapsed timeout windows.
- Improved checkpoint/rewind prompt rendering to stay accurate after a rewind and be more concise.
- Fixed Cursor turns dying with HTTP/2 stream errors (NGHTTP2_INTERNAL_ERROR / NGHTTP2_REFUSED_STREAM) after tool calls already had results, instead of leaving the agent idle until the user typed "continue".
- Fixed mixed-case plugin tool names being lowercased during tool-set refresh, which unmounted them from xd:// whenever MCP tools connected.
- Fixed Exa MCP servers being unmounted when their config explicitly requests tools the native Exa integration does not provide, breaking /mcp reconnect exa.
- Fixed Claude Code custom tool discovery attempting to import non-module files from .claude/tools.
- Fixed Agent Hub parking a mid-spawn child session so subsequent task calls failed with an ownership error and the row could never be revived.
- Fixed the welcome banner displaying a stale model name when the session's active model changes after startup (e.g. after a delayed config load or an explicit /model switch).
- Fixed Nix standalone binaries retaining Bun's build-time package in their runtime closure.
- Fixed birch user/custom message card contrast on dark terminals, where chat bubbles could render light-on-light.
- Fixed hidden tool snapshots preventing long streamed assistant responses from entering terminal scrollback.
- Prevented omp models from loading ambient hook factories while preserving extension-contributed providers.
- Fixed the ask dialog's multi-select mode dead-ending on Enter; Space now toggles options and Enter submits the current selection.
- Fixed workspace diagnostics reporting a clean workspace when its checker crashed without producing output.
- Fixed manual /compact failing outright when a summarization request hit a transient provider overload.
- Fixed transient Anthropic failures (overloaded_error, rate_limit_error, 429/500/502/503/529) aborting or silently degrading side-effect-free background LLM calls such as session title generation, TTS speech enhancement, commit-message generation, thinking/stop classifiers, memory extraction/consolidation, and commit analysis/summary/changelog passes; these now retry with backoff honoring retry-after instead of failing or returning an indistinguishable empty result.
- Fixed the shared headless browser daemon launching from the macOS system Google Chrome bundle, which could cause macOS to route the user's link clicks to the automation daemon and silently swallow them; the daemon now prefers an isolated Chrome for Testing binary on macOS.
- Reclaimed abandoned daemon runtime directories under ~/.omp/run/daemons/, preventing unbounded growth of leftover Chromium profiles and broker state.
- Kept the welcome screen's Tips, LSP Servers, and Recent sessions visible when a long model name still leaves enough terminal width for both columns.
- Fixed focused shimmer animation frames (ultrathink, orchestrate, workflowz) repainting the full TUI too frequently, causing high CPU usage while composing prompts on WSL2.
- Fixed the /debug report bundle including unrelated historic sessions, leaking other sessions' files and bloating archives.
- Fixed adopted keep-alive agents remaining stuck in a running state in the registry after deferred turn settlement, and prevented stale refs from sustaining bare hub wait calls indefinitely.
- Fixed home-relative marketplace catalog paths not being expanded before cache access, preventing updates from writing into a literal ~ directory.
- Fixed broker-owned headless Chromium opening and retaining an unowned blank foreground window on Windows.
- Fixed the auto thinking classifier failing every turn on Anthropic models served through LiteLLM/Vertex due to a thinking-budget mismatch.
- Fixed always-ask approval prompts bypassing edit preview readiness when a built-in tool executes under its wire-level alias, such as edit running as apply_patch.
- Fixed lsp reload crashing non-rust-analyzer language servers by sending them a rust-analyzer-specific request; that request is now gated to rust-analyzer only.
- Fixed browser open failing with "Shared browser daemon unavailable" when HTTP_PROXY/HTTPS_PROXY is set, because liveness probes were incorrectly routed through the proxy.
- Fixed defaultThinkingLevel: auto skipping classification for user-invoked /skill:<name> turns, leaving the effort stuck on pending auto.
- Fixed custom-tool directory discovery recursing into subtrees despite a non-recursive default, which could crash startup when scanning large dependency directories such as Python venvs.
- Repaired torn session JSONL appends after disk-write failures, rewrote malformed resumed files before their next append, retried transient persistence failures, and surfaced failures in the TUI.
- Prevented Anthropic model fallback from replaying model-bound thinking blocks across models, and surfaced immutable-thinking errors without retrying the unchanged invalid turn.
- Fixed empty-stop failure messages always suggesting a context problem even when the provider billed output tokens; the message now reports the billed token count and points at a provider-side filter/translation issue when appropriate.
- Fixed a parked, session-less agent-registry entry with no reviver permanently poisoning its agent id, preventing fresh subagent spawns from reusing that id.
- Made extension tool-call timeouts configurable and paused them during user dialogs.
- Fixed /vibe cancellation leaving an in-flight model turn unaware that Vibe mode and its tools were removed.
- Fixed empty local-model stops lingering on the persisted active branch after retries, preventing them from resurfacing after reload or a mid-retry process kill.
- Fixed the Biome linter client silently dropping every diagnostic due to an outdated JSON output schema; it now supports Biome 2.x's diagnostic format.
- Fixed `hub jobs` and empty `hub wait` snapshots hiding running subagents that have no live turn, which removed the only way to discover and `hub cancel` a stale registration; such agents are listed again and flagged as having no turn in flight.
- Fixed external thinking being offered on xAI reasoning-only Responses models (grok-4 family) that reject `reasoning.effort`, where the private scratchpad ran alongside native reasoning instead of replacing it.
- Fixed the extension tool-call handler timeout rendering outside a titled section in `/settings` by registering its Extensions group on the Tools tab.

#### Module: `@oh-my-pi/mnemopi`

##### **Fixed**
- Fixed an issue where transient provider failures (such as Anthropic overload or rate limit errors) were incorrectly treated as empty responses; these failures are now retried automatically before falling back.

#### Module: `@oh-my-pi/natives`

##### **Fixed**
- Fixed the native `xargs` builtin panicking in `-I`/`-i` replace mode when stdin is empty; it now exits successfully without running the command, matching GNU behavior.
- Fixed inline-code foreground color incorrectly carrying into plain text when a Markdown codespan ended exactly at a soft-wrap boundary.
- Fixed `wrapTextWithAnsi` leaving a trailing space plus a stray underline open/close pair on the line above a soft wrap when a style opened immediately after that space (e.g. `read this thread <underline>https://…`), a regression from the codespan color-bleed fix: only sequences that follow visible content now ride along with the current token, while sequences after whitespace still wait for the token they style.

#### Module: `@oh-my-pi/tui`

##### **Fixed**
- Fixed long CPU-bound event-loop stalls being misclassified as system sleep and omitted from loop-blocked diagnostics.
- Fixed focused components with markers falling back to full-screen redraws instead of direct row updates, preserving cursor position and native scrollback across marker changes.

#### Module: `@oh-my-pi/utils`

##### **Fixed**
- Fixed the Markdown renderer incorrectly breaking into a raw code block when a 4-space-indented line (such as a box-drawing tree child under a └── branch) directly followed paragraph text; it now correctly stays part of the paragraph, matching standard Markdown behavior.

---

### 🚀 Release `v17.3.6` (2026-08-17)

#### Module: `@oh-my-pi/catalog`

##### **Changed**
- Changed the paid xAI (XAI_API_KEY) and SuperGrok (xai-oauth) default models to grok-4.6.

##### **Fixed**
- Raised the GPT-5.6 Sol/Terra/Luna context window on the Codex transport (openai-codex) from 372K to 1M tokens: OpenAI enabled the 1M window for subscription Codex on 2026-08-16, but the Codex model registry still reports the stale 272,000, so discovery now floors these SKUs at 1,000,000 instead of trusting the reported value ([openai/codex#38917](https://github.com/openai/codex/issues/38917)).

#### Module: `@oh-my-pi/coding-agent`

##### **Added**
- Added `ExtensionAPI.registerFileWriteFallback(handler)` and `ExtensionAPI.registerFileDeleteFallback(handler)`, letting an extension supply a fallback writer or deleter that is consulted when a native `write`, `edit`, or `apply_patch` byte-write or unlink is denied with a permission error (`EPERM`/`EACCES`/`EROFS`) — for hosts that embed the agent inside a sandbox that denies direct filesystem access but exposes a privileged channel. The brokered path is symlink-resolved so a handler's allowlist sees the real destination, a destination that cannot be resolved is not brokered at all, and `req.sessionId` names the session that issued the mutation so a handler sharing the process-wide registry can enforce policy per session. See [`docs/extensions.md`](../../docs/extensions.md).

##### **Changed**
- Updated the default model for XAI_API_KEY (xai) and SuperGrok OAuth (xai-oauth) to grok-4.6. Automatic model selection continues to prefer paid xai/grok-4.6 when only XAI_API_KEY is set, with xai-oauth/grok-4.6 still available explicitly.

##### **Fixed**
- Fixed `omp stats` and `/stats` dashboards being unreachable from container hosts by accepting an explicit `--host` bind address while preserving the `127.0.0.1` default.

#### Module: `@oh-my-pi/stats`

##### **Fixed**
- Fixed the stats dashboard being unreachable from container hosts by accepting an explicit `--host` bind address while preserving loopback-only binding and same-origin API access by default.

---

### 🚀 Release `v17.3.7` (2026-08-18)

#### Module: `@oh-my-pi/ai`

##### **Changed**
- Send the `omp/<version>` User-Agent on xAI chat (`xai` and `xai-oauth`) unless the request already set its own.

#### Module: `@oh-my-pi/coding-agent`

##### **Changed**
- Send the `omp/<version>` User-Agent on xAI chat (`xai` and `xai-oauth`) unless the request already set its own ([#8840](https://github.com/can1357/oh-my-pi/pull/8840) by [@Jaaneek](https://github.com/Jaaneek)).

---

### 🚀 Release `v17.3.8` (2026-08-19)

#### Module: `@oh-my-pi/agent`

##### **Fixed**
- Fixed `/compact` (and automatic compaction) resurrecting pre-`/clear` conversation turns: `prepareCompaction` now honors the latest `reset_boundary`, so a compaction after an in-place `/clear` only summarizes messages created after the reset ([#8718](https://github.com/can1357/oh-my-pi/issues/8718)).
- Hardened compaction summarization against prompt injection: conversation history and previous summaries are now treated as untrusted, and embedded `<conversation>`/`<previous-summary>` boundary tags are neutralized before prompt assembly ([#8727](https://github.com/can1357/oh-my-pi/pull/8727) by [@koopmannleon19977-cmyk](https://github.com/koopmannleon19977-cmyk)).
- Compaction summarization input is now bounded to the summary model's context (windowed fold for oversized spans) and deterministic context-overflow 400s are no longer retried up to the full retry budget; artifact ids containing `503` no longer misclassify hard 400s as transient.
- Fixed remote compaction mirroring the #8789 Responses shape: `buildOpenAiNativeHistory` now hoists an assistant `message` wedged between a tool-call batch and its outputs ahead of the batch, so compaction requests to strict opencode-go gateways match the canonical `message(s) → calls → outputs` order ([#8789](https://github.com/can1357/oh-my-pi/issues/8789)).

#### Module: `@oh-my-pi/ai`

##### **Changed**
- Fixed Gemini thought summaries occasionally leaking a raw `` ```thinking `` / `` ``````thinking `` fence delimiter into the reasoning block, so it no longer shows up as fence spam in the thinking display or persisted transcripts ([#8719](https://github.com/can1357/oh-my-pi/issues/8719)).
- Fixed the OpenCode Go login prompting for an "OpenCode Zen API key": the shared login flow now names the provider you selected, so connecting OpenCode Go asks for an OpenCode Go key (the `opencode.ai/auth` console is still shared, as documented upstream) ([#8738](https://github.com/can1357/oh-my-pi/issues/8738)).
- Fixed Anthropic-compatible endpoints with strict prompt validation (e.g. Z.AI GLM `api.z.ai/api/anthropic`, which rejects the whole request with `400 code 1213 "The prompt parameter was not received normally"`) failing sessions once a tool returned empty output on a vision-capable model: empty successful `tool_result` blocks now encode as `content: ""` instead of `content: []`, which both the official API and strict compatible endpoints accept.
- Fixed `retry.usageReservePct` (Reserve Margin) ignoring Claude Fable/Mythos weekly tier usage until it hit 100%, so a Fable model kept serving turns past the configured reserve; reserve health now honors the mapped tier row while credential-wide hard blocks still require confirmed exhaustion ([#8773](https://github.com/can1357/oh-my-pi/issues/8773)).
- Fixed `cursor-agent` streams stalling with "Provider stream stalled while waiting for the next event" when Cursor asked the client to approve a hosted WebFetch / web search (reproduced on `cursor-grok-4.6-xhigh` after "I'll fetch the page…"). Those `interaction_query` frames — including the newer WebFetch field 9 this proto did not name — were dropped, so the server waited forever and the idle watchdog aborted a live connection. Permission queries are now answered; hosted search/fetch is approved, unnamed permission fields get an `approved` reply on the same field number, and prompts this client cannot serve are rejected so the turn can continue.

##### **Fixed**
- Fixed thinking effort selections being ignored for local Qwen 3.8+ models on llama.cpp and vLLM: the Qwen chat-completions dialects only toggled `enable_thinking`, so the chat template always reasoned at its `xhigh` default no matter which level was selected. The encoder now routes the requested effort onto the template's `reasoning_effort` kwarg (`chat_template_kwargs` for both Qwen dialects, plus the top-level field newer llama.cpp builds map natively).
- Fixed OpenAI Completions, Amazon Bedrock, and Cursor providers ignoring `onPayload` replacement payloads. The hook now transforms the actual request body sent upstream on these providers, matching the Anthropic/Gemini/OpenAI Responses replacement contract. `devin-agent` still does not fire the hook (its payload is a protobuf object).
- Fixed Codex requests failing outright when the signed-in ChatGPT account is not entitled to the requested model; the exact model denial is now classified as an account-policy error so credential rotation can reach an entitled sibling account
- Fixed Perplexity email-OTP login after its verification response renamed the encrypted session token from `token` to `challenge_token`.
- Cloud Code Assist Gemini 3.6/3.7 Flash requests at `minimal` now send `thinkingLevel: LOW` on the aliased `-low` SKU instead of `MINIMAL`, which the API rejects with HTTP 400.
- Answer Cursor `interaction_query` permission gates (hosted web search, Exa, unnamed field-9 WebFetch) so the Run RPC continues instead of sitting silent until the 300s idle watchdog.
- Fixed provider tool calls arriving with flattened array argument paths (e.g. Gemini's `questions[0].id`) being stripped and rejected by argument validation; well-formed flattened paths are now rebuilt into the nested arrays the tool schema expects ([#8886](https://github.com/can1357/oh-my-pi/issues/8886)).
- Fixed opencode-go (Console Go) rejecting Responses turns with `400 No tool output found for tool call …` (naming a random call of the batch on each retry) when a model streamed a trailing text/thinking block after its tool calls: `buildResponsesInput` emitted that block as an assistant `message` item wedged between the `function_call` batch and its `function_call_output` items. Such interleaved messages are now hoisted ahead of their call batch (canonical `message(s) → calls → outputs`), which the strict gateway validator accepts; content is unchanged ([#8789](https://github.com/can1357/oh-my-pi/issues/8789)).
- Fixed the OpenAI-wire transport sleeping on a LiteLLM concurrency-admission 429 (`rate_limit_type: max_parallel_requests`, `Retry-After: 60`) and retrying it up to 6 times (~300s) before session recovery saw the error. Because a 60s hint equals the transport's `maxDelayMs` cap, `fetchWithRetry` kept sleeping and retrying; the request now surfaces on the first attempt so `TurnRecovery`'s concurrency backoff/model fallback runs promptly. Genuine RPM/quota 429s (no such marker) still honor `Retry-After` ([#8854](https://github.com/can1357/oh-my-pi/issues/8854)).
- Fixed OAuth login (Codex `localhost:1455`, and any `localhost` callback flow) failing on hosts with IPv6 disabled at the kernel (`ipv6.disable=1`). The `::1` companion listener added in #8081 fails there with Bun's generic "Is port X in use?" message (oven-sh/bun#7187), which the in-use check misread as a real collision — tearing down the healthy IPv4 listener and surfacing a bogus "port 1455 is in use" error. The dual-bind path now detects the missing IPv6 loopback up front and serves IPv4 alone ([#8814](https://github.com/can1357/oh-my-pi/issues/8814)).

#### Module: `@oh-my-pi/catalog`

##### **Added**
- Added a Cursor variant-collapse table folding the per-effort Grok siblings (`cursor-grok-4.5` low/medium/high and `cursor-grok-4.6` low/medium/high/xhigh, plus their `-fast` service-tier lanes) into one logical model per lane with effort routing onto the live wire ids, matching Devin's `grok-4-5` collapse ([#8803](https://github.com/can1357/oh-my-pi/issues/8803)).
- Regenerated the Cursor agent protobufs to model hosted WebFetch permission queries (`interaction_query` / `interaction_response` field 9) and the matching `ToolCall` variant (field 37).

##### **Fixed**
- Fixed a physically corrupt `models.db` (`SQLITE_CORRUPT*` / `SQLITE_NOTADB`, "database disk image is malformed") permanently disabling the model cache. The shared read/write paths swallowed unrecoverable SQLite corruption as a best-effort miss and cached the broken handle, so a successful live catalog could never overwrite the corrupt cache and every later process repeated the miss — a runtime provider extension with no bundled catalog was left with only its bootstrap model. Corruption now self-heals: the cache closes the handle, quarantines `models.db`(+`-wal`/`-shm`) aside, recreates a fresh database, and retries the operation once; `SQLITE_BUSY`, permission, and unrelated errors keep their existing best-effort paths ([#8867](https://github.com/can1357/oh-my-pi/issues/8867)).
- Fixed local Qwen 3.8+ models (llama.cpp, vLLM, loopback custom providers) exposing the generic `minimal..high` thinking ladder instead of the chat template's real `low`/`medium`/`xhigh` `reasoning_effort` tiers. The derived metadata now marks thinking as mandatory (the official 3.8 template raises on `enable_thinking: false`), vLLM-served Qwen routes through the `chat_template_kwargs` dialect (top-level `enable_thinking` is ignored by vLLM), and vLLM discovery lights up the reasoning dial for Qwen 3.8+ ids its `/v1/models` endpoint reports as non-reasoning.
- Fixed `deepseek-v4-pro-0813` surfacing from Alibaba Token Plan discovery with `contextWindow`/`maxTokens` of `null`. The dated DeepSeek V4 Pro snapshot was missing from `ALIBABA_TOKEN_PLAN_DISCOVERED_MODEL_LIMITS`, so unlike its `deepseek-v4-flash-0731` sibling it fell through to unknown limits ([#8847](https://github.com/can1357/oh-my-pi/issues/8847)).
- Cloud Code Assist Gemini 3.6/3.7 Flash no longer maps user `minimal` to wire `thinkingLevel: MINIMAL` when that effort is aliased onto the `-low` SKU. The request now sends `LOW`, which those SKUs accept.
- Fixed SuperGrok (`xai-oauth`) Grok 4.6 hiding the thinking-level picker: the Responses effort-capable allowlist now includes `grok-4.6`, so `/model` can select the documented `low`/`medium`/`high`/`xhigh` ladder (`max` is rejected by api.x.ai).
- Marked CoreWeave runtime discovery as authoritative so stale bundled model ids that the endpoint no longer serves stop appearing as selectable models.
- ChatGPT Codex discovery that advertises only worker `-wm` SKUs now also registers the plain model route, so a configured `openai-codex/<model>` keeps resolving instead of fuzzy-falling-back to the `-wm` SKU some accounts reject.
- Fixed `opencode-go/muse-spark-1.2` (and `muse-spark-1.2-contributor`) failing every tool-call turn with `OpenAI completions stream closed before a finish_reason was received`. The Go gateway serves these ids only at `/zen/go/v1/responses`, but the `/zen/go/v1/models` discovery omits the `provider.npm` hint, so the resolver fell through to `openai-completions`; both ids are now pinned to `openai-responses` like `deepseek-v4-flash` ([#8957](https://github.com/can1357/oh-my-pi/issues/8957)).
- Fixed GitHub Copilot `grok-4.6` / `grok-4.6-1m` failing with HTTP 400 `unsupported_api_for_model` by routing them through the OpenAI Responses API (`/responses`) instead of `/chat/completions`, matching `grok-4.5`. Stale cached completion routes are invalidated on refresh ([#8807](https://github.com/can1357/oh-my-pi/issues/8807)).
- Fixed Cursor Grok 4.5/4.6 discovery classifying the versioned ids as non-reasoning: `GetUsableModels` ships no `thinkingDetails` and the bundled references read `reasoning: false`, so the picker hid the effort ladder. Discovery now marks `cursor-grok-<version>` ids as reasoning models (the non-reasoning `grok-code-*` ids stay out) ([#8803](https://github.com/can1357/oh-my-pi/issues/8803)).
- Fixed GMI Cloud (`gmi-cloud`) models resolved via `/v1/models` discovery surfacing with `null` context windows, zero pricing, and no reasoning/thinking metadata for every model except the bundled `deepseek-ai/DeepSeek-V4-Flash` seed. GMI's endpoint returns only bare `{id}` rows, so the mapper now recovers intrinsic capability metadata (context window, output limit, reasoning, thinking ladder) for resold open-weight models from the cross-provider canonical reference index — matching the SiliconFlow behavior — while never borrowing another provider's pricing ([#8890](https://github.com/can1357/oh-my-pi/issues/8890)).

#### Module: `@oh-my-pi/coding-agent`

##### **Added**
- Added `providers.cacheRetention` setting (`/settings` → Providers → Protocol) to control prompt-cache retention per request: `auto` keeps the provider default (Anthropic: 5m entries with idle keep-alive refreshes), `short` forces 5m, `long` restores 1h TTLs where supported and disables the keep-alive refresh loop, `none` disables prompt caching.

##### **Changed**
- The `read` tool now materializes a local text file once per invocation instead of once per consumer. A ranged read of a file within the snapshot cap previously cost four opens and three UTF-8 decodes — an 8KiB binary sniff, a streaming scan for the rendered window, a whole-file read for bracket context, and another whole-file read to hash the snapshot — with two of those readers separately normalizing line endings; whole-file reads under the structural summarizer paid a fifth read. Byte counts and truncation boundaries are now measured on the buffered bytes, so they stay exact for content that is not valid UTF-8. Files above the snapshot cap keep streaming, since nothing on that path wants the whole file. Raw reads, which skip the tree-sitter parse that documented the old cost, no longer pay for it.
- Documented that `bash.patterns` gates the `bash` tool only and does not cover a shell that `eval` can spawn via subprocess, and that closing that path needs a `tools.approval.eval` policy — noted in `docs/bash-tool-runtime.md`, `docs/approval-mode.md`, and `docs/settings.md` ([#8838](https://github.com/can1357/oh-my-pi/issues/8838)).

##### **Fixed**
- Fixed the `/btw` panel re-committing its frame to native scrollback on every update while the primary turn is still streaming: a live region that pins itself (an anchored HUD/panel such as `/btw`) no longer leaks its scrolled-off rows just because an unpinned transcript seam sits above it in the same frame ([#8793](https://github.com/can1357/oh-my-pi/issues/8793)).
- Fixed a submitted `/skill:<name>` command staying invisible in the transcript until its awaited preflight (memory recall, `before_agent_start` hooks, auto-thinking classification, pre-prompt compaction) finished, so a slow step such as a Hindsight auto-recall timeout made the command look unaccepted. Idle skill submissions now paint an optimistic row immediately — like a normal prompt — and reconcile it in place when the canonical `message_start` lands ([#8895](https://github.com/can1357/oh-my-pi/issues/8895)).
- Fixed broker-backed MCP OAuth credentials never refreshing, so remote OAuth MCP servers dropped out of `/mcp` once their access token expired under `omp auth-broker serve`. The client threw on the broker-redacted refresh sentinel instead of asking the broker to refresh, and the broker had no `mcp_oauth:*` refresh path (`POST /v1/credential/:id/refresh` answered `Unknown OAuth provider`). The client now routes redacted MCP refreshes through the broker, and the broker refreshes MCP credentials with a generic `refresh_token` grant from the credential's embedded token endpoint and client id — so the background refresher also keeps MCP tokens live ([#8933](https://github.com/can1357/oh-my-pi/issues/8933)).
- Fixed `omp commit` split-commit failing with `corrupt binary patch` when a split commit contains a binary file. `parseFileDiffs` split the captured diff on `"\ndiff --git "`, consuming the `\n` that terminates each block, and `patch.join` stripped trailing newlines — both dropped the blank line that terminates a `GIT binary patch` block, so the rebuilt patch was rejected by `git apply --binary`. Both trailing and mid-diff binary blocks now survive the parse/rebuild round-trip byte-exact ([#8899](https://github.com/can1357/oh-my-pi/issues/8899)).
- Fixed `omp update` (and other non-launch subcommands) crashing with `error: Unknown option '--cwd'` when a leading global launch flag preceded the subcommand — e.g. a shell alias/wrapper that runs `omp --cwd <dir> update`. `resolveCliArgv` hoisted the subcommand to the front but forwarded the launch-only flag into `update`'s strict `node:util.parseArgs` parser, which rejected it. Launch-global flags before a launch-shaped command (`acp`/`launch`) are still forwarded; before any other subcommand they are now stripped as inapplicable ([#8891](https://github.com/can1357/oh-my-pi/issues/8891)).
- Fixed Claude Code marketplace plugins ignoring the `enabledPlugins` switch in `~/.claude/settings.json` and `.claude/settings(.local).json`: a plugin turned off for a project no longer loads there, and a local-scope install enabled for a project loads even when its recorded `projectPath` is a different directory
- Fixed revived subagents (warm lifecycle reviver and cold persisted reviver) rebuilding the session without initializing the extension runtime, leaving every runtime action throwing `ExtensionRuntimeNotInitializedError`. An extension with a `tool_call` handler that touched a runtime action (e.g. `appendEntry`) then tripped the fail-closed gate in `emitToolCall` and blocked every tool — including the hidden `yield` — so the revived agent could neither finish nor exit and looped until killed. Both revivers now call the shared `initializeExtensions` helper, restoring runtime actions, `onError`, and the `session_start` event ([#8824](https://github.com/can1357/oh-my-pi/issues/8824)).
- Fixed `omp commit` split-commit crashing with a misleading `No diff found for <path>` when a staged binary (or any payload) pushed `git diff --cached --binary` past the 8 MiB subprocess output cap. The capture is truncated silently, so files sorting after the binary vanished from the parsed diff; the split flow now requests a complete diff and fails fast naming the real cause instead ([#8897](https://github.com/can1357/oh-my-pi/issues/8897)).
- Fixed a mid-run compaction being misread as a phantom overflow: after a compaction rebased the in-flight context snapshot, `getContextBreakdown` used message position (`anchorIndex >= cutoffCount`) as a freshness proxy, so an in-flight provider response whose request predated the compaction out-ranked the rebased estimate and reported the pre-compaction token count (~2.6x the real one). This tripped the "Compaction freed too little context to make progress" guard and drove the frame-rescue path on a byte-identical `tokensBefore`. Assistant context snapshots now carry a monotonic compaction epoch, and a post-cutoff anchor whose epoch predates the last compaction is no longer trusted over the rebased estimate ([#8887](https://github.com/can1357/oh-my-pi/issues/8887)).
- Fixed `after_provider_response` extension handlers receiving the primary session model in `ctx.model` and `ctx.models.current()` for cross-provider side requests. `ExtensionRunner.emitAfterProviderResponse` accepted the response model but discarded it, so a handler revoking a credential on an HTTP 402 could target the wrong provider. It now threads the response model into the context, matching `emitBeforeProviderRequest` ([#8955](https://github.com/can1357/oh-my-pi/issues/8955)).
- Fixed the TinyFish web search provider ignoring the `lang:`/`language:` query directive, so every request fell back to the API's US/English geolocation. `parsed.lang` now maps onto TinyFish's `location`/`language` parameters (e.g. `lang:it-it` → `location=IT&language=it`), matching the DuckDuckGo, Perplexity, and SearXNG providers ([#8913](https://github.com/can1357/oh-my-pi/issues/8913)).
- Fixed the `/model` Roles panel silently dropping roles and model-keyed fallback chains that fell past the visible panel height: the list had no scroll window, so entries below the cutoff were unreachable with no indication anything was missing. The panel now windows around the cursor like the provider list and shows an `↑/↓ N more` hint when rows are clipped ([#8817](https://github.com/can1357/oh-my-pi/issues/8817)).
- Fixed task and eval subagents discovering newly added agent definitions while resolving their role aliases from stale startup settings. Subagent preflight now atomically reloads persisted settings before agent discovery while preserving live runtime overrides.
- Fixed images returned by tools mounted under `xd://` rendering only as file links instead of inline terminal graphics.
- Resume Cursor idle-stall turns after completed MCP/todo tool results. The watchdog already closes the Connect stream, so unmarked blocks no longer need the `exec-resolved` marker to continue.
- Fixed the Web Search Provider Order settings summary showing providers excluded from web search ([#8884](https://github.com/can1357/oh-my-pi/issues/8884)).
- Fixed subagents aborting when external thinking exposes `think` as the required prelude before their remaining tools become callable ([#8909](https://github.com/can1357/oh-my-pi/pull/8909) by [@olegpulatov](https://github.com/olegpulatov)).
- Fixed session-title generation ignoring user `/skill:<name>` invocations, so titles now see the skill name and args instead of only later assistant text.
- Fixed destructive `rm` escaping the critical-pattern approval check when anything separates the flags from the target, so `rm -rf -- /`, `rm --recursive --force /` and `rm -rf --no-preserve-root /` are now classified critical like `rm -rf /`. `--no-preserve-root` is treated as critical wherever it appears, since it is what defeats coreutils' own refusal to recurse on `/`.
- Fixed thinking-loop aborts (`AIError.Flag.ThinkingLoop`) walking `retry.fallbackChains` and switching to another model family on attempt 1, so a healthy planning turn on Grok 4.6 (SuperGrok / Cursor OAuth) no longer gets replaced by whatever the chain lists next. The loop guard now re-samples the same model with its `thinking-loop-redirect` notice, and no longer parks the model selector on a fallback cooldown. ([#8760](https://github.com/can1357/oh-my-pi/issues/8760))
- Fixed the clipboard image-paste keybind attaching Finder's generated file icon instead of the copied image on macOS. Current Finder `Cmd+C` pasteboards advertise both a `public.file-url` and a generated 1024x1024 icon bitmap, so `arboard::get_image()` succeeded with the icon and `InputController.handleImagePaste` attached it before the file-URL branch was ever reached. The handler now probes `readMacFileUrlsFromClipboard()` before the bitmap representation, so an image file URL wins over the co-advertised icon; pure bitmap pasteboards (screenshots, browser copies) and non-image file URLs still fall through to the image/text paths ([#8769](https://github.com/can1357/oh-my-pi/issues/8769)).
- Fixed the Home Manager module (`programs.omp.settings`) breaking every launch on macOS with `Failed to acquire native file lock … Permission denied (os error 13)`. The declared config is now copied into `~/.omp/agent/config.yml` as a writable file via `home.activation` instead of a read-only `/nix/store` symlink, so OMP can acquire its config lock and persist runtime changes; `home-manager switch` still reapplies the declared settings ([#8775](https://github.com/can1357/oh-my-pi/issues/8775)).
- Fixed OpenCode MCP servers 401ing when config used OpenCode's `{env:VAR}`/`{file:path}` substitution (e.g. `Bearer {env:MCP_KEY}` headers); the OpenCode loader now expands those tokens the way OpenCode does instead of only `${VAR}` ([#8778](https://github.com/can1357/oh-my-pi/issues/8778)).
- Fixed `omp update` leaking Bun's raw `fetch()` error ("pass `verbose: true` in the second argument to fetch()") when a proxy environment variable (`HTTPS_PROXY`, `ALL_PROXY`, …) uses an unsupported scheme such as SOCKS; the update check now reports an actionable message naming the offending variable and the http/https proxy requirement ([#8784](https://github.com/can1357/oh-my-pi/issues/8784)).
- Fixed worker subprocesses (memory embeddings, tiny-model titles, TTS/STT, JS eval, browser relay, LSP mux, daemon broker) running with their cwd pinned to the CLI install directory. They share the agent's foreground process group, and terminal cwd heuristics such as kitty's `new_tab_with_cwd` pick the newest process in that group, so new terminal tabs opened in `~/.bun/install/global/node_modules/@oh-my-pi/pi-coding-agent/dist` while any worker was alive. Workers now spawn with the absolute host entry and inherit the agent's cwd.
- Preserved MCP `ImageContent` tool-result blocks so vision-capable models and the TUI can inspect returned images instead of receiving only a text placeholder ([#8687](https://github.com/can1357/oh-my-pi/issues/8687)).
- Fixed a whole-file `read` of a file with a UTF-8 BOM minting a hashline tag hashed from BOM-bearing text. Because the patcher's live read strips the BOM, the next edit to that file only applied through stale-hash recovery and reported that the file had changed externally when it had not.
- Extension bare imports of workspace members now resolve inside installed git-dependency monorepo plugins (the walk recognizes `workspaces` roots; installed node_modules copies still shadow members)
- Fixed `omp completions <shell>` hanging after writing shell completion scripts to stdout by invoking `postmortem.quit(0)` upon completion. Prevents lingering event loop handles (such as background timers or sockets loaded when inspecting command metadata) from pinning the process and blocking tools like `chezmoi`.
- Fixed `omp --smoke-test` recursively deleting unrelated directories in `os.tmpdir()` (tmux/ssh sockets, editor state, build trees). The smoke broker now keeps its runtime dir under a private parent, and the dead-scope reclaim refuses any root that is not the `daemons` container and only prunes entries named like a 16-hex daemon scope key ([#8721](https://github.com/can1357/oh-my-pi/issues/8721)).
- Fixed high CPU during multi-subagent / workflowz / orchestrate sessions: each live tool block (streaming args, a running partial tool, or a `task` subagent) armed its own 80ms spinner `setInterval` driving `requestComponentRender`, so N concurrent live blocks created N unsynchronized repaint timers that kept the render scheduler awake near-continuously. The per-block timers are now consolidated into a single shared spinner ticker that repaints every live block in one coalesced frame per glyph step, independent of block count ([#8731](https://github.com/can1357/oh-my-pi/issues/8731)).
- Fixed `omp update` writing to the PATH launcher instead of the running binary on binary-only releases (major bumps or `omp.dist: "binary"`): a foreign symlink — e.g. an admin symlink into a shared install — now resolves to its real binary in every distribution channel, avoiding an `EACCES` on a root-owned link directory or a split-brain copy that shadows the shared install. Package-manager launchers keep their deliberate in-place takeover. ([#8732](https://github.com/can1357/oh-my-pi/issues/8732))
- Added `.css` to the built-in Biome server `fileTypes` so CSS files route through Biome's linter/asserter by default instead of requiring a full per-project `fileTypes` override. ([#8741](https://github.com/can1357/oh-my-pi/pull/8741))
- Fixed memory extraction sending its instructions, few-shot examples, and the user's message as a single user turn, which caused small local models to echo the examples instead of extracting facts; instructions now travel as a system turn and the raw text as the user turn
- Fixed local title generation stopping on a stop string that appeared in the prompt instead of the generated tokens
- Fixed the Subagents HUD role display and restored generated task labels by keeping spawn handles separate from UI descriptions.
- Fixed `models.yml` custom-model providers declaring `auth: oauth` being rejected by validation with "apiKey is required", which forced a dummy `apiKey` that then shadowed the broker's OAuth tokens ([#8937](https://github.com/can1357/oh-my-pi/pull/8937) by [@usr-bin-roygbiv](https://github.com/usr-bin-roygbiv)).
- Provider-qualified model selectors (e.g. `anthropic/claude-opus-5`) now fail closed when the named provider is unavailable instead of silently re-binding to OpenRouter's same-named flat id and billing the aggregator ([#8832](https://github.com/can1357/oh-my-pi/issues/8832)).
- Fixed PlanYolo plan approval dropping all MCP tools: the post-handoff tool restore now accounts for MCP discovery that completed while planning instead of restoring a pre-discovery snapshot.
- Fixed parallel `web_search` calls hanging forever past the 60s timeout when the shared headless-browser daemon or page died mid-setup; browser fallback setup and teardown are now abort-protected ([#8865](https://github.com/can1357/oh-my-pi/issues/8865)).
- Fixed extension-package `.mcp.json` `${VAR}` env placeholders (stdio env/command/args/cwd, HTTP url/headers/oauth) reaching MCP servers unexpanded.
- Advisor blocker advisories raised inside the post-interrupt immune window now wake a new turn instead of parking as asides until the next user prompt.
- The exit banner only advertises `omp --resume <id>` when the session was actually written to disk, so the printed command no longer fails for sessions that ended before persistence ([#8860](https://github.com/can1357/oh-my-pi/issues/8860)).
- Fixed terminals that deliver Shift+Enter as a bare LF (or the legacy CSI `13;2~` form) getting a plain switch instead of summarize-and-switch in the `/tree` selector ([#8821](https://github.com/can1357/oh-my-pi/issues/8821)).
- Fixed OMP panicking at startup when the host environment contains a non-UTF-8 variable value; such entries are now skipped when copying the host environment into the shell ([#8925](https://github.com/can1357/oh-my-pi/issues/8925)).
- Fixed `/mcp reauth` refusing to run the OAuth flow for HTTP MCP servers that allow unauthenticated `initialize` but require auth for `tools/call`; endpoint discovery now runs against the server URL before giving up ([#8922](https://github.com/can1357/oh-my-pi/issues/8922)).

#### Module: `@oh-my-pi/collab-web`

##### **Fixed**
- The ask tool card now renders the note the user attached to their answer; previously it was dropped from HTML exports and the collab guest view.

#### Module: `@oh-my-pi/mnemopi`

##### **Added**
- Added optional task metadata to the runtime LLM completion interface so hosts can tell an extraction call from a consolidation call and choose the matching prompt

#### Module: `@oh-my-pi/natives`

##### **Changed**
- `enclosingBlockBoundaries` and `blockRangeAt` now reuse a parsed tree-sitter tree when the same source and language were parsed before, and skip subtrees whose line span holds no visible line. Together these cut the block-context work the `read` tool performs on every non-raw read: for an 81KB TypeScript source with a mid-file window, 13.4ms to 4.45ms on a first parse and to 0.149ms once the tree is cached; for a 1.06MB source, 188.1ms to 55.8ms and to 0.440ms. The tree cache is bounded (12 entries, 4MiB of retained source) and verifies content byte-for-byte on every hit, so a hash collision can only cost a re-parse. The subtree skip is proven equivalent by differential comparison against the exhaustive walk across 4827 repository files and 38,616 window comparisons.

#### Module: `@oh-my-pi/snapcompact`

##### **Fixed**
- Fixed image-based compaction confusing digit `0` with letter `O` and corrupting compacted identifiers (e.g. Slack IDs): the default frame fonts (X.org `8x13`, `6x12`, `5x8`) drew zero as a bare oval indistinguishable from `O`. Zero now carries a disambiguating interior slash (`8x13`) or bar (`6x12`/`5x8`); unscii-8 already shipped a slashed zero ([#8713](https://github.com/can1357/oh-my-pi/issues/8713)).

#### Module: `@oh-my-pi/tui`

##### **Fixed**
- Fixed images rendering as the `[Image: …]` text card on SIXEL terminals that expose no identifying environment variable (foot, xterm, contour): the graphics probe no longer requires Windows Terminal, and no longer reads an XTSMGRAPHICS success reply as a failure.
- Fixed the multiline editor ignoring a `tui.input.submit` remap onto Ctrl+Enter: the hardcoded Ctrl/Shift+Enter → newline fallbacks now yield to an explicit submit binding, so Ctrl+Enter can be used to submit ([#8906](https://github.com/can1357/oh-my-pi/issues/8906)).

#### Module: `@oh-my-pi/utils`

##### **Added**
- Exported `BINARY_SNIFF_BYTES`, the header window `isProbablyBinary` sniffs, so a caller holding the whole file in memory can classify the identical prefix through `isProbablyBinaryHeader` instead of reopening the file.

---

### 🚀 Release `v17.4.0` (2026-08-20)

#### Module: `@oh-my-pi/agent`

##### **Breaking Changes**
- Replaced global token counting functions (`countTokens`, `countTokensConservatively`, `setTokenizerModel`, and `estimateTokens`) with model-scoped, immutable `Tokenizer` instances (`agent.tokenizer`). Use `tokenizer.countTokens(text, mode?)`, `tokenizer.countMessage(message)`, or `tokenizer.countMessages(messages)`.
- Updated context management functions (`findCutPoint`, `prepareBranchEntries`, `collectShakeRegions`, `pruneToolOutputs`, `pruneSupersededToolResults`, and `trimRemoteCompactionInputToContextWindow`) to require an explicit `Tokenizer` instance.

##### **Added**
- Added `Tokenizer.checkTokenBudget(text, budget)` to efficiently verify if text fits within a token limit using fast byte-bound checks before falling back to full tokenization.
- Added provider-anchored transcript token estimation (`findTranscriptUsageAnchor`, `isTranscriptUsageAnchor`, `estimateTranscriptTokens`) to calculate transcript token counts incrementally from the latest reported assistant turn usage.
- Added `remotePreserveReusable()` to check whether a previous remote compaction payload remains reusable with the active model.

##### **Changed**
- Expanded native tokenizer support across catalog models, adding exact embedded token counting for Claude, Qwen 3.5+, DeepSeek V3/V4/R1, Kimi K2/K3, and GLM-5+ models. `Tokenizer` now constructs from a resolved catalog `Model`.
- `createCompactionSummaryMessage` takes an options object after `(summary, tokensBefore, timestamp)`; `CompactionSummaryMessage` gained optional `method` and `tokensAfter` display metadata.

#### Module: `@oh-my-pi/ai`

##### **Added**
- Added model metadata fields (`context_length`, `max_output_tokens`, `input_modalities`, etc.) to auth gateway model listing responses

##### **Fixed**
- Fixed tool-argument repair applying lossy transformations (such as stringifying objects or stripping unrecognized keys) when validating union schemas (`anyOf`/`oneOf`), preventing corrupted tool call and subagent payloads
- Fixed 400 errors when communicating with local OpenAI-compatible inference servers that reject `chat_template_kwargs.reasoning_effort` by improving reasoning effort parameter fallback and compatibility handling
- Fixed DeepSeek-family models on hosts like Fireworks losing reasoning whenever tools were offered: a redundant `tool_choice: "auto"` is now omitted so the provider keeps thinking enabled; forced and `"none"` selectors still take priority ([#1207](https://github.com/can1357/oh-my-pi/issues/1207))

#### Module: `@oh-my-pi/catalog`

##### **Added**
- Models now include an optional `tokenizer` family field across bundled, discovered, and custom models (supporting Claude, Qwen, DeepSeek, Kimi, and GLM families), with support for explicit overrides in model configuration.
- Added long-context cost tiers (`cost.longContext`) to subscription Codex GPT-5.6 models (Sol, Terra, Luna) matching first-party API pricing above 272K input tokens.

##### **Changed**
- Bundled model metadata is prebuilt during generation, reducing catalog startup work.

##### **Fixed**
- Fixed tool-call turn failures for `opencode-go/muse-spark-1.2` and related variants by ensuring API transport pins apply to live discovery and automatically inferring response routes for gateway-first OpenCode models ([#8957](https://github.com/can1357/oh-my-pi/issues/8957)).

#### Module: `@oh-my-pi/coding-agent`

##### **Added**
- `/cleanse` (and `omp cleanse`) — run the checker/repair loop in-session, with a live status board of running checkers, repair subagents, and token/cost totals.
- `omp ps` — interactive monitor for daemon-supervised background processes.
- Composer layouts — `composer.shape` picks the editor frame (rounded box, Claude Code rules, upstream-pi rules, borderless), with live previews in `/settings` and the setup wizard.
- Context line — `statusLine.contextLine` gauge (`percentage`, `annotated`, `embedded`) showing context usage and compaction boundaries.
- Backgroundable Python — `eval` cells can run async and auto-background like `bash`, with configurable thresholds.
- Local Claude token counting — Anthropic-family tokens now count via a native local tokenizer, and every counter (session maintenance, advisor, stats, context tools) uses the active model's own tokenizer.
- `extendedContext` setting — pick whether models with premium long-context pricing (272K/1M tiers on Codex-class models) use the extended window or compact early and stay on standard pricing.
- `/extended-context` — toggle premium long-context windows without leaving the session.
- Speculative compaction — with `compaction.asyncEnabled`, all compaction modes compact in parallel while the session continues, then splice the result in instantly.
- `tokenizer` property on custom models and `modelOverrides` to pin the tokenizer family for proxy models.
- `qwenTemplateReasoningEffort` in `models.yml` `compat` to disable the Qwen 3.8+ reasoning-effort template parameter for strict local servers.
- Click-to-toggle and drag-to-reorder for list-valued editors in `/settings`.
- `icon.subscription` and `icon.advisor` symbol-theme tokens (Nerd Font, Unicode, ASCII).

##### **Changed**
- Typing anywhere in the /models UI now immediately focuses the model list for instant search and arrow navigation.
- Revamped the todo HUD — overall progress renders along the tree-spine connector with smooth completion transitions.
- Compaction divider now names the maintenance method that fired (`remote-compacted`, `soft-compacted`, `handed-off`, `snap-compacted`) and shows the before → after context size (e.g. `256K→20K`).
- `/handoff` (and automatic handoff compaction) now compacts in place, replacing the session context instead of forking a new session.
- Compaction method priorities — `compaction.methodOrder` takes an ordered preference list (e.g. `[remote, snap]` uses remote compaction where the provider supports it, such as OpenAI, and snap everywhere else), replacing `compaction.strategy`/`compaction.remoteEnabled`.
- Unified inline overlays and selectors (model picker, settings, `/cleanse`) into one titled rounded-box panel style.
- Risk badges and warnings on `/settings` rows, starting with External Thinking.
- Faster CLI Startup

##### **Fixed**
- `/models` keeps `auto` thinking on non-default roles such as `task` instead of changing the active model and displaying the role as `max`.
- Subagent `yield` structured results no longer get corrupted by lossy argument repairs; prompt guidance improved for weak callers.
- GitHub `file_read` returns proper image blocks and direct view URLs for image/binary files.
- Cancelled prompts during pre-stream turn setup restore the text and image attachments to the editor.
- `top` builtin accepts single-dash macOS flags such as `-pid` and `-stats`.
- GNU/BSD compat sweep across built-in shell utilities (`timeout`, `diff`, `find`, `date`, `tail`, `head`, `rg`, `stat`, `truncate`, `cksum`, `sleep`, `which`, `nohup`, `kill`).

#### Module: `@oh-my-pi/hashline`

##### **Added**
- Added an opener-escape landing correction for insertions anchored on a construct's opening line to place shallower sibling constructs after the enclosing block rather than splitting the opener from its body.

##### **Fixed**
- Fixed an issue where single-line replacements echoing attributes or decorators (such as `#[napi]` or `@Injectable()`) could lead to silently duplicated annotations.
- Increased the default snapshot-store path capacity from 30 to 256 to prevent early tags in wide sessions from aging out and triggering misleading "hash is not from this session" errors.

#### Module: `@oh-my-pi/natives`

##### **Added**
- Added offline `countTokens` support for Anthropic Claude families (`ClaudeV3`, `ClaudeV47`, `ClaudeV5`) via a high-performance native port of `ctok`.
- Added exact offline token counting support for Qwen (3.5+, 3.6+, 3.8), DeepSeek (V3, V4, R1), Kimi (K2, K3), and GLM-5 models alongside rebuilt OpenAI encodings, with optimized zero-allocation string passing from JavaScript.
- Added `nodeChainAt` native API to retrieve innermost-first tree-sitter node chains with grammar kinds and line spans for structural syntax analysis.

##### **Changed**
- Improved shell builtins (`grep`, `rg`, `sed`, `cat`, `head`, `tail`, `jq`, `ls`, etc.) to stream output progressively with destination-aware line buffering for pipes, terminals, and live TUI output, while maintaining block buffering for file writes.
- Updated compound blocks (`{ ...; }`, `(...)`) and shell-function pipeline stages to run concurrently with other pipeline stages, preventing head-of-line blocking and pipe buffer deadlocks.

##### **Fixed**
- Fixed the shell output minimizer dropping failure details from non-TTY `bun test` runs: the `(fail)` line, code frame, `error:` assertion, and stack trace are now kept instead of collapsing a failing run to bare pass/fail counts; unrecognized failing test formats now fall back to head/tail instead of counts-only output.

#### Module: `@oh-my-pi/stats`

##### **Changed**
- Window token estimates now incorporate broker-reported fleet token burn when an auth broker is configured, accurately tracking fleet-wide usage instead of undercounting with local-only statistics.

##### **Fixed**
- Fixed an issue in subscription-window insights where distinct limits sharing a duration label (such as Anthropic overall vs. model-scoped 7-day windows) were incorrectly merged, which inflated window-equivalents and skewed tokens-per-window estimates. Windows are now grouped by provider limit ID.

#### Module: `@oh-my-pi/tui`

##### **Added**
- Added composer border styles (`box`, `claude`, `pi`, `borderless`) via `ComposerStyle` objects and `getComposerStyle`, unifying chrome geometry and rendering across the editor and previews.
- Added support for warning risk notes and row markers in settings lists.

---

## 📋 Instruction Guide: Recreating this Analysis

### Automated Reproduction
1. **Run the Automated Extraction Script**:
   ```bash
   python scripts/update-oh-my-pi-status.py --days 7 --write
   ```
2. **Add / Update the Executive Summary**:
   - After script generation, read through the newly generated changelog entries below.
   - Synthesize and distill the key cross-cutting themes (e.g. major breaking changes, native module optimizations, UI/TUI revamps, new settings/commands) and add/update them under `## 🌐 Executive Summary`.

### Manual Step-by-Step Procedure
1. **Fetch Upstream Tags**:
   ```bash
   git -C oh-my-pi-git-tag/src/oh-my-pi fetch origin --tags
   # Query tags from the last 7 days sorted chronologically (oldest to newest)
   git -C oh-my-pi-git-tag/src/oh-my-pi tag -l --sort=creatordate --format='%(creatordate:short) %(refname:short)'
   ```
2. **Inspect Monorepo Package Changelogs**:
   `can1357/oh-my-pi` maintains modular changelogs under `packages/*/CHANGELOG.md`. For each target release tag, inspect all package changelogs for the matching `## [X.Y.Z]` headings:
   ```bash
   for ch in oh-my-pi-git-tag/src/oh-my-pi/packages/*/CHANGELOG.md; do
       echo "=== $ch ==="
       sed -n '/## \[17.3.0\]/,/## \[/p' "$ch"
   done
   ```
3. **Filter and Group by Category**:
   - Prioritize **`Breaking Changes`**, **`Added`**, and **`Changed`** under each `@oh-my-pi/<package>` module.
   - Include relevant **`Fixed`** and **`Removed`** sections to capture behavioral adjustments and deprecations.
4. **Format Markdown & Distill Summary**:
   - Present releases in chronological order (`v17.3.0` → `v17.4.0`).
   - Read the distilled content and write an Executive Summary highlighting the top cross-cutting changes.
