# 📦 Oh-My-Pi: 7-Day Release Activity & Module Breakdown

This document tracks releases of [`can1357/oh-my-pi`](https://github.com/can1357/oh-my-pi) published over the last 7 days (November 17, 2026 – November 24, 2026), moving chronologically from the oldest release (**v18.22.1**) to the newest release (**v19.1.1**). It focuses specifically on **Breaking Changes**, **Added** features, and **Changed** behavior per module.

---

## 🌐 Executive Summary

Across **6 releases** (`v18.22.1` → `v19.1.1`, Nov 17–23, 2026), `can1357/oh-my-pi` landed a major architectural cycle (`v19.0.0` and `v19.1.0`) followed by rapid stabilization (`v19.0.1`, `v19.1.1`):

- **Major Breaking Changes & Migrations (`v19.0.0`, `v19.1.0`):**
  - **Unified per-user daemon (`v19.0.0`):** Consolidated project-specific brokers into one per-user daemon with upgrade survival (`OMP_DAEMON_TCP`), unified `omp ps` output (removing `--global`), and MCP servers moved into the daemon (`v19.1.0`, `mcp.shared` / `mcp.idleStopMinutes`).
  - **Tool commands replace `xd://` (`v19.1.0`):** Rarely-used tools now run as bash commands (`<tool> --help`, `<tool> <args>`); `tools.xdev*` settings renamed to `tools.command*`; docs moved from `xd://<tool>/<topic>` to `help://<tool>/<topic>`.
  - **`local://N.log` replaces `artifact://N` (`v19.0.0`):** Session spill files are now readable/listable under `local://` (with `/session` and `/copy local` in `v19.0.1`).
  - **Browser Relay native host (`v19.1.0`):** Chrome extension now uses a pinned ID + native messaging host and adds an interactive **Chrome Side Panel**; removed `omp browser-relay` CLI server (`--port`/`--token`). **Action:** reinstall/reload the unpacked Chrome extension after upgrading.
  - **Provider & SDK removals/renames:** Removed built-in `google-gemini-cli` OAuth (`v19.1.0`; Antigravity remains); `session.handoff(focus)` → `session.compact(focus, { mode: "handoff" })`; `createAgentSession.cacheWarming` now takes `"off" | "streaming" | "idle"`; RPC `ask` now emits a single HTML `form` request instead of field-by-field prompts; `archive.search(query)` now does full-text session search.
- **Headline Features:**
  - **Magic Edit mode (`v19.1.0`, hardened in `v19.1.1`):** Markdown bulleted change descriptions applied by a fast model with syntax checks and retry-without-loss.
  - **Prompt Cache Warming & Compaction (`v18.22.1`, `v19.0.0`, `v19.1.1`):** Anthropic no-output `prewarm`, `auto`/`keepalive`/`compact` warming strategies, per-model `snapcompactShape`, and Anthropic on-demand remote compaction for custom gateways.
  - **New Providers & Models:** Native **Kiro** provider (`/login kiro`, `/usage` credits, AWS GovCloud support), **Z.AI** GLM dynamic discovery, **Gemini 4 Neon** (unified SKU with `low`–`xhigh` thinking), **Liquid AI** `d1.2` judge models, `omp auth-gateway` `GET /v1/pi/models`, and extension provider overrides (`registerProvider` stream/image/search/discovery hooks) + `pi.registerTodoBackend()`.
  - **Workflow & TUI/UX:** `btw` mode (`?` prefix), composer next-message predictions (on by default), Tern live subagent/job cards, `tree` status segment, `ovnfs` worktree + `/wt` `post-checkout` hook support, cross-instance peer discovery (`task.crossInstance`), Binary Ninja disassembler backend (`disassembler.backend = binja`), and configurable live voice endpoints (`live.endpoint`/`live.apiKey`).
- **Linux, Native & Reliability Fixes:**
  - **Linux inotify & Wayland (`v18.22.1`, `v19.0.0`, `v19.1.1`):** Language-server file watching now excludes `node_modules`/`.git/objects` and caps usage at 25% of the user's inotify limit; Wayland screenshots, libei non-Latin text input, and GTK/Qt accessibility fixes; WSL2 `FileLock` sidecar fix eliminating multi-second session-save freezes.
  - **Native engine & regex (`v19.1.0`, `v19.1.1`):** Added `LinearRegExp` (non-backtracking SIMD-accelerated engine for TTSR/secret redaction), in-process `file` and `column` shell builtins, and fixed multi-CPU hangs/cancellation races in `grep`/`glob`/`astGrep`/`astEdit`.
  - **Claude / OpenAI / MCP stability:** Fixed Claude cross-model reasoning replay and refusal contamination, OpenAI Codex header compatibility (`session-id`), GPT-6.2 Responses prompt-cache preservation, Claude-format plugin agent tool-name mapping (`WebFetch`, `TodoWrite`, `MultiEdit`, `Agent`, etc.), and MCP 2026-07-28 fallback.

---

## 📅 Release-by-Release Detailed Changelog

### 🚀 Release `v18.22.1` (2026-11-17)

#### Module: `@oh-my-pi/agent`

##### **Added**
- A model on an extension's custom api can take the Anthropic on-demand compaction lane by declaring `remoteCompaction: { api: "anthropic-messages", enabled: true }`; the request goes through its own stream like any turn ([#19580](https://github.com/can1357/oh-my-pi/pull/19580) by [@ryanskidmore](https://github.com/ryanskidmore))

##### **Fixed**
- Fixed provider-error handling so failed tool calls are no longer fed back to the model as refusal explanations.
- Fixed one-shot retries and title generation for custom Zhipu Coding Plan providers so Beijing-time quota resets are honored.
- Fixed OpenAI remote compaction (V1 and V2) dropping configured headers of models.yml and extension-registered models, so header-authenticated gateways returned 401 ([#19579](https://github.com/can1357/oh-my-pi/pull/19579) by [@ryanskidmore](https://github.com/ryanskidmore))

#### Module: `@oh-my-pi/ai`

##### **Added**
- Added support for request-specific Anthropic beta headers through the `extraBetas` option in `buildAnthropicSearchHeaders`.
- Added `omitDemotedReasoning` to `StreamOptions`, allowing Anthropic requests to omit other models' reasoning that would otherwise be replayed as text; refused requests report the omitted block count in `demotedReasoningBlocks`.
- Usage reports can now include the credential ID used by API-key or OAuth credentials, and `AuthStorage.sessions.sticky` provides a read-only lookup for the credential serving a session.
- Added `riskAcknowledgement` to `OAuthPrompt`, allowing hosts to display login-warning acceptance text even when they decline input before the authorization URL is shown.
- `remoteCompaction: { api: "anthropic-messages", enabled: true }` opts an Anthropic model at a gateway `baseUrl` outside the known deployments into on-demand compaction; `enabled` alone keeps such a gateway excluded, and a reroute away from the configured endpoint still has to reach a known deployment. `isBuiltinApi()` tells a built-in request adapter from an extension's custom api ([#19580](https://github.com/can1357/oh-my-pi/pull/19580) by [@ryanskidmore](https://github.com/ryanskidmore))

##### **Changed**
- OpenAI Codex requests now track the latest compatible `@openai/codex` client version automatically, with an optional `PI_AI_CODEX_CLIENT_VERSION` override, so newly available Codex models can be used without updating omp.
- Updated OpenAI Codex request formatting and ChatGPT token-refresh reporting to match Codex CLI 0.169.
- Updated Claude Code and Gemini CLI client version identifiers to 2.1.326 and 0.68.0, respectively.

##### **Fixed**
- Fixed OpenAI Decisions usage accounting for gateways that report `prompt_tokens` and `completion_tokens` instead of `input_tokens` and `output_tokens`.
- Improved streaming performance for fenced thinking content containing very long unbroken lines.
- Fixed Anthropic requests replaying signed server-compaction blocks with unsupported thread metadata, avoiding a rejected request before retrying.
- Improved diagnostics for Anthropic connections that drop before a response by reporting elapsed time, upload state, and request size.
- Fixed Anthropic conversations losing reasoning from earlier non-Claude turns or turns retained through compaction.
- Fixed credential rotation and retry timing for custom providers using the Zhipu Coding Plan endpoint so Beijing-time quota resets are honored.
- Fixed Claude Fable and Mythos usage-limit errors so rotation selects a sibling account with available quota when possible.
- Invalid Antigravity CLI tool arguments now return validation errors and the expected schema to the model instead of ending the turn.
- Abandoned Antigravity CLI login directories without credentials are automatically cleaned up after 24 hours.
- Improved reliability of managed Antigravity CLI downloads on slow connections and provided more useful progress and timeout errors.
- Fixed Antigravity CLI host tools with mixed-type union schemas being published incorrectly, allowing subagents to submit results.
- Fixed Codex assistant messages in the `partial_answer` phase losing their phase when stored and replayed.

#### Module: `@oh-my-pi/browser-relay`

##### **Fixed**
- Fixed an issue where the browser relay could fail to identify the page and title of a frame it emptied and hid in a tab.

#### Module: `@oh-my-pi/catalog`

##### **Fixed**
- Fixed Factory Droid's Muse Spark 1.3 support so image inputs work and the model is available without the retired feature flag.
- Fixed GitLab Duo Claude models so earlier reasoning context is handled correctly during follow-up turns and compaction.
- Fixed stale Command Code model metadata, including image-input support, reasoning controls, token pricing, and deployment context limits.
- Fixed retry-reset timezone handling for custom providers using the Zhipu Coding Plan endpoint, including base URLs with trailing slashes.

#### Module: `@oh-my-pi/coding-agent`

##### **Breaking Changes**
- The JavaScript eval `commit` helper now validates its arguments strictly: unknown option names and non-object options throw a `TypeError` that lists the supported options. Update scripts that pass extra options. Committing an unchanged draft repository now reports that it is unchanged instead of suggesting `take()`.

##### **Added**
- Added the `providers.webKeyless` setting, enabled by default, to control whether web search and URL reading may use keyless services. Disable it to restrict these operations to configured providers; individual `omp q --model web/<engine>` requests can still explicitly run a keyless engine.
- Added configurable live voice endpoints and API keys through `live.endpoint` and `live.apiKey`. Live voice can now connect to any OpenAI Realtime WebRTC-compatible server without Codex or ChatGPT sign-in, including offline use, and `live.voice` accepts arbitrary voice names.
- Computer `el.setValue()` now accepts finite safe integer and decimal numbers and writes them as text, while continuing to reject unsupported values such as booleans, objects, `NaN`, and `Infinity`.
- On macOS, browser results now report relevant native windows—such as pickers, print or save sheets, sign-in prompts, passkey dialogs, and permission bubbles—with their `computer.window()` identifiers.
- Browser `select()` now accepts label-, value-, and zero-based index-based choices, including mixed choices for multi-select controls, across Chromium, Tern, and cmux tabs.

##### **Changed**
- Keyless Parallel searches no longer send session or model identifiers; only the search query is sent.
- The `computer` tool's macOS takeover messages now describe the actual keyboard handoff state and explain the behavior of background window moves and hover-only controls.
- Chromium `tab.observe()` and `tab.ariaSnapshot()` now wait briefly for page updates triggered by preceding actions, producing more reliable post-action results.
- When another agent controls the desktop, `InputBusy` now identifies that agent and its omp process.
- Subagents now use their own browser context by default instead of opening tabs in the user's Chrome, Tern, or cmux session; relay or Tern access can still be requested explicitly.
- Browser task guidance is now delivered automatically after the first browser call, with safety guidance available before the first call and restored after compaction or rewind.
- Named-menu reads now include nested commands with their complete command paths.
- The eval `commit` helper now runs configured Git hooks in addition to hooks in `.git/hooks/`, matching `git commit` behavior. Configured hooks may cause commits to take longer or be rejected.
- Service readiness patterns now match line boundaries correctly, and shell file-time commands honor the configured `TZ` timezone.
- Large `write` and `edit` calls remain responsive while their arguments stream.
- Selective commits now handle initialized submodule pointers and sparse checkouts more accurately, and report unmatched paths explicitly.
- Git commit operations now provide clearer status and hook feedback, including unchanged repositories, hook output, hook-modified commit subjects, and repositories with an in-progress operation or unresolved conflicts.
- `/continue` now resumes the newest session for the current directory when the most recent session was created elsewhere before receiving its first message.
- `/copy` now copies the content displayed by mid-turn `out://` replies and preserves their code blocks.
- Tools enabled in goal mode remain available after leaving that mode.
- Status-line usage now reflects the credential actually selected for multi-credential providers.
- Custom providers using the Zhipu Coding Plan endpoint now retry at the correct Beijing-time quota reset.
- `^model` references followed by sentence punctuation now resolve as model-agent references.
- `/restart` now restarts through the original launcher so upgraded installations are used by the resumed session.
- RPC hosts reliably receive completion events after quota errors, and OSC 7501 terminals no longer play stale success notifications during a newer run.

##### **Fixed**
- Fixed configured Exa and Firecrawl credentials silently falling back to keyless endpoints when credential resolution failed; credential errors are now reported.
- Fixed eval cells bypassing delegated-task completion with `yield`; use the direct tool instead.
- Fixed `/commit` and eval commits creating incorrect single-parent commits during merge and other Git operations; commits are now refused while an operation is in progress or conflicts remain.
- Fixed the `apply_patch` tool documentation incorrectly describing it as a shell command and disallowing absolute paths.
- Fixed the shell `rg` builtin ignoring slash-containing `--glob` patterns.
- Fixed `eval commit only(...)` failing when a selected path or glob matched no changed files.
- Fixed browser calls becoming permanently busy after interrupted page evaluation, and fixed stale JavaScript `confirm` or `prompt` dialogs causing subsequent calls to fail.
- Fixed macOS Chrome and Electron `computer.setValue()` failing to select an option from an empty option list.
- Fixed browser relay tabs being closed when another extension—such as a password manager—holds the tab; the tab now remains available for reattachment.
- Fixed macOS computer takeovers failing to report user intervention when the user continued typing.
- Improved browser relay errors for hidden extension frames by identifying the frame, extension, and page involved.
- Fixed Anthropic web search for `site:` queries and safety-refused searches, including clearer refusal and provider-error reporting and appropriate retry behavior.
- Subagents without an output schema no longer receive an unnecessary `yield` tool, and `yield` without data no longer incorrectly uses the last message as its result.
- Fixed macOS popup and menu interactions that could leave menus open or press the wrong control.
- Fixed Claude losing reasoning from earlier non-Claude model turns after model switches or compaction, and prevented refusal text from contaminating later requests.
- Fixed selective commits skipping updated submodule pointers and incorrectly reporting sparse-checkout paths as deletions.
- Fixed Git status scans hanging when background Git processes kept output pipes open.
- Fixed first-launch WebKit startup on macOS falling back to Chromium while the engine was still initializing.
- Fixed rejecting pre-commit hook output being omitted from commit errors.
- Fixed Ghidra analysis of Objective-C message results and arm64 retain-register data in Mach-O binaries, including cached frameworks.
- Fixed browser interactions behind modal dialogs incorrectly reporting success; covered fields and disabled elements are now rejected, and covered drag endpoints are detected.
- Fixed RPC login for providers that require an at-your-own-risk confirmation; the confirmation is now presented to the host and login proceeds only after approval.
- On Linux, language-server file watching no longer consumes excessive inotify watches in `node_modules` and `.git/objects`.

#### Module: `@oh-my-pi/mnemopi`

##### **Fixed**
- Fixed embedding requests failing when oversized inputs were clipped in the middle of an emoji or other Unicode character.

#### Module: `@oh-my-pi/natives`

##### **Added**
- Added `DesktopFocusReturn.keyboard`, which reports what happened to the user's keyboard after a macOS takeover: handed back, left as chosen, kept, brought to the front only, or not sent.
- Added `desktopWindowRoster()` to enumerate all on-screen macOS windows, including popups, pickers, and system prompts, with their owners, layers, and visibility to `listWindows`.
- Added sparse-checkout-aware Git tree operations so selective commits preserve files outside the sparse cone and collapsed sparse-directory entries.

##### **Changed**
- macOS scrolling now matches Windows and Linux: positive `dy` scrolls down and positive `dx` scrolls right.
- `InputBusy` now identifies the agent and omp process holding input or focus control when that information is available.
- Wayland text input now supports characters unavailable through the active keyboard layout, including accented characters, CJK text, and emoji, on compositors providing libei text support.
- Improved Linux accessibility performance and scalability for large GTK, Qt, and other applications, including faster element lookups and bounded tree reads for very large tables and lists.
- Tree listings now expose gitlink modes so selective commits can distinguish submodule pointers from ordinary files.

##### **Fixed**
- Fixed macOS and Windows focus restoration after computer takeovers and background input, including cases where the target application brought itself forward; the originating app now becomes active again and focus results are reported accurately.
- Fixed keyboard input on Windows and X11 when the target uses a different keyboard layout or when Caps Lock, StickyKeys, or another layout is active.
- Fixed X11 input being delivered to another application's menu, screen lock, or other keyboard grab; input now waits for transient grabs to end or fails without sending keys.
- Fixed Linux text entry from affecting the user's active field during agent input. Supported GTK and Qt text fields now use safe accessibility-based entry where possible, while unsupported fields continue to use the existing keyboard path.
- Fixed Linux interactions with combo boxes so unsupported popup-opening actions are refused safely, while supported GTK 3 and Chromium selections can be made without taking over the keyboard.
- Fixed macOS accessibility labels for SwiftUI toggles, including matching their adjacent labels with `find({ title })`.
- Fixed macOS element references in refreshed tables, including Activity Monitor, so row actions follow an unchanged row, reject a changed row safely, and provide useful before-and-after details when the row cannot be matched.
- Fixed macOS clicks and presses being reported as successful when the target was hidden, unavailable, covered by a sheet, or otherwise not clickable.
- Fixed macOS Chromium `<select>` interactions, including option matching, menu cleanup, and safe handling when the available options are incomplete.
- Fixed macOS `setValue` for numeric controls such as sliders and steppers, including reporting values that the control clamps or rounds; unsupported but step-able controls now explain how to use their increment and decrement actions.
- Fixed macOS takeover and background input from sending keys while the user is actively typing or holding input controls; such operations now wait for a safe idle point or fail without sending input.
- Fixed macOS menu and popup-button interactions from leaving menus open or sending keys into the user's application after background input completes.
- Fixed macOS background actions from incorrectly stopping when the user's app briefly took the keyboard, and improved target selection after drag-and-drop or remote-control interaction.
- Fixed Wayland screenshots and screenshot-dependent clicks, drags, and scrolls in released Linux builds. `capabilities()` now reports when capture is unavailable, with an explanatory error when PipeWire is missing.
- Fixed a Windows native IPC crash that could leave daemon-served tools hanging after another session closed its connection.
- Fixed `commitCreate()` errors from omitting rejecting `pre-commit` or `commit-msg` hook output; hook output is now included consistently with `git commit`.
- Fixed Rust block edits anchored on the first attribute or documentation comment so they cover the complete item instead of being treated as single-line edits.

##### **Removed**
- Removed the obsolete `wayland-pipewire` Cargo feature and `OMP_NATIVE_FEATURES` configuration variable.

#### Module: `@oh-my-pi/stats`

##### **Fixed**
- Fixed the Gain tab undercounting savings for sessions that use snapcompact context compaction, including backfilling recent compaction history after upgrading.

---

### 🚀 Release `v18.22.2` (2026-11-18)

#### Module: `@oh-my-pi/ai`

##### **Added**
- Added the native Kiro provider: sign in with AWS IAM Identity Center, AWS Builder ID, Google, GitHub, or a Kiro API key (`KIRO_API_KEY`), stream responses with reasoning, tool calls, and images, and report Kiro credits in `/usage` ([#18955](https://github.com/can1357/oh-my-pi/pull/18955) by [@Xytronix](https://github.com/Xytronix), based on [#14215](https://github.com/can1357/oh-my-pi/pull/14215) by [@ajdiyassin](https://github.com/ajdiyassin))
- Added a `definitive` option to `OAuthError`; `isDefinitiveOAuthFailure` now takes the error object and disables a credential marked definitive without matching its message ([#18955](https://github.com/can1357/oh-my-pi/pull/18955) by [@Xytronix](https://github.com/Xytronix))
- `buildAnthropicSearchHeaders` takes `extraBetas`, request-specific betas sent beside the web search beta ([#18125](https://github.com/can1357/oh-my-pi/pull/18125) by [@will-bogusz](https://github.com/will-bogusz))
- Added `omitDemotedReasoning` to `StreamOptions`: an Anthropic request leaves out other models' reasoning that it would otherwise replay as text, and a refused request reports how many such blocks it carried in `demotedReasoningBlocks` ([#10407](https://github.com/can1357/oh-my-pi/issues/10407)) ([#17610](https://github.com/can1357/oh-my-pi/pull/17610) by [@will-bogusz](https://github.com/will-bogusz))

##### **Fixed**
- Fixed shutting down or cancelling an omp session making every other session sharing the agent directory see its OAuth accounts as depleted for 5 minutes; still-valid tokens are also served during shutdown ([#19607](https://github.com/can1357/oh-my-pi/issues/19607))
- OAuth accounts refreshed through an auth broker keep their stored routing metadata (such as an API endpoint) in the key built for the request, instead of losing it after the first refresh ([#18955](https://github.com/can1357/oh-my-pi/pull/18955) by [@Xytronix](https://github.com/Xytronix), based on [#14215](https://github.com/can1357/oh-my-pi/pull/14215) by [@ajdiyassin](https://github.com/ajdiyassin))
- Fenced (```thinking) reasoning with very long unbroken lines no longer slows down as it streams ([#19493](https://github.com/can1357/oh-my-pi/pull/19493) by [@H4vC](https://github.com/H4vC))
- Fixed Anthropic requests that replay a signed server-compaction block still asking for a message thread, which the API refuses (`thread_unsupported_request`), so every such request first paid a rejected round trip before resending without the thread ([#19473](https://github.com/can1357/oh-my-pi/pull/19473) by [@alphastorm](https://github.com/alphastorm))
- Anthropic requests whose connection drops before any response now say how long after the request started it dropped and whether the request body was still uploading or had all been written to the socket, with its size, instead of a bare "Connection error." ([#18624](https://github.com/can1357/oh-my-pi/pull/18624) by [@will-bogusz](https://github.com/will-bogusz))
- Fixed Anthropic requests dropping the reasoning of earlier non-Claude turns signed in under another credential, or kept through a compaction; it is now replayed like other models' reasoning ([#7241](https://github.com/can1357/oh-my-pi/issues/7241)) ([#17610](https://github.com/can1357/oh-my-pi/pull/17610) by [@will-bogusz](https://github.com/will-bogusz))

#### Module: `@oh-my-pi/catalog`

##### **Added**
- Added Kiro to the model catalog with automatic discovery of every model available to the signed-in Kiro account ([#18955](https://github.com/can1357/oh-my-pi/pull/18955) by [@Xytronix](https://github.com/Xytronix), based on [#14215](https://github.com/can1357/oh-my-pi/pull/14215) by [@ajdiyassin](https://github.com/ajdiyassin))
- Added Factory Droid's Claude Fable 5.2, Gemini 4 Carbon (with its launch credit promotion, half the input rate until 2026-12-01) and Kimi K3.1 Pro, each listed once the account's feature flag enables it, and GPT Image 2.6 and GPT Image 2.6 Flare ahead of GPT Image 2.5 in the `image` role's Factory defaults ([#19191](https://github.com/can1357/oh-my-pi/pull/19191) by [@will-bogusz](https://github.com/will-bogusz))
- Added `writeModelCacheAsync()` and `forEachInSlices()`: model refreshes now build and cache discovered models in slices that yield to the event loop; `writeModelCache()` returns its outcome and no longer rewrites a provider whose rows are unchanged

##### **Changed**
- `readModelCache()` parses a payload once per process: cache files holding identical rows return the same shared row objects

#### Module: `@oh-my-pi/coding-agent`

##### **Added**
- Computer `el.setValue(75)` now writes the number as `"75"` instead of refusing a non-string; `NaN`, `Infinity`, booleans and objects are still refused, as are a whole number past 2^53 and a number that prints with an exponent, which are passed as text in digits instead ([#19405](https://github.com/can1357/oh-my-pi/pull/19405) by [@will-bogusz](https://github.com/will-bogusz))
- Added a report of native windows to browser results on macOS for visible managed browsers, spawned Chromium browsers and a loopback relay: a `<select>` menu, colour or date picker, or a print, save, sign-in, passkey or permission sheet or bubble a call raised over its tab is named with its `computer.window()` id while the browser's tab list shows that tab in front of its window, by the next call when it shows just after the call returned, and on failed calls too; connected CDP endpoints, remote relays and page-backed popup windows are excluded ([#18925](https://github.com/can1357/oh-my-pi/pull/18925) by [@will-bogusz](https://github.com/will-bogusz))
- Added Kiro as a built-in provider: run `/login kiro`, pick Identity Center, Builder ID, or an API key, and choose a discovered `kiro/<model-id>` model. Each `/login kiro` adds an account ([#18955](https://github.com/can1357/oh-my-pi/pull/18955) by [@Xytronix](https://github.com/Xytronix), based on [#14215](https://github.com/can1357/oh-my-pi/pull/14215) by [@ajdiyassin](https://github.com/ajdiyassin))
- Added Google and GitHub to `/login kiro`: approve a one-time code at `app.kiro.dev`, then sign in with that account ([#18955](https://github.com/can1357/oh-my-pi/pull/18955) by [@Xytronix](https://github.com/Xytronix), based on [#14215](https://github.com/can1357/oh-my-pi/pull/14215) by [@ajdiyassin](https://github.com/ajdiyassin))
- `/usage` and `omp usage` now show Kiro credits: the monthly plan credits with their reset date, active bonus credits with their expiry, and overage credits and charges when overage is enabled ([#18955](https://github.com/can1357/oh-my-pi/pull/18955) by [@Xytronix](https://github.com/Xytronix), based on [#14215](https://github.com/can1357/oh-my-pi/pull/14215) by [@ajdiyassin](https://github.com/ajdiyassin))

##### **Changed**
- Model registries in one process (SDK embedders, tests) now share discovered-model builds, so refreshing another registry skips rebuilding models an earlier one already built

##### **Fixed**
- Fixed the UI freezing briefly when a prompt is submitted: prompt history is now written to disk in the background (within 100 ms, and on exit) instead of on the Enter keystroke
- Fixed the UI freezing while discovered models from large provider catalogs are merged: the merge now runs in slices that yield to the event loop
- Fixed closing omp's headless browser taking about 7 s when Chromium never finishes a graceful shutdown (seen with Chrome for Testing 150 on macOS 27): a browser on an omp-created profile is now killed at once
- Failed computer runs retain text and screenshots already produced in JavaScript and Python Eval, so agents can inspect partial actions without losing the error; direct computer calls also show the failure's name and message alongside partial output ([#19100](https://github.com/can1357/oh-my-pi/pull/19100) by [@will-bogusz](https://github.com/will-bogusz))
- Fixed Exa and Firecrawl web searches silently falling back to their keyless public endpoints when a configured credential failed to resolve (for example a failing `!command`); they now report the credential error
- Fixed eval cells being able to call `yield` (directly or through `xd://yield`) without finishing the delegated task; eval now rejects `yield` and points to the direct tool ([#19470](https://github.com/can1357/oh-my-pi/pull/19470) by [@alphastorm](https://github.com/alphastorm))
- Fixed service `ready.log` and wait patterns not matching `^` and `$` at line boundaries after earlier output ([#19471](https://github.com/can1357/oh-my-pi/pull/19471) by [@alphastorm](https://github.com/alphastorm))
- Fixed the shell's `stat`, `diff` and `find` builtins ignoring `TZ` when printing file times; `find -ls` now prints times in the shell's time zone instead of UTC, and `find -newermt` reads dates like `Nov 15, 2023` in the shell's time zone ([#19482](https://github.com/can1357/oh-my-pi/pull/19482) by [@alphastorm](https://github.com/alphastorm))
- With TTSR rules active, large `write` and `edit` calls no longer slow down as their arguments stream ([#19494](https://github.com/can1357/oh-my-pi/pull/19494) by [@H4vC](https://github.com/H4vC))
- Fixed `/commit` and eval `commit` creating a single-parent commit during a merge; committing now refuses while a merge, cherry-pick, revert, rebase or `git am` is in progress or the index has unresolved conflicts ([#19474](https://github.com/can1357/oh-my-pi/pull/19474) by [@alphastorm](https://github.com/alphastorm))
- Fixed the `apply_patch` tool description calling it a shell command and forbidding absolute paths ([#19325](https://github.com/can1357/oh-my-pi/issues/19325), [#19468](https://github.com/can1357/oh-my-pi/pull/19468) by [@alphastorm](https://github.com/alphastorm))
- Fixed the shell's `rg` builtin ignoring `--glob` patterns that contain a slash ([#19476](https://github.com/can1357/oh-my-pi/pull/19476) by [@alphastorm](https://github.com/alphastorm))
- Fixed eval `commit` `only(...)` failing when one of its paths or globs matched no changed file; unmatched ones are now reported ([#19472](https://github.com/can1357/oh-my-pi/pull/19472) by [@alphastorm](https://github.com/alphastorm))
- Fixed a Tern browser block answering every later browser call with "Tab is busy: another call on this tab is still running" after a call whose page evaluation never returned, such as one cut off by a redirect; such a call now ends at its time limit or when cancelled, and the tab takes the next call
- Fixed the browser tool reporting a JavaScript `confirm` or `prompt` as still open, and failing page calls on it, after the user clicked it away or another CDP client answered it ([#19481](https://github.com/can1357/oh-my-pi/pull/19481) by [@will-bogusz](https://github.com/will-bogusz))
- Fixed `computer` `setValue` on a `<select>` in Chrome or an Electron app on macOS failing with an empty list of options; it now chooses the option the value names ([#19224](https://github.com/can1357/oh-my-pi/pull/19224) by [@will-bogusz](https://github.com/will-bogusz))
- A relay tab is no longer closed when another extension's frame, such as a password manager's autofill menu that undoes the relay clearing it, keeps Chrome refusing omp: the call fails saying what holds the tab, the tab stays open as the user left it, and the next call reattaches to it ([#19178](https://github.com/can1357/oh-my-pi/pull/19178) by [@will-bogusz](https://github.com/will-bogusz))
- Fixed the computer tool telling the model that only an X11 takeover can end with nothing sent because the user kept typing; a macOS takeover now waits for the user's pause too and reports `UserIntervened` the same way ([#19296](https://github.com/can1357/oh-my-pi/pull/19296) by [@will-bogusz](https://github.com/will-bogusz))
- When the browser relay hides another extension's frame in a tab omp drives (a password manager's inline menu or save card), the call that ran into it, or a later one on that tab, now names the frame's page, the extension's id and the page's own title, and says the frame is hidden for the user too ([#19001](https://github.com/can1357/oh-my-pi/pull/19001) by [@will-bogusz](https://github.com/will-bogusz))
- Anthropic web search now passes `site:`-scoped queries to Claude with the domain and path still in the text, and tells Claude to always search, so those lookups and queries it thought it could answer from memory no longer fail with "returned no sources" ([#18125](https://github.com/can1357/oh-my-pi/pull/18125) by [@will-bogusz](https://github.com/will-bogusz))
- Anthropic web search on models with a refusal fallback (Opus 5 and 5.5, Sonnet 5.5, Fable 5) has Anthropic retry a query the safety classifier declines on another Claude model, and reports a refusal or a failed search (`too_many_requests`, …) by name instead of "returned no sources" ([#18125](https://github.com/can1357/oh-my-pi/pull/18125) by [@will-bogusz](https://github.com/will-bogusz))
- Subagents without an output schema (including eval `agent()` calls without `schema`) no longer get a `yield` tool; their final message is the result.
- A `yield` without `data` no longer uses the subagent's last message as the result; it only finalizes incremental sections that were already submitted.
- A `computer` key press that opens a macOS popup button's or menu button's menu in the background now fails listing the items and naming the press or click that chooses one, instead of leaving the menu open with your keyboard ([#19179](https://github.com/can1357/oh-my-pi/pull/19179) by [@will-bogusz](https://github.com/will-bogusz))
- Fixed Claude not seeing the reasoning of earlier Codex, Kimi, Grok and other non-Claude turns after a model switch, including turns kept through a compaction; it now gets that reasoning as text. When Claude refuses a turn with `Refusal (reasoning_extraction)` because of that carried reasoning, the turn is retried once without it, and the session stops sending it to Claude ([#7241](https://github.com/can1357/oh-my-pi/issues/7241)) ([#17610](https://github.com/can1357/oh-my-pi/pull/17610) by [@will-bogusz](https://github.com/will-bogusz))
- After an Anthropic refusal, later turns no longer resend the refusal text with the tool calls it stopped: those calls now replay as "not executed" only, so one `reasoning_extraction` refusal stops making every following turn of the session likely to be refused too ([#19419](https://github.com/can1357/oh-my-pi/pull/19419) by [@flosrn](https://github.com/flosrn))
- Fixed selective commits skipping updated submodule pointers; existing initialized gitlinks can now be reviewed and explicitly selected without committing changes inside the submodule ([#19556](https://github.com/can1357/oh-my-pi/pull/19556) by [@kim-dali](https://github.com/kim-dali))
- Fixed git reads such as `/commit`'s status scan hanging when a background git process kept the output pipe open ([#19478](https://github.com/can1357/oh-my-pi/pull/19478) by [@alphastorm](https://github.com/alphastorm))
- Fixed the browser falling back to Chromium on the first launch of a new WebKit engine build on macOS: the WebKit host now gets 60 seconds instead of 10 to answer its greeting while macOS scans the engine's binaries and libraries ([#19423](https://github.com/can1357/oh-my-pi/pull/19423) by [@shgew](https://github.com/shgew))
- Fixed `--continue` opening a new empty session when the terminal's last session was started in another directory and closed before its first message; it now resumes the current directory's newest session ([#19495](https://github.com/can1357/oh-my-pi/issues/19495)).
- Fixed a rejecting `pre-commit` hook's stdout (e.g. the `pre-commit` framework's per-hook report) missing from the error raised by the eval `commit` namespace and `omp commit` ([#19449](https://github.com/can1357/oh-my-pi/issues/19449))
- `/commit` now shows the subject a commit-msg hook wrote onto the commit, instead of the subject from before the hook ran ([#19448](https://github.com/can1357/oh-my-pi/pull/19448) by [@eggpeat](https://github.com/eggpeat))
- `^model` references followed by sentence punctuation now register their model agent instead of remaining literal ([#19445](https://github.com/can1357/oh-my-pi/pull/19445) by [@yuzu-octopus](https://github.com/yuzu-octopus))
- Selective commits in sparse checkouts no longer report paths outside the cone as unstaged deletions to commit hooks ([#19453](https://github.com/can1357/oh-my-pi/pull/19453) by [@yuzu-octopus](https://github.com/yuzu-octopus))
- Custom providers pointing at the Zhipu Coding Plan endpoint now retry at the Beijing-time quota reset instead of waiting eight hours too long ([#19446](https://github.com/can1357/oh-my-pi/pull/19446) by [@yuzu-octopus](https://github.com/yuzu-octopus))
- `/copy` now copies what a mid-turn `out://` reply showed, instead of the reply tool's own "Shown to the user." result, and lists the reply's code blocks in the turn's blocks ([#19551](https://github.com/can1357/oh-my-pi/pull/19551) by [@bannert1337](https://github.com/bannert1337))
- Fixed tools enabled during goal mode becoming unavailable after leaving it ([#19514](https://github.com/can1357/oh-my-pi/pull/19514) by [@yuzu-octopus](https://github.com/yuzu-octopus))
- Fixed the status-line usage segment showing another account's quota for multi-credential API-key providers such as `opencode-go`; it now follows the credential row the session router actually serves from ([#19456](https://github.com/can1357/oh-my-pi/issues/19456)) ([#19492](https://github.com/can1357/oh-my-pi/pull/19492) by [@thekitaev](https://github.com/thekitaev)).
- Fixed Objective-C message results and arm64 retain-register data flow in Ghidra analysis of Mach-O binaries, including previously analyzed cache-extracted frameworks ([#19558](https://github.com/can1357/oh-my-pi/pull/19558) by [@shgew](https://github.com/shgew)).
- With a modal dialog open, browser `fill`, `type` and `press` aimed at a field behind it now fail naming what covers it, as `click` does, instead of typing into the dialog's button and reporting success (on Chromium tabs and Tern tabs without native DOM reads); `press` also refuses a disabled element (on Chromium tabs and Tern tabs without native DOM reads), and Chromium `drag` refuses a covered start or end ([#19524](https://github.com/can1357/oh-my-pi/pull/19524) by [@will-bogusz](https://github.com/will-bogusz))
- Fixed RPC `login` refusing providers with an at-your-own-risk warning (`antigravity-cli`, `google-antigravity`): the warning now reaches the host as an `extension_ui_request` `input`, and login continues on "yes" and cancels on anything else ([#19523](https://github.com/can1357/oh-my-pi/issues/19523))
- On Linux, file watching for language servers no longer puts an inotify watch on every directory under `node_modules` and `.git/objects`, which could use up the system's inotify watch limit and keep other programs such as systemd from adding watches ([#19459](https://github.com/can1357/oh-my-pi/issues/19459))
- `/restart` now re-execs through the launcher omp was started by, so an open session moves onto an upgraded binary instead of re-running a retained old install ([#19529](https://github.com/can1357/oh-my-pi/pull/19529) by [@yuzu-octopus](https://github.com/yuzu-octopus))
- RPC hosts now always receive a terminal `agent_end` after an over-quota 429: usage-limit bookkeeping is bounded so a stalled usage report can no longer hold the event ([#19411](https://github.com/can1357/oh-my-pi/issues/19411), [#19417](https://github.com/can1357/oh-my-pi/pull/19417) by [@yuzu-octopus](https://github.com/yuzu-octopus))
- Rex and other OSC 7501 terminals no longer play a success sound mid-run when a stale agent end arrives after another run has opened ([#17307](https://github.com/can1357/oh-my-pi/issues/17307), [#19418](https://github.com/can1357/oh-my-pi/pull/19418) by [@yuzu-octopus](https://github.com/yuzu-octopus))

#### Module: `@oh-my-pi/natives`

##### **Added**
- `TtyWriter` now works on Windows consoles: it writes off the JS thread in 16 KiB `WriteFile` chunks, restores the UTF-8 console code pages that child processes change, and `stop()` cancels a blocked write
- Added `isolateThreadStartsFromConsole()`, which keeps a Windows console whose terminal stopped reading from blocking new threads in the process

#### Module: `@oh-my-pi/utils`

##### **Added**
- Added `readBoundedBody` and `readBoundedJson` for reading HTTP response bodies with a size limit, with an optional signal so a stalled peer cannot outlive the caller's deadline ([#18955](https://github.com/can1357/oh-my-pi/pull/18955) by [@Xytronix](https://github.com/Xytronix))

---

### 🚀 Release `v19.0.0` (2026-11-19)

#### Module: `@oh-my-pi/agent`

##### **Added**
- Added support for excluding custom messages from model context and compaction or branch summaries, while allowing queued steering and follow-up messages to continue correctly after excluded messages.

#### Module: `@oh-my-pi/ai`

##### **Added**
- Added a `prewarm` stream option for Anthropic Messages requests to refresh prompt caches without generating billable output; it is rejected for budget thinking, forced tool choice, and structured output.
- Claude usage reports now include the account subscription plan in `metadata.subscriptionPlan`, supporting Max 5x, Max 20x, Pro, Team, and Enterprise plans.
- Added `retryUnreachableBroker` and `onBrokerRetry` options to `discoverAuthStorage`, allowing hosts to control startup retries for temporarily unavailable authentication brokers and display retry status.

##### **Fixed**
- Fixed Claude account failover after a shared weekly usage limit recovers, ensuring accounts become available again when usage reporting no longer shows that window.
- Authentication broker startup now tolerates temporary broker restarts and connection interruptions by retrying for up to 30 seconds, while still failing immediately for rejected tokens or malformed snapshots.
- Improved authentication broker compatibility across client and broker versions by tolerating unknown credential, usage, and observed-usage fields and values.
- Fixed Codex Spark usage meters so reports that identify the meter only by `metered_feature` remain correctly scoped to the Spark model.
- Fixed Antigravity CLI requests for models whose available IDs include effort suffixes, such as resolving `gemini-4-hydrogen` when only `gemini-4-hydrogen-high` is offered.

#### Module: `@oh-my-pi/catalog`

##### **Added**
- Added support for prompt-cache prewarming on the first-party Anthropic endpoint via the `isPromptCachePrewarmSupported` compatibility capability.

##### **Fixed**
- Fixed hosted judgment requests for TypeSafe, OpenRouter, Command Code, and OpenCode Zen when evaluating more than 32 questions.
- Improved Devin image handling to support more conversation images within provider limits, and updated image compaction for Devin Gemini models to reflect their billed token usage.
- Fixed Devin Gemini model pricing so models switch from promotional to list pricing when promotions end.
- Fixed Kiro API key authentication (`KIRO_API_KEY` and `ksk_…`) so model listing, chat, and `/usage` requests work correctly.

#### Module: `@oh-my-pi/coding-agent`

##### **Breaking Changes**
- Changed SDK cache warming controls: createAgentSession.cacheWarming now accepts the mode cap "off", "streaming", or "idle"; the lower of this value and providers.cacheWarming applies. Use "off" instead of false.
- Replaced artifact://N links with readable, listable, and completable local://N.log files at the session's local:// root. artifact:// links in existing sessions are not migrated.
- Replaced session.handoff(focus) with session.compact(focus, { mode: "handoff" }); use abortCompaction() to cancel it.
- Consolidated shared background processes under one per-user daemon rather than project-specific brokers. Daemons and services from older versions are not adopted; omp ps now reports global, project, and session units together, removes --global, changes --json output to {daemon, reports}, and no longer adds ?project= to dsm:// handles.
- Renamed SDK deferSkillDescriptionCompression to deferHintCompression and startSkillDescriptionCompression() to startHintCompression(); these settings and methods now also cover MCP namespace hints.

##### **Added**
- Added built-in MCP transforms, including the Codex Desktop node_repl replacement. Built-ins can be disabled with mcp.builtinTransforms; /mcp list identifies replaced servers and /mcp enable node_repl can explicitly connect one.
- Added optional MCP eval namespaces through mcp.evalNamespaces, exposing servers as JavaScript and Python namespaces with documentation at xd://eval/<server>. Results preserve text and structured data, and binary resources are saved as local:// files.
- Added model-generated names for /tan agents and their tray cards, with a readable random fallback when naming fails or times out.
- Added configurable cache-warming strategies (auto, keepalive, and compact), including long-tool-call keepalive and pre-expiry prompt compaction. Cache-warming events now report the selected method and costs.
- Added optional cross-instance task discovery and messaging with task.crossInstance, exposing same-folder instances through agent://peers.
- Added btw mode: drafts beginning with ? submit as /btw questions and receive distinct UI indication.
- Added Tern live cards for running subagents and background jobs, including progress, tool counts, status, controls, transcripts, and restored access to finished agents.
- Added daemon update survival and optional TCP hosting through OMP_DAEMON_TCP, preserving running services, PTYs, and language servers across daemon upgrades.
- Loaded speech-to-text and text-to-speech models once per machine, unloading them after 15 minutes of inactivity.
- Added ovnfs worktree support to /wt, the project resume picker, and omp worktree list/clear, while preserving session resume from the source repository after checkout removal.
- Added Claude subscription plans to omp usage and /usage output.
- Added progress reporting for background skill-description and MCP namespace hint generation.
- Added excludeFromContext to pi.sendMessage payloads so extensions can display and save per-turn messages without sending them to the model.
- Added a 30-second retry window for CLI and print-mode commands while the authentication broker restarts or is briefly unavailable.
- Added a notify option to the bash tool for reporting matching output from background commands and named services, waking idle sessions or ending blocked waits.

##### **Changed**
- Improved cache warming for Anthropic-compatible providers with no-output prewarming where supported and billing based on actual replay costs; task subagents now keep prompt caches warm during long tool calls when streaming warming is enabled.
- Generated skill descriptions and MCP namespace hints once per machine, sharing results and progress across omp windows.
- Preserved thinking levels when switching models, adjusting only when the selected model cannot support the current level; model defaults apply only when no level is set.
- Extended repeated reply and subagent waits to use the session's prompt-cache lifetime, and made subagent waits follow the live parent's next message when appropriate.
- Made /handoff run as background compaction while preserving the current response and newly arriving messages.
- Redesigned ask prompts as a single scrolling form above the composer, preserving partial answers and allowing users to skip pending questions by sending a message.
- Enabled composer predictions by default, showing the active model's suggested next message after completed turns; disable them in Settings → Interaction.
- Disabled tool-call intent tracing by default in print, RPC, ACP, and SDK sessions; enable it with tools.intentTracing or PI_INTENT_TRACING.
- Updated ovnfs checkout guidance and git guard messages to explain how to land, pull, or discard changes.
- Improved subagent completion probes and side requests so they focus on deliverables and do not include still-streaming reasoning as plain history.
- Standardized wait behavior to a 5-second initial idle wait followed by four-minute back-to-back waits.
- Always provide subagents with the shared LSP tool; task.enableLsp now controls only LSP formatting and diagnostics for edits.
- Improved bash services, PTYs, and embedded shells with session environment inheritance, session-file URL support, clearer readiness validation, and more transparent minimized output.
- Named managed Chromium clearly when running in a window and improved browser, screenshot, upload, frame, selector, network, and CDP behavior across tabs and browser backends.
- Improved hashline editing with verbatim replacement bodies, safer range and path validation, clearer parse and syntax diagnostics, support for larger files and SSH files, and more predictable raw reads and line selectors.
- Improved MCP reliability with ten-minute tool-call deadlines, longer deadlines when progress is reported, clearer timeout and connection errors, and one retry after expired HTTP sessions.
- Expanded the embedded shell with portable built-ins and internal-URL support for common workflows, including file inspection, archiving, process control, environment loading, file watching, locking, speech, opening files, and patch application.
- Improved LSP and debugging diagnostics, language coverage, workspace detection, references, rename, code actions, and server lifecycle reporting.
- Improved eval tooling with Python 3.9+ validation, UTF-8 execution, package installation refreshes, full tool results, protocol-file access, threaded Python helpers, and clearer kernel-loss and timeout messages.
- Improved commit drafts and summaries to handle hooks, amend operations, worktrees, filters, line endings, large untracked trees, review files, and JavaScript/Python API parity more accurately.
- Improved URL, archive, GitHub, Terraform Registry, package documentation, web search, and remote-file handling, including filtering, pagination, binary conversion, archive member access, and clearer provider errors.
- Improved usage and account policy reporting so subscription limits and scoped exhaustion identify the affected plan or meter accurately.
- Improved worktree, process, wait, agent messaging, session restore, memory retention, Spotlight, Windows shell, and macOS performance behavior.

##### **Fixed**
- Fixed MCP resource links and binary resources so they remain accessible as readable files or inline content rather than being dropped or shown only as placeholders.
- Fixed commit drafts after pre-commit hooks and partial prior commits so the index, diff, selected blocks, amended parent, review files, and generated summaries remain accurate.
- Fixed automatic Hindsight and Mnemopi retention during runs with async work, subagents, or peer messages, preventing duplicate or overlapping retention.
- Fixed blocked agents and waits by reporting waiters and dependency chains, delivering messages to queued agents, and correctly handling killed, evicted, resumed, or empty-output jobs.
- Fixed session resume and process-result handling across unified-daemon upgrades.
- Fixed thinking-level display and model-switcher behavior for subagents, auto-thinking sessions, and manually adjusted levels.
- Fixed worktree cloning, ovnfs/Git transitions, service readiness checks, shell environment inheritance, Windows junction removal, process substitution, checksums, and background command cancellation.
- Fixed browser automation reliability across screenshots, clicks, fills, tabs, frames, dialogs, uploads, CDP endpoints, stale connections, concurrent evaluations, browser startup, viewport emulation, clipboard, and platform-specific input.
- Fixed hashline, AST editing, generated-file detection, numbered content, remote-file editing, syntax diagnostics, path handling, and line-ending behavior.
- Fixed eval kernels, Python and JavaScript helpers, package imports, nested tool calls, internal URLs, and moved working directories.
- Fixed LSP, language-server startup, diagnostics, references, rename, code actions, project loading, file types, and debugger adapter selection.
- Fixed command-output summarization so relevant context, metadata, Git output, test timing, AWS output, lint diagnostics, and binary detection are preserved instead of being misclassified.
- Fixed read, grep, glob, URL, archive, SQLite, video, RSS, GitHub, package-documentation, SSH, and web-search handling across selectors, filters, pagination, archives, binary content, and provider failures.
- Fixed todo operations, ask compatibility and timeout behavior, image generation validation, GitHub PR pushes, plan proposals, and session accounting for side-channel model calls.
- Fixed MCP OAuth reauthentication errors to expose registration endpoints, status details, and remedies, and fixed auth-broker shutdown so refreshed tokens are saved safely.
- Fixed Spotlight retry and account handling, including waitlisted accounts, rate limits, outages, and request identification.
- Fixed cross-platform shell and desktop behavior, including macOS startup and redraw performance, Windows file operations and application lookup, speech output, and desktop opening.

#### Module: `@oh-my-pi/collab-web`

##### **Fixed**
- Fixed web search cards without a synthesized answer displaying raw numbered result lists; they now show a concise excerpt for each source instead.

#### Module: `@oh-my-pi/natives`

##### **Added**
- Added `VcsGitRepo.worktreeToGit()` to convert worktree content into the blob representation produced by `git add`.
- Added support for using a `Shell` as a process's shell, routing commands through the process's standard streams while preserving the process session and terminal for external commands.
- Added `ShellRunOptions.speech` to connect the host speech handler to the shell's `say` command.
- Added an in-process `file` shell builtin with broad file-type detection, MIME and encoding output, archive/image/document support, and compatibility with the commonly used `file` command options.

##### **Changed**
- Improved typing and key-press responsiveness in iPhone Mirroring, reducing per-character latency by approximately half.

##### **Fixed**
- Fixed screenshots of partially off-screen Linux windows on Wayland and X11 so the visible region is captured and coordinate-based zoom targets correctly.
- Fixed Wayland input operations on desktops without an available input route to fail immediately with a clear `PermissionDenied` error instead of attempting unnecessary screen capture first.
- Fixed macOS `computer` interactions so background clicks, key presses, pop-up menu actions, and takeover calls restore the previously active window within the call.
- Fixed macOS pop-up menu reads immediately after typing so they reflect the option selected by the entered letters.

#### Module: `@oh-my-pi/stats`

##### **Breaking Changes**
- Spotlight recovery counts reads from local spill files toward recovery counts; reads from artifact references in older sessions continue to count as before.

##### **Added**
- Expanded the Overview's Token mix to include off-transcript model calls—such as title generation, job captions, judge queries, and cache warming—with per-source request counts, token totals, and usage shares.
- Added a Decision models card to the Overview showing requests, tokens, and usage share by judgment use case for native judgment models.
- Request details for title-generation and judge calls now display the generated reply or recorded judge answers.

##### **Changed**
- Token mix shares for the main agent, subagents, and advisor now reflect conversation turns only, excluding side-channel model calls.

##### **Fixed**
- Hardened the dashboard against DNS rebinding by rejecting requests made through unconfigured public host names. IP addresses, localhost, LAN short names, local network domains, and Tailscale names remain supported; configure reverse-proxy or other custom domains with OMP_STATS_ALLOWED_HOSTS, including wildcard subdomains such as *.example.com.

#### Module: `@oh-my-pi/utils`

##### **Added**
- Added utilities for formatting and parsing session spill URLs using the `local://N.log` format.
- Added `postmortem.exitCleanlyOnStopSignals()` so long-running services exit successfully after completing cleanup on SIGINT or SIGTERM.

##### **Fixed**
- Fixed Windows shell discovery incorrectly selecting the WSL `bash.exe` launcher, which could cause services to run under WSL.
- Fixed archive opening so the extraction-size limit is enforced when an oversized member is read rather than preventing access to the entire archive.
- Fixed `OMP_LOG_LEVEL` so it also controls console output from services such as `omp auth-broker serve`, not just log-file output.
- Fixed Markdown parsing so emphasis and link labels are not prematurely terminated by marker characters inside code spans, autolinks, inline HTML tags, or link destinations.

#### Module: `@oh-my-pi/wire`

##### **Added**
- Added tray state and interaction properties, including focus, peek, quiet, main status, item references, card status and actions, and event state.
- Added layout transition properties to nodes for coordinating layout animations.
- Added support for folding a dock composer into its compact row.

---

### 🚀 Release `v19.0.1` (2026-11-19)

#### Module: `@oh-my-pi/ai`

##### **Fixed**
- Fixed GIF images failing Liquid AI judgments with HTTP 422; they are now sent as PNG ([#19757](https://github.com/can1357/oh-my-pi/pull/19757) by [@alphastorm](https://github.com/alphastorm))
- Anthropic strict-tool fallback now treats a Vertex org-policy rejection of `structured_outputs` (`allowedPartnerModelFeatures` / "disallowed feature structured_outputs") as a strict-tools rejection, retries once without `strict`, and pins `strictToolsDisabled` ([#19576](https://github.com/can1357/oh-my-pi/issues/19576)) ([#19655](https://github.com/can1357/oh-my-pi/pull/19655) by [@koeria](https://github.com/koeria))
- Kiro requests rejected with `Input is too long.` or `CONTENT_LENGTH_EXCEEDS_THRESHOLD` can now recover through conversation compaction ([#19723](https://github.com/can1357/oh-my-pi/pull/19723) by [@emotionbug](https://github.com/emotionbug))
- Kiro thinking off now turns reasoning off instead of running the model's default effort; models that cannot disable reasoning use their lowest effort ([#19722](https://github.com/can1357/oh-my-pi/pull/19722) by [@emotionbug](https://github.com/emotionbug))
- Kiro `/usage` shows purchased add-on credits, and an account whose plan credits are spent keeps serving while add-on credits remain ([#19724](https://github.com/can1357/oh-my-pi/pull/19724) by [@emotionbug](https://github.com/emotionbug))
- Kiro Identity Center logins in AWS GovCloud (US) now list profiles in `us-gov-west-1` and `us-gov-east-1` instead of the commercial regions, which reject GovCloud tokens ([#19726](https://github.com/can1357/oh-my-pi/pull/19726) by [@TechDufus](https://github.com/TechDufus))
- Statusless gateway errors reading `stream interrupted` now retry like `stream was interrupted` instead of ending the turn ([#19709](https://github.com/can1357/oh-my-pi/issues/19709)).

#### Module: `@oh-my-pi/browser-relay`

##### **Fixed**
- The browser relay extension survives a browser whose loaded permission set predates the `downloads` permission: the service worker keeps working without download pairing instead of crashing before it ever connects ([#19659](https://github.com/can1357/oh-my-pi/pull/19659) by [@pavel-kalmykov](https://github.com/pavel-kalmykov))

#### Module: `@oh-my-pi/catalog`

##### **Added**
- Added Liquid AI's `d1.2` and `d1.2-ultra` judge models; `liquid` now defaults to `d1.2` ([#19753](https://github.com/can1357/oh-my-pi/pull/19753) by [@alphastorm](https://github.com/alphastorm))
- Added `gemini-4-neon` to the bundled Antigravity CLI roster, with the `low`/`medium`/`high`/`xhigh` thought levels `agy` offers for it ([#19787](https://github.com/can1357/oh-my-pi/pull/19787) by [@ataberkus](https://github.com/ataberkus)).
- `Model.snapcompactShape` (`{ variant, frameSize? }`) gives a model its own snapcompact frame shape ([#19591](https://github.com/can1357/oh-my-pi/pull/19591) by [@ryanskidmore](https://github.com/ryanskidmore))

##### **Fixed**
- Discovered Kiro models that cannot turn reasoning off now use their lowest supported effort when thinking is set to off ([#19722](https://github.com/can1357/oh-my-pi/pull/19722) by [@emotionbug](https://github.com/emotionbug))
- Kiro accepts AWS GovCloud (US) profile ARNs (`arn:aws-us-gov:codewhisperer:…`), which were previously skipped during profile listing ([#19726](https://github.com/can1357/oh-my-pi/pull/19726) by [@TechDufus](https://github.com/TechDufus))
- Google Antigravity no longer lists Gemini 4 Hydrogen's sonar monitor slot or its tiered High/XHigh SKUs as separate models; the tiered SKUs fold into the one Gemini 4 Hydrogen model ([#19795](https://github.com/can1357/oh-my-pi/pull/19795) by [@eggpeat](https://github.com/eggpeat))
- Gemini 4 Neon on Google Antigravity now shows as one model whose thinking level (low, medium, high, xhigh) selects the matching SKU, instead of four separate models, and is priced at $3/$15 per million tokens ($0.15 cached) instead of $0 ([#19789](https://github.com/can1357/oh-my-pi/pull/19789) by [@eggpeat](https://github.com/eggpeat))
- Gemini 4 Neon now collapses into one model on Gemini CLI too, and on the Gemini API and Vertex AI offers the xhigh thinking level and long outputs up to 262,144 tokens, with its $3/$15 Gemini API price

#### Module: `@oh-my-pi/coding-agent`

##### **Added**
- `/session` shows the path of the session's `local://` directory, and `/copy local` copies it, creating the directory first so it can be entered before anything was written there ([#19778](https://github.com/can1357/oh-my-pi/pull/19778) by [@farnoy](https://github.com/farnoy))
- `snapcompactShape` on `models.yml` models, `modelOverrides` and extension `registerProvider` models sets that model's snapcompact frame shape ([#19591](https://github.com/can1357/oh-my-pi/pull/19591) by [@ryanskidmore](https://github.com/ryanskidmore))

##### **Fixed**
- Fixed PTY command transcripts sometimes gaining a blank line where a `\r\n` line ending was split across two terminal reads.
- Fixed the shell's `dirname` builtin on Windows ignoring `\` separators and drive prefixes (`dirname 'C:\a\b'` printed `.`), which broke scripts like VS Code's `code` launcher (`./Code.exe: No such file or directory`)
- Fixed bash output minimizing being skipped on Windows when a command is named by a `\` path or with `.exe` (`"C:\Program Files\Git\cmd\git.exe" status`, `git.exe log`)
- Fixed the bundled `omp://tools` docs still describing the removed `ida` tool; `tools/dsm.md` now documents eval's `dsm` namespace and `disassembler.*` settings, and `tools/read.md` documents metadata-only executable reads ([#19608](https://github.com/can1357/oh-my-pi/issues/19608))
- Fixed native terminal hosts such as Tern placing extension aboveEditor widgets and a blank row between the status row and the tray; the widgets now sit above the status row ([#19767](https://github.com/can1357/oh-my-pi/issues/19767))
- Fixed `^model` mentions in queued messages (`->`/`=>` while the agent is busy, later items of a numbered list, RPC `steer`/`follow_up`, ACP steering) reaching the model as literal `^provider/model` text instead of registering their `m<N>` agent ([#19683](https://github.com/can1357/oh-my-pi/pull/19683) by [@a-glapinski](https://github.com/a-glapinski))
- Fixed `^model` mentions in extension messages sent with `sendUserMessage({ deliverAs: "steer" | "followUp" | "aside" })` while the agent is busy reaching the model as literal text ([#19799](https://github.com/can1357/oh-my-pi/pull/19799) by [@H4vC](https://github.com/H4vC))
- Fixed every message queued behind an undelivered `^model` mention repeating the "`m<N>` now available" notice to the model ([#19799](https://github.com/can1357/oh-my-pi/pull/19799) by [@H4vC](https://github.com/H4vC))
- A plugin manifest with a non-string `extensions` entry (e.g. an object) no longer crashes extension loading with `ERR_INVALID_ARG_TYPE`; the entry is reported as not found and valid entries still load ([#19674](https://github.com/can1357/oh-my-pi/pull/19674) by [@koeria](https://github.com/koeria))
- Fixed embedded `bash script.sh` resolving `BASH_SOURCE[0]` to `bash` instead of the script path, which broke scripts loading files beside themselves ([#19792](https://github.com/can1357/oh-my-pi/issues/19792))
- Fixed proxy model discovery ignoring a gateway's advertised input modalities and output-token cap ([#19754](https://github.com/can1357/oh-my-pi/pull/19754) by [@zhyc9de](https://github.com/zhyc9de)).
- Fixed a provider routed through an auth gateway (`transport: pi-native` in `models.yml`) still listing models from the provider's own endpoint, sending the gateway key there; such providers now skip the provider's model discovery and keep their bundled and cached models ([#19646](https://github.com/can1357/oh-my-pi/pull/19646) by [@ray8828](https://github.com/ray8828))
- Fixed a spurious "cache miss" marker on the first turn after a compaction: compaction rewrites the prompt prefix, so that miss is expected and no longer flagged ([#19679](https://github.com/can1357/oh-my-pi/pull/19679) by [@Petyok](https://github.com/Petyok))
- Fixed `omp --resume <id>` under `--mode rpc`, `--mode rpc-ui` and `--mode acp` failing at start when the session's directory no longer exists; the session now opens where it is stored, with the launch directory as its working directory, without asking whether to move it ([#19651](https://github.com/can1357/oh-my-pi/pull/19651) by [@sjawhar](https://github.com/sjawhar))
- Fixed the browser relay extension dying silently in a browser whose loaded permission set predates the `downloads` permission: it now keeps working without download pairing, and the relay reports a download tracking gap instead of a generic not-found ([#19659](https://github.com/can1357/oh-my-pi/pull/19659) by [@pavel-kalmykov](https://github.com/pavel-kalmykov))
- Sharing a session whose subagents report progress faster than the uplink drains no longer ends with "collab send backlog exceeded its limit" while a guest joins
- Fixed `/loop` iterations and `/goal` continuations firing ~800ms after a turn yields to wait on background subagents or jobs; they now wait until the run finishes ([#19781](https://github.com/can1357/oh-my-pi/issues/19781))
- Fixed Codex and OpenAI API web search ignoring the `web` role's thinking level (`openai-codex/gpt-6-luna:xhigh`); the level now reaches the request as `reasoning.effort` ([#19793](https://github.com/can1357/oh-my-pi/issues/19793))
- Fixed plan review measuring "Approve and keep context" against the pre-plan model instead of the tier chosen in the "continue with" slider, so switching to a larger-context tier now enables it ([#19660](https://github.com/can1357/oh-my-pi/issues/19660))

#### Module: `@oh-my-pi/natives`

##### **Fixed**
- Fixed omp freezing for seconds to minutes on WSL2 while saving sessions: Linux `FileLock` now locks a sidecar file instead of binding a socket, which takes about 10 ms per call there. Older omp versions still running do not see these locks, so restart them after updating ([#19704](https://github.com/can1357/oh-my-pi/pull/19704) by [@turgaybulut](https://github.com/turgaybulut))

#### Module: `@oh-my-pi/snapcompact`

##### **Added**
- `resolveShape()` uses a model's configured `snapcompactShape` in place of its model-line default; an explicit variant still wins and billing still follows the model ([#19591](https://github.com/can1357/oh-my-pi/pull/19591) by [@ryanskidmore](https://github.com/ryanskidmore))

#### Module: `@oh-my-pi/stats`

##### **Added**
- Added 2d and 3d range presets with hourly buckets to the stats dashboard time selector ([#19766](https://github.com/can1357/oh-my-pi/issues/19766), [#19774](https://github.com/can1357/oh-my-pi/pull/19774) by [@thekitaev](https://github.com/thekitaev)).

---

### 🚀 Release `v19.1.0` (2026-11-21)

#### Module: `@oh-my-pi/agent`

##### **Added**
- Added standby tools support through `Agent.setStandbyTools()` and `AgentContext.standbyTools`, allowing tools to remain inactive until a request explicitly enables tool use.

#### Module: `@oh-my-pi/ai`

##### **Added**
- Added provider hooks (`setProviderHooks` in `@oh-my-pi/pi-ai/provider-hooks`), which replace a provider's stream adapter or image generation while its models keep their api.
- Added opt-in prompt perturbation: model-visible prompt prose and tool descriptions use a per-install wording chosen from a committed paraphrase pool covering every static system- and tool-prompt line. Models enable it with the `prompt-perturbation` KDL axis; `OMP_PROMPT_PERTURBATION=1`/`0` forces it on or off.

##### **Changed**
- The Cursor provider forwards `bash` instead of `write` so staged previews can be finalized
- Increased provider stream watchdog defaults from 5 to 15 minutes, preventing slow one-shot completions from being interrupted prematurely.
- Extended Gemini reasoning-stream protection to allow longer planning sequences before interruption.

##### **Fixed**
- Broker-backed credential stores now detect a login the broker stores but does not serve and keep it in the local `agent.db` (`HybridAuthCredentialStore`) instead of losing it on the next snapshot; a broker-only `RemoteAuthCredentialStore` fails the upload with `AuthBrokerUnservedProviderError`.
- OpenAI Codex requests no longer send the `session_id` and `conversation_id` headers; the session goes out only as `session-id`, like the Codex CLI, so proxies that reject underscore header names (Envoy, nginx defaults) pass them ([#20018](https://github.com/can1357/oh-my-pi/issues/20018))
- Preserved the intended conversation structure when a user message follows a tool result for models that fold user messages after tool results.
- LiteLLM requests now rotate to another configured API key when a 422 budget-exceeded response disables the current key. ([#19860](https://github.com/can1357/oh-my-pi/issues/19860))
- GPT-6.2 system prompts are now sent as leading developer messages through third-party Responses proxies, enabling prompt caching and avoiding unnecessary full-rate input charges on subsequent turns. ([openai/codex#62312](https://github.com/openai/codex/issues/62312))
- Improved thinking-mode detection across request formats, avoiding unnecessary retries and correctly remembering formats accepted or rejected by the server. ([#19758](https://github.com/can1357/oh-my-pi/pull/19758) by [@eggpeat](https://github.com/eggpeat))
- Auth refresh failures that could cause an access token to expire before the next retry are now surfaced with a warning instead of remaining visible only in debug logs. ([#19590](https://github.com/can1357/oh-my-pi/pull/19590) by [@will-bogusz](https://github.com/will-bogusz))
- Chat Completions now preserve reasoning returned only in `reasoning_details`, including reasoning from Bifrost Gemini. ([#19595](https://github.com/can1357/oh-my-pi/pull/19595) by [@Xytronix](https://github.com/Xytronix))
- Antigravity quota exhaustion is now reported as a 429 rate-limit error, allowing configured retries, credential rotation, and model fallback behavior to apply correctly instead of treating the response as assistant text. ([#19382](https://github.com/can1357/oh-my-pi/pull/19382) by [@gimso2x](https://github.com/gimso2x))
- Anthropic requests now preserve prompt caching when tools are activated later in a conversation, avoiding unnecessary system-prompt and transcript cache rewrites. ([#19826](https://github.com/can1357/oh-my-pi/issues/19826))

#### Module: `@oh-my-pi/browser-relay`

##### **Breaking Changes**
- The omp extension now uses a pinned Chrome extension ID and connects to the browser relay through its native host. Reinstall the extension using Chrome’s “Load unpacked” flow; the relay port and token options have been removed.

##### **Added**
- Added an omp Chrome side panel with session model selection, role shortcuts, thinking controls, input shortcuts, message queuing, and run interruption controls.
- Added browser interaction features including page overlays, image and element picking, Teach, scheduled shortcuts, and GIF export.

##### **Changed**
- The Chrome side panel shows brief labels for tool steps with structured intents.
- The extension now keeps registered installations up to date across omp upgrades and reloads when idle.
- Browser relay ports are assigned automatically and discovered locally by terminal clients, while sidebar chats continue using their existing connection.
- Side panel sessions now control the connected Chrome browser directly instead of opening a separate headless browser.

##### **Fixed**
- Improved relay recovery so Chrome reconnects automatically when the native host is unavailable or a stale connection drops.

#### Module: `@oh-my-pi/catalog`

##### **Breaking Changes**
- Removed the built-in Gemini CLI OAuth provider (`google-gemini-cli`). Google Antigravity and Antigravity CLI remain available.

##### **Added**
- Added runtime provider rules (`setRuntimeProviderRule` in `compat/cascade`). They apply KDL directives to one provider's models, win ties with bundled rules, and clear rule-derived caches when they change.
- Added the `prompt-perturbation` catalog axis, which opts a provider or model into per-install prompt paraphrasing.
- Added the `uncached-instructions` compatibility flag for GPT-6.2 models across all hosts, moving system prompts out of the uncached Responses `instructions` field.

##### **Fixed**
- Fixed Vercel AI Gateway model refreshes so public models remain discoverable when a stored API key has expired.
- Fixed OpenRouter models that require reasoning but do not advertise effort levels; requests that disable thinking now use the lowest supported reasoning effort instead of failing.
- Fixed Gemini 4 models (Argon, Carbon, Hydrogen, and Neon) failing with empty malformed responses when messages arrived immediately after tool results.
- Updated pricing for newly served Cursor models to use their documented per-token rates instead of being reported as free.
- Fixed Codex client version caching so its cache file is stored under the configured `$XDG_CACHE_HOME/omp` directory.

#### Module: `@oh-my-pi/coding-agent`

##### **Breaking Changes**
- Replaced `xd://` tool devices with tool commands: rarely-used tools now run as bash commands (`<tool> --help`, `<tool> <args>`) while `bash` is active and are ordinary tools otherwise
- Renamed the `tools.xdev`, `tools.xdevDocs`, `tools.xdevInlineDevices` and `tools.xdevNotices` settings to `tools.commands`, `tools.commandDocs`, `tools.commandInline` and `tools.commandNotices`
- Staged previews, plan submission and Auto-QA reports now use the `resolve`, `reject`, `propose` and `report_issue` commands, and tool doc topics moved from `xd://<tool>/<topic>` to `help://<tool>/<topic>`
- Removed the `tui.completeScrollback` setting; transcript rows covered by the HUD, dialogs, or draft now always move to scrollback, and the input returns to the bottom row when overlays close.
- Replaced the standalone MCP transport and tool-cache SDK exports and removed `DeferredMCPTool` plus MCP cache and reconnect-policy manager options. MCP servers are now accessed through the MCP host APIs.
- Browser relay hosting now runs through the omp extension's native host while Chrome is open. Removed the on-demand `omp browser-relay` server command and its `--port`, `--token`, and `--no-group` options; `browser.relayUrl` remains available for relays forwarded from another machine. Reload the omp extension once after upgrading, or restart Chrome.
- Changed `archive.search(query)` to search session titles, idle recaps, and user/assistant content across all history and return matching session records; use `archive.prompts({ query })` for prompt-only searches. Searches match query terms at the beginning of words.
- RPC hosts must handle the `ask` tool as one complete HTML-form `form` request and respond with submitted data or cancellation; field-by-field prompts are no longer emitted.

##### **Added**
- Extensions can take over a built-in provider through `registerProvider`: `stream` replaces its request adapter, `generateImage` its image generation, and `webSearch` its grounded search request, and `discoverModels` its model discovery request. `rules` sets KDL rule directives (such as `prompt-perturbation`) for its models.
- Added the `magic` edit mode, which accepts Markdown bulleted change descriptions grouped under `# path` headings and uses a configurable fast model or role to generate and apply patches. It supports concise block replacement, deletion, movement, and identifier-renaming descriptions, and presents the resulting diffs.
- Added remote session model controls through RPC, including the model picker, thinking-level and role selection, `auto` thinking, and commands to resume, abort while delivering queued messages, or continue the host agent. Collab guests can now continue, interrupt, and queue follow-up prompts for the host.
- Added support for Unicode set mode (`v`) in slash-delimited `secrets.yml` regular expressions.
- Moved MCP servers into the omp daemon, with optional process sharing across sessions, lazy startup, idle shutdown, shared discovery caching, and `/mcp list` status including process and session information. Configure sharing with `mcp.shared` and idle shutdown with `mcp.idleStopMinutes`.
- Added MCP protocol revision 2026-07-28 support, including server discovery, per-request metadata, root input rounds, subscriptions, and cache controls, while retaining compatibility with servers that require the initialize handshake.
- Added native browser-relay integration for the Chrome extension, including side-panel sessions, extension installation and synchronization, automatic profile registration, and in-tab action overlays. Side-panel sessions remain separate from terminal resume, recent-session, `--continue`, and ACP session lists unless explicitly resumed.
- Added a coloured extension-status variant to `omp gallery --segment status`.
- Added notifications and waiting status when a program running in a bash `pty` is waiting for keyboard input, such as a password or confirmation prompt; disable notifications with `pty.notify`.
- Eval `completion()` now records raw provider frames for `/debug` inspection and saves frames from failed calls as log files in the session artifacts directory.
- Added `parentToolCallId` to extension `tool_call` and `tool_result` events so nested tool calls can be associated with the eval cell or kernel-defined tool that dispatched them.
- Added full-text transcript search indexing for `archive.search`, covering user and assistant messages across session history.
- Session files now record approval requests and their outcomes, allowing dashboards and sidebars to show when a session is waiting for tool approval.
- Added live visibility into output redirected to files by background bash jobs, including job streams, the jobs sheet, job widgets, and command cards; selecting a command shows the output for its relevant pipeline or redirected stream.
- Added Binary Ninja as a disassembler backend for read analysis views and the `dsm` namespace. Select it with `disassembler.backend = binja` and configure its installation with `binja.installDir` or `$BN_INSTALL_DIR`.
- Clicking the usage-limit segment in native terminal hosts such as Tern now opens `/usage`. Changing Tern's Agents tray setting immediately switches between tray cards and the running-agent and job counters without restarting omp.

##### **Changed**
- Images a command prints as kitty or sixel graphics are saved to a temp file and linked in the bash output, in addition to being attached
- `generate_image` returns its images as attachments
- Spotlight tool calls use `Label: detail`; activity shows only the label, while output ranking uses the full intent.
- Improved regex performance for TTSR and secret-redaction scans, including SIMD acceleration and faster candidate matching, without changing matching semantics.
- Improved performance when listing sessions across all projects, especially with thousands of project directories.
- Interactive `wait` now waits up to four minutes on its first call for background jobs instead of returning after five seconds.
- Updated the MCP OAuth client name to `Codex`.
- Made automatic retries less disruptive: failed attempts stay out of the transcript, retry status explains the reason, and successful recovery leaves only a brief indication.
- Selective commits now attribute edit-tool and shell-built-in changes more accurately, distinguish external program changes for review, and use a substantially smaller change journal. Long-line commit previews now highlight only the changed words while preserving the original patch.
- TTSR rules that cannot interrupt streaming are evaluated at the end of the relevant response, reasoning, or tool call, reducing unnecessary work while preserving matches and reminders.
- Eval `completion()` now accepts user-tagged model agents, such as models pinned with `^model`, and uses their tagged effort level.
- `read` recognizes SQLite-backed `.i64` and `.idb` files as IDA databases and reports disassembler-backend mismatches clearly.

##### **Fixed**
- A tool card left unfinished by a stream that never completed no longer keeps the rest of the transcript out of scrollback and squeezed to one-line rows; it is closed when the next reply starts
- Spotlight keeps short relevant passages from multiple large function bodies together with their signatures, even when a code outline is cut again.
- A usage-limit reset inside `retry.maxDelayMs` is now waited out even without a `Retry-After` header.
- Logging in while an auth broker is configured no longer reports success for a provider the broker stores but does not serve (such as one an older broker pauses); the login is kept in this machine's `agent.db` instead, survives restarts, and login/logout now name where credentials were saved.
- Spotlight keeps more high-relevance lines with their neighbours in long results and large code outlines, while preserving visible intent matches within the window budget.
- Fixed Tern tray cards and subagent live previews showing stale calls, models, or thinking states while an agent was running or after a model switch; completed cards now retain the model and thinking level used.
- Fixed extension side-panel sessions launching omp's own browser instead of driving only the user's Chrome window.
- Preserved answer footers and Copy controls in Tern after resuming, compacting, or rebuilding a transcript.
- Prevented `--continue` and `autoResume` from attaching to a session currently being written by another omp process.
- Added visible progress reporting while `/handoff` writes its summary.
- Fixed access to cloud-only files on macOS iCloud Drive, Desktop & Documents, Google Drive, and Dropbox locations.
- Prevented pathological TTSR condition and secret-redaction regular expressions from freezing sessions or requests.
- Fixed prompt-cache handling for IRC-woken subagents and sessions whose context hooks provide an initial message.
- Improved shell `rg` and `fd` path output and option handling to match their native tools, including paths beginning with `-`, null-separated output, and explicit current-directory prefixes.
- Fixed sloppy-edit validation and block matching for incomplete actions, numeric `||` expressions, nested or partial block endings, JSDoc comments, and hashline headers with trailing whitespace.
- Fixed OpenCode v2 MCP configuration discovery from `mcp.servers` while preserving support for legacy flat `mcp` entries.
- Fixed `ovnfs` commands when `ovnfs.path` contains Windows backslashes, spaces, or `$` characters.
- Stopped failed browser launches from logging URL credentials, query strings, OAuth device codes, or fragments.
- Fixed `web_search` to honor the search order and exclusions configured for the current session.
- Fixed MCP OAuth refresh for Microsoft Entra servers where the client is also the resource; previously saved credentials may require one `/mcp reauth`.
- Fixed model resolution for OpenRouter route variants used by per-call subagents and roles.
- Fixed secret redaction in shared sessions so provider-encrypted reasoning is not retained unexpectedly.
- Fixed bash approval handling for compound commands with environment assignments and flags, including wildcard allow rules.
- Fixed selective commits when HEAD changes during a commit hook and when edits from multiple writers are reordered or overlap; ambiguous changes are now sent to review instead of being duplicated or silently misapplied.
- Fixed archive records to include all documented keys with `null` for missing values.
- Fixed unnecessary empty session log files for inline bash/eval output and request-timeout recovery.
- Improved `read` suggestions for line, range, and column selectors and preserved source line metadata for in-memory and converted text reads.
- Fixed agent lifecycle races involving duplicate IDs, pending messages, shutdown, and revival.
- Fixed browser tab handling on CDP engines that use separate connections per page, including recovery after timeouts or worker exits.
- Fixed browser interaction reporting for overlay-only clicks, hidden frames containing inline SVG or MathML, and search fields that update on key events.
- Fixed browser computer-use inspection of minimized macOS windows and fully covered Windows Chrome, Edge, and Electron windows.
- Fixed `/goal` on Anthropic from unnecessarily rewriting the cached system prompt and transcript.
- Fixed isolated task subagents in bare Git repositories by refusing early and identifying available work trees instead of starting without a usable work tree.
- Fixed Nix browser-relay builds to fetch all dependencies without falling back to the npm registry.
- Fixed extension, plugin, custom-tool, hook, command, and share-script loading for paths containing `?`, with a useful error identifying the path and remedy.

#### Module: `@oh-my-pi/collab-web`

##### **Added**
- Enhanced guest collaboration APIs: `GuestClient.sendPrompt` now supports sending images, while `sendResume`, `sendDeliverQueue`, and the `followUp` option enable continuing the host’s agent, interrupting it to deliver queued messages, or queueing a follow-up prompt.

##### **Changed**
- Tool commands run inside a bash call render as nested cards under the bash card
- Tool cards in shared sessions and HTML exports show brief intent labels instead of detailed ranking instructions.

#### Module: `@oh-my-pi/mnemopi`

##### **Fixed**
- Improved diagnostics when a configured embedding provider fails, making provider errors visible in logs while preserving the existing fallback behavior.

#### Module: `@oh-my-pi/natives`

##### **Added**
- Added host-provided session commands to `Shell.run` (`commands`) and `shellReservedCommandNames()`

##### **Fixed**
- Fixed grouped `sed` scripts such as `1{h;d};2{G}` being rejected when no semicolon precedes a closing brace.
- Fixed the native addon failing to load when `HOME`, `PI_NATIVES_DIR`, or the installation path contains `?`.
- `commitCreate()` now reports a `HeadMoved` error when `HEAD` changes after the expected-HEAD check, including changes made by a `commit-msg` hook.
- Fixed macOS window reads for minimized windows so the requested window remains inspectable without being restored or replaced by a sibling window; unavailable menus and commands now report `WindowUnavailable`.
- Fixed Windows captures and accessibility trees incorrectly reporting fully covered Chromium and Electron windows as current; they now report `covered` when those applications stop drawing while covered.
- Fixed Windows `computer` `setValue` bringing classic Win32 and WinForms text-box windows to the foreground and directing subsequent keyboard input into them.

#### Module: `@oh-my-pi/utils`

##### **Added**
- Added `LinearRegExp` (`@oh-my-pi/pi-utils/regex`), a JavaScript-compatible regular expression engine that avoids catastrophic backtracking, with support for scoped modifiers, Unicode modes and properties, Unicode set operations, large repetitions and literal dictionaries, fixed-width block counts, and additional character classes.
- Added `RegexStream` for detecting regular-expression matches in text received incrementally in chunks.
- Added `getCodexClientVersionPath()` to locate the Codex client version cache record under the initialized `$XDG_CACHE_HOME/omp` directory.

##### **Changed**
- Improved `LinearRegExp` performance for scans and searches involving delimiters, word backreferences, required literals or suffixes, lookbehinds, and large character alphabets.

##### **Fixed**
- Fixed RAR4 extraction stalling for seconds per filter on archives that declare an out-of-range delta filter channel count; such archives are now rejected as corrupt.
- Fixed `formatAge` to display durations of one year or more in years, such as `23y ago`, instead of months.

#### Module: `@oh-my-pi/wire`

##### **Added**
- Added `toolIntentLabel` for displaying the brief prefix of a structured tool-call intent.
- Added clickable shell-command steps with output selection and visual highlighting of the currently displayed step.
- Added a terminal `features` event for notifying clients when terminal settings change.
- Added collaboration guest support for resuming sessions and delivering queued messages, plus `followUp` prompts.

---

### 🚀 Release `v19.1.1` (2026-11-23)

#### Module: `@oh-my-pi/agent`

##### **Fixed**
- Prevented oversized handoffs from reaching the provider by detecting when prepared context exceeds the target model’s context window.
- Preserved provider error status, error identifiers, retry classification, and cancellation markers on failed or cancelled assistant turns.
- Fixed speculative tool calls hanging when discarded or aborted before execution completed.

#### Module: `@oh-my-pi/ai`

##### **Added**
- Added `AssistantMessage.requestId`, populated from Anthropic’s `request-id` response header, so failed or refused requests retain the identifier needed for Anthropic support.
- Added `GET /v1/pi/models` to `omp auth-gateway`, serving the gateway's model catalog (limits, thinking levels, pricing) to pi-native clients.

##### **Changed**
- Devin account selection now prioritizes logins with remaining daily or weekly quota, then accounts funded by on-demand balance, while skipping accounts with no available capacity. Devin logins also track email, user ID, and organization so separate organizations are distinguishable in `omp usage` and `auth.accountPolicies`; existing logins must be reauthenticated to populate this information.
- Billing failures from providers are now treated as usage limits, allowing retries to rotate accounts and continue through the model fallback chain.
- Provider usage reports registered by extensions now persist across omp processes, avoiding unnecessary repeated usage-endpoint checks.
- Requests that stall during provider operations are now classified as timeouts, allowing automatic fallback to another model.
- Reduced idle memory usage by loading prompt-perturbation data only when perturbation is enabled for a request.

##### **Fixed**
- Fixed split tool-call handling so models configured with `splitToolCalls` receive each tool call together with its corresponding result in the correct message order.
- Fixed `apple/on-device` finish-reason handling so requests no longer emit spurious stderr warnings and correctly report recognized stop or length completions.
- Improved local validation for empty Anthropic requests by reporting the model, provider, and received message count instead of an opaque provider error.
- Fixed OpenAI and Codex requests failing on MCP tool schemas containing unsupported unescaped character patterns.
- OpenRouter Responses requests that end in an unbilled encrypted reasoning item now surface the underlying provider failure instead of completing silently.
- Fixed preservation of Gemini thought signatures across tool calls when using Portkey or the authentication gateway.
- Fixed the thinking-loop guard incorrectly retrying final answers containing long Markdown tables or similarly shaped JSON records.
- Fixed strict tool-schema conversion so object properties that accept arbitrary fields are not incorrectly restricted to empty objects.
- Fixed `antigravity-cli` models failing to receive images returned by tools such as `read`.
- Fixed transient proxy errors from disrupting snapshot streaming and disabling usage reporting for the remainder of the process.
- Fixed concurrent Antigravity CLI sessions for the same account failing during credential staging.
- Fixed OpenAI Codex WebSocket continuations so sticky turn routing information is preserved for subsequent requests.
- Improved recovery from a corrupt `agent.db` so readable provider credentials are restored where possible and disabled credentials remain disabled.

#### Module: `@oh-my-pi/browser-relay`

##### **Fixed**
- The side panel’s Connection settings now show the browser’s specific reason when it refuses the native host (for example, because native messaging is blocked by enterprise policy), instead of incorrectly suggesting that the host may be missing.

#### Module: `@oh-my-pi/catalog`

##### **Added**
- Z.AI (`zai`) now discovers the models available to your GLM Coding Plan key, so newly released GLM models appear without waiting for a catalog update.
- Added `getUpstreamPin()` and `routedModelsAreEqual()` to `@oh-my-pi/pi-catalog/models` for distinguishing aggregator models routed to different upstream providers.
- Added `@oh-my-pi/pi-catalog/discovery/pi-native` and `piNativeModelManagerOptions()` for reading a provider's model roster from an auth gateway's `GET /v1/pi/models`.

##### **Fixed**
- Fixed Llama 3.x models failing after turns that invoked multiple tools when served through vLLM-based hosts, including CoreWeave through OpenRouter.
- Devin usage is now kept separate for organizations that share the same email address.
- Updated Devin image token accounting to match Devin’s published 1,089-token charge per image across supported Gemini image models.
- Corrected Devin pricing and context limits for GPT-5.6 Sol, Terra, and Luna Fast lanes, including long-context rates above 272K input tokens and the standard 272K limit when Extended Context is disabled.
- Corrected Cursor pricing for GPT-5.6 Sol, Terra, and Luna models so output above 272K input tokens uses the documented 1.5× rate.
- Turning thinking off for GPT-6.1 Terra now uses the supported `none` reasoning effort.
- Fixed GPT-6.2 and later OpenAI Responses models losing reasoning context after session pruning and subsequent tool calls.
- Corrected Bedrock Kimi K3.1 Pro Highspeed reasoning options and effort handling.
- GitHub Copilot now lists only models available to the account, including after restarting.
- Codex models discovered before being bundled now use their formatted display names, such as `GPT-6.2 Sol`.
- Fixed Bedrock Kimi K3.1 requests that set a temperature (history summaries, skill routing hints) failing with "This model doesn't support the temperature field" ([#20239](https://github.com/can1357/oh-my-pi/issues/20239))
- Fixed Llama 3.x models failing with "This model only supports single tool-calls at once!" after a turn that called several tools, on hosts serving them through vLLM (such as CoreWeave behind OpenRouter)
- Devin usage from two organizations under one email is no longer merged into one account ([#19928](https://github.com/can1357/oh-my-pi/pull/19928) by [@will-bogusz](https://github.com/will-bogusz))
- Devin's Gemini 4 Neon images are now budgeted at the 1,089 tokens Devin bills per image, measured across sizes, instead of the unverified 1,120-token Gemini estimate ([#19883](https://github.com/can1357/oh-my-pi/pull/19883) by [@will-bogusz](https://github.com/will-bogusz))
- Devin's Gemini 4 Hydrogen and Argon and Gemini 3.5 and 3.8 Flash images are now budgeted at the 1,089 tokens Devin bills per image, measured across sizes, instead of the unverified 1,120-token Gemini estimate ([#20038](https://github.com/can1357/oh-my-pi/pull/20038) by [@will-bogusz](https://github.com/will-bogusz))
- Devin's GPT-5.6 Sol, Terra and Luna Fast lanes are now costed at Devin's published long-context rates above 272K input tokens and, with Extended Context off, capped at 272K like the standard lanes ([#20094](https://github.com/can1357/oh-my-pi/pull/20094) by [@will-bogusz](https://github.com/will-bogusz))
- Devin's GPT-5.6 Sol is costed above 272K input tokens at Devin's published $8 / $30 rate instead of $10 / $45 derived from its new standard-context price ([#20094](https://github.com/can1357/oh-my-pi/pull/20094) by [@will-bogusz](https://github.com/will-bogusz))
- Cursor's GPT-5.6 Sol, Terra and Luna (standard and Fast) now price output above 272K input tokens at 1.5x the base rate, as each model's Cursor docs page publishes, instead of the base rate ([#20093](https://github.com/can1357/oh-my-pi/pull/20093) by [@will-bogusz](https://github.com/will-bogusz))
- Turning thinking off on GPT-6.1 Terra now sends reasoning effort `none`, which the model supports, instead of falling back to `low` ([#20144](https://github.com/can1357/oh-my-pi/pull/20144) by [@Komzpa](https://github.com/Komzpa))
- Fixed GPT-6.2 and later OpenAI Responses models lacking thinking prefix-binding, so sessions pruned already-sent tool results and the API dropped later reasoning items ([#19721](https://github.com/can1357/oh-my-pi/issues/19721), [#19988](https://github.com/can1357/oh-my-pi/pull/19988) by [@JamieJ5926](https://github.com/JamieJ5926))
- Fixed Bedrock's Kimi K3.1 Pro Highspeed profiles missing the `xhigh` and `max` reasoning efforts, offering an unsupported `minimal`, and sending token budgets instead of effort controls ([#19998](https://github.com/can1357/oh-my-pi/pull/19998) by [@alblez](https://github.com/alblez))
- Fixed GitHub Copilot listing bundled models the account's `/models` roster omits, and models Copilot disables for the account, including after a restart ([#14832](https://github.com/can1357/oh-my-pi/issues/14832), [#19984](https://github.com/can1357/oh-my-pi/pull/19984) by [@JamieJ5926](https://github.com/JamieJ5926))
- Fixed Codex models discovered before they are bundled for `openai-codex` showing Codex's slug-style name, e.g. `GPT-6.2-Sol` instead of `GPT-6.2 Sol` ([#20167](https://github.com/can1357/oh-my-pi/issues/20167))

#### Module: `@oh-my-pi/coding-agent`

##### **Breaking Changes**
- The native shell Rust API now stores indexed variables as `IndexedArray` instead of `Vec`; construct `VarValue::Indexed` values with `items.into()`.

##### **Added**
- Added the opt-in `tree` status segment, which shows a session’s position in the session tree after a rewind or on a branch; in Tern, the segment opens `/tree` when clicked.
- Providers routed through an auth gateway (`transport: pi-native`) now list the gateway's models, so models the gateway discovered at runtime (such as new Codex models) can be selected without declaring them in `models.yml`, and models the gateway cannot route are hidden.
- Added `computer.takeover` as the replacement for `computer.backgroundFallback`, with `fallback`, `foreground`, and `always` modes for controlling when the computer tool takes over the foreground window. Existing fallback behavior is preserved by default.
- Added a portable `column` shell builtin with util-linux-compatible options, including table formatting, named columns, alignment, hiding, ordering, JSON output, tree display, and width controls.
- Added extension todo backends through `pi.registerTodoBackend()` and the `todo.backend` setting. Registered backends can mirror the session’s complete todo list to an external store and can be selected and configured from `/settings` → Tools → Todos.
- `/wt` now runs the new worktree’s `post-checkout` hook, displays progress in the TUI, and loads skills and commands created by the hook. Failed hooks leave the worktree intact and display a warning.

##### **Changed**
- Empty-stop recovery now records each retry with the selected model, provider, and stop metadata, making repeated empty model responses visible in the session log.
- The quick model picker refreshes stale provider catalogs in the background, so long-running sessions can discover newly available models.
- On Linux, language-server file watching now adapts to the inotify watch limit so large workspaces are less likely to interfere with other file watchers and system services.
- The `eval` tool now documents its default 30-second cell deadline in its prompt and timeout parameter.

##### **Fixed**
- Improved Magic Edit so it can search and read the current draft, retry failed replacements without losing successful edits, validate syntax before writing, and support models that emit tool calls as text.
- Fixed shell tool command handling when `bash` is replaced by an extension, including support for tool-only command lines with remote or sandboxed shells.
- Fixed browser scrolling validation and documentation so invalid object forms explain the correct pixel-delta signature and equivalent call.
- Fixed `ask` handling of fieldsets whose radio buttons use different names, preventing a preselected option from being submitted alongside the user’s choice.
- Fixed title generation to stop when a model explicitly declines with `<title/>` or `none`, while continuing to the next candidate for errors or unusable replies.
- Fixed automatic and speculative compaction so oversized or non-retriable handoff requests move on to the next available compaction method instead of being repeatedly sent to a provider.
- `wait()` in eval cells now accepts displayed subagent IDs, including the `agent://id` form, while still rejecting handles belonging to other sessions.
- Fixed startup and session model configuration so thinking levels, model-provider ordering, enabled-model allowlists, routed selections, and pinned upstream routes remain consistent across model switches, cycling, restore, plan mode, and metadata refreshes.
- Fixed queued follow-up messages being lost when interrupted responses are discarded, and fixed TTSR interruptions that could leave a session unable to continue.
- Fixed OpenAI Responses sessions rewriting previously sent tool results, which could cause later reasoning items to be rejected.
- Fixed format-on-write and symlink-related file editing issues, including incorrect write failures, missing snapshots, duplicated `local://` paths, and incorrect symlinked filenames in previews and journals.
- Fixed Windows browser downloads occasionally retaining temporary GUID filenames when the downloaded file was briefly locked.
- Fixed RPC shutdown leaving MCP subprocesses running after the session ended.
- Fixed advisor and Spotlight output so truncated or repeated tool results are represented accurately without losing the original content.
- Fixed first-run startup warnings that persisted after a default model had been selected.
- Fixed context rollover handling so concurrent bookkeeping no longer silently drops an explicit rollover, and skipped rollovers produce a warning.
- `/omfg` now closes its panel after successfully saving a rule and shows the saved path; errors keep the panel open.
- Fixed shell handling of leading `cd` commands that use glob, brace, or named-user home expansion.
- Claude-format plugin agents now correctly map Claude tool names such as `WebFetch`, `WebSearch`, `TodoWrite`, `AskUserQuestion`, `MultiEdit`, and `Agent` to their OMP equivalents.
- Startup extension notifications now remain visible instead of being overwritten by later notices or MCP startup status.
- Fixed CLI parsing so `--plan` no longer consumes a following CLI flag as its value during startup, restart, fork, or subcommand routing.
- Fixed `/usage` when the usage database is temporarily locked; stored history remains visible and is marked unsynced if it cannot be refreshed.
- Model discovery now classifies speech-only and transcription-only models as TTS and STT models rather than chat models.
- Subagents stopped by their parent now record that they were stopped by the parent agent.
- Fixed SDK and extension imports, examples, and session-specific extension discovery for RPC and ACP sessions.
- Fixed X and YouTube URL reads to honor SDK session settings even when global settings have not been initialized.
- Restored sessions now correctly report background jobs whose outcome is unknown, and `omp --restore` no longer replays completed turns after idle compaction or interruption.
- Selective commits now preserve the drafted contents and Git clean-filter results for binary, non-text, oversized, and Git LFS files, and avoid overwriting files changed since the draft was created.
- Fixed `read` hanging on images and other non-text files when speculative execution and `beforeToolCall` hooks are enabled.
- Provider error logs now include the request ID needed for troubleshooting Anthropic refusals.
- Sessions started from collaboration prompts now receive automatic titles.
- Fixed `/tan` forks ending an idle wait prematurely when their assignment remains blocked.
- Fixed ACP sessions using the launch directory's `enabledModels` for model selection and cycling instead of their own workspace's ([#20106](https://github.com/can1357/oh-my-pi/pull/20106) by [@taibenvenuti](https://github.com/taibenvenuti))
- Fixed ACP `--api-key` being copied to whichever provider each session selected: the key stays on the provider named by `--model` or the launch directory's scope, a workspace that would start on another provider is refused with `--api-key is bound to X, not Y`, and a launch scope naming several providers fails with `--api-key requires exactly one enabled provider in the launch scope` ([#20106](https://github.com/can1357/oh-my-pi/pull/20106) by [@taibenvenuti](https://github.com/taibenvenuti))
- Fixed applying a model preset writing its roles before checking the default it leaves in effect; a preset whose default would fall outside the resulting roles or `enabledModels` allowlist (including through a role alias such as `@slow`) now leaves settings untouched ([#20107](https://github.com/can1357/oh-my-pi/pull/20107) by [@taibenvenuti](https://github.com/taibenvenuti))
- Fixed the `enabledModels` cycling scope going stale after a preset or model hub edit changes a role that an `enabledModels` alias refers to, and the model hub resolving its default fallback against such a stale scope ([#20107](https://github.com/can1357/oh-my-pi/pull/20107) by [@taibenvenuti](https://github.com/taibenvenuti))
- Fixed `wait` on a finished background job logging "Async job completion delivery failed" with a retry that never runs. A push that a `wait` or job snapshot already collected now logs "Async job completion delivery superseded" at debug level. The failure warning names `nextRetryAt` only when it queued a retry ([#20245](https://github.com/can1357/oh-my-pi/pull/20245) by [@nick-maderight](https://github.com/nick-maderight))
- Magic edit can now search and read the current draft, retry failed replacements without losing successful ones, and check syntax before writing; apply models that write their tool calls as text, such as Gemma 3, work too, and small apply models are shown where a mistyped replacement's text actually is instead of retrying it blindly.
- An extension that re-registers `bash` no longer turns tool commands off for the whole session, which pushed every MCP tool back into the top-level definitions of each request. A command line made only of tool commands now runs on the native tool, so a replacement that never delegates — a remote or sandboxed shell — serves the mounted tools too, while every other command line stays its own ([#18339](https://github.com/can1357/oh-my-pi/issues/18339), [#20174](https://github.com/can1357/oh-my-pi/pull/20174) by [@kaluli123123](https://github.com/kaluli123123))
- `tab.scroll({ direction: "down", amount: 600 })` and other objects that name no pixel delta are rejected with the helper's signature and the equivalent call (`tab.scroll(0, 600)`) instead of silently scrolling nothing; the browser docs point at the `TabApi` interface in `tab-worker.ts` instead of a declaration file that no longer exists ([#20171](https://github.com/can1357/oh-my-pi/pull/20171) by [@kaluli123123](https://github.com/kaluli123123))
- `ask` now reports a `<fieldset>` whose radios each carry a different `name` back to the model instead of showing it, so a preselected option can no longer be submitted next to the user's pick as a second answer ([#19625](https://github.com/can1357/oh-my-pi/issues/19625), [#20170](https://github.com/can1357/oh-my-pi/pull/20170) by [@kaluli123123](https://github.com/kaluli123123))
- Title generation stops after a model declines with `<title/>` or `none`, instead of sending the same request to every remaining title candidate, including fallback chains and the session model; errors and unusable replies still move on to the next candidate ([#20168](https://github.com/can1357/oh-my-pi/issues/20168)).
- Automatic compaction moves past an oversized handoff request without calling the provider ([#20099](https://github.com/can1357/oh-my-pi/issues/20099)).
- `wait()` in eval cells accepts a displayed subagent id, optionally as `agent://id`, so you can wait for an agent you only have the name of; ids that are not yours still report an unknown handle ([#20148](https://github.com/can1357/oh-my-pi/pull/20148) by [@Komzpa](https://github.com/Komzpa))
- Fixed the startup thinking level coming from the first `--models`/`enabledModels` entry instead of the entry the session starts on, such as a remembered default that is not listed first, and replacing the level given with `--model` ([#20109](https://github.com/can1357/oh-my-pi/pull/20109) by [@taibenvenuti](https://github.com/taibenvenuti))
- Fixed TTSR discard mode dropping follow-up messages queued while an interrupted response was unwinding ([#20131](https://github.com/can1357/oh-my-pi/pull/20131) by [@harshaygadekar](https://github.com/harshaygadekar))
- Fixed automatic compaction repeating a handoff request too large for the model after a cross-provider switch; it now moves on to the next compaction method ([#20126](https://github.com/can1357/oh-my-pi/pull/20126) by [@harshaygadekar](https://github.com/harshaygadekar))
- Upstream pins (`openrouter/z-ai/glm-4.7@cerebras`) survive model switches, cycling, session restore, prewalk, plan mode, and model metadata refreshes; `enabledModels` and `--models` keep two pins of one model distinct and never re-pin a listed route ([#19664](https://github.com/can1357/oh-my-pi/pull/19664) by [@taibenvenuti](https://github.com/taibenvenuti)).
- Fixed MCP servers that reject the 2026-07-28 revision, such as Datadog, failing to connect instead of falling back to the handshake-era protocol ([#20113](https://github.com/can1357/oh-my-pi/pull/20113) by [@DanielTatarkin](https://github.com/DanielTatarkin))
- Resuming in plan mode now remembers the model and thinking level to restore when planning ends, including routed model selections ([#20114](https://github.com/can1357/oh-my-pi/pull/20114) by [@SuperUserA](https://github.com/SuperUserA))
- Fixed the `enabledModels` allowlist (`/model` and the RPC and ACP model lists) ignoring `modelProviderOrder` for an ambiguous entry, so it could pick a different provider than the cycling scope; editing `modelProviderOrder` now refreshes a cycling scope derived from `enabledModels` ([#20108](https://github.com/can1357/oh-my-pi/pull/20108) by [@taibenvenuti](https://github.com/taibenvenuti))
- Reduced idle memory of compiled binaries and the npm bundle by loading the browser-relay extension only when it is installed or synced ([#20089](https://github.com/can1357/oh-my-pi/pull/20089) by [@iliaal](https://github.com/iliaal))
- A background wake can retry its own empty model responses even if the previous turn exhausted its retries ([#19997](https://github.com/can1357/oh-my-pi/pull/19997) by [@ashtacore](https://github.com/ashtacore))
- Fixed GPT-6.2 sessions on the OpenAI Responses APIs rewriting already-sent tool results every turn, which made the API drop later reasoning items; superseded reads now stay as they were sent while the prompt cache is warm ([#19721](https://github.com/can1357/oh-my-pi/issues/19721), [#19988](https://github.com/can1357/oh-my-pi/pull/19988) by [@JamieJ5926](https://github.com/JamieJ5926))
- Fixed a session-only model pick or quick-role pick recording a second model change when Enter was pressed again before the switch finished ([#12310](https://github.com/can1357/oh-my-pi/issues/12310), [#19986](https://github.com/can1357/oh-my-pi/pull/19986) by [@JamieJ5926](https://github.com/JamieJ5926))
- Fixed `edit` reporting a failed disk write when format-on-write restored the file's original content ([#20059](https://github.com/can1357/oh-my-pi/pull/20059) by [@eggpeat](https://github.com/eggpeat))
- Fixed browser downloads keeping their GUID temp name when Windows held the downloaded file open without share-delete at finalize time; the atomic replace now retries the rename within its budget ([#20062](https://github.com/can1357/oh-my-pi/pull/20062) by [@jchanghong023](https://github.com/jchanghong023))
- Fixed RPC mode exiting before its private MCP host finished reclaiming servers, which could orphan MCP subprocesses after the session ended ([#20067](https://github.com/can1357/oh-my-pi/pull/20067) by [@jchanghong023](https://github.com/jchanghong023))
- Fixed the advisor reading the lines its own view cut from a tool result as missing from the main thread: they are now labelled as cut in the advisor view only, and a tool's own truncation is still named ([#12777](https://github.com/can1357/oh-my-pi/issues/12777), [#19982](https://github.com/can1357/oh-my-pi/pull/19982) by [@JamieJ5926](https://github.com/JamieJ5926))
- Fixed the "No default model selected" startup warning still showing after first-run setup had selected a model ([#8053](https://github.com/can1357/oh-my-pi/issues/8053), [#19985](https://github.com/can1357/oh-my-pi/pull/19985) by [@JamieJ5926](https://github.com/JamieJ5926))
- Fixed `new_context` silently dropping the rollover when a non-message journal append (goal mode usage bookkeeping) raced the experimental leaf guard; journal appends no longer abort the boundary, a transcript append still does, and a skipped explicit rollover now warns instead of looking successful ([#20063](https://github.com/can1357/oh-my-pi/issues/20063))
- Fixed the bash tool treating leading `cd` targets with active glob, brace, or named-user home expansion as literal working directories; these commands now stay with the shell ([#20024](https://github.com/can1357/oh-my-pi/pull/20024) by [@eggpeat](https://github.com/eggpeat))
- Fixed AST edits and searches across several targets duplicating explicit `local://` file names (such as `local://example.ts/example.ts`) or replacing symlinked file names in previews, search results, and the edit journal ([#20025](https://github.com/can1357/oh-my-pi/pull/20025) by [@eggpeat](https://github.com/eggpeat))
- Fixed Claude-format plugin agents losing tools whose Claude Code names match no OMP built-in: frontmatter `tools:` now translates `WebFetch`, `WebSearch`, `TodoWrite`, `AskUserQuestion`, `MultiEdit`, `Agent`, and the rest to their OMP equivalents, and `Agent` infers unrestricted spawns like `Task` ([#19887](https://github.com/can1357/oh-my-pi/pull/19887) by [@joseotaviorf](https://github.com/joseotaviorf))
- Fixed a TTSR rule interrupt that matched a tool call leaving the session idle with `Cannot continue from message role: assistant` instead of retrying the turn with the rule ([#19875](https://github.com/can1357/oh-my-pi/issues/19875))
- Extension `ctx.ui.notify(…, "info")` notices shown at session start stay visible instead of being overwritten by the next extension's notice or the MCP startup status line ([#19866](https://github.com/can1357/oh-my-pi/issues/19866))
- Passing `--plan` before another CLI flag no longer treats that next flag as `--plan`'s value during startup, `/restart`, `/fork`, or subcommand routing ([#20028](https://github.com/can1357/oh-my-pi/pull/20028) by [@eggpeat](https://github.com/eggpeat))
- Fixed the edit tool not finding the snapshot it recorded for a file created beneath a symlinked ancestor, such as a new file under `/var/...` on macOS ([#19926](https://github.com/can1357/oh-my-pi/pull/19926) by [@FnSGit](https://github.com/FnSGit))
- Fixed `/usage` showing "Usage history unavailable (database is locked)" while another process was writing the stats database; the stored history stays visible, marked not synced when the refresh cannot finish ([#19896](https://github.com/can1357/oh-my-pi/pull/19896) by [@Xytronix](https://github.com/Xytronix))
- `openai-models-list` discovery no longer offers a gateway's speech and transcription models as chat models: rows whose only output is `speech` or `transcription` (including OpenRouter's `text->speech` style `architecture.modality` summary) become `tts` and `stt` models ([#19900](https://github.com/can1357/oh-my-pi/pull/19900) by [@Xytronix](https://github.com/Xytronix))
- Subagents stopped by their parent through `proc://<id>/kill` now record "Stopped by parent agent" in their transcripts instead of "Interrupted by user" ([#20012](https://github.com/can1357/oh-my-pi/pull/20012) by [@nick-maderight](https://github.com/nick-maderight))
- Fixed the omp daemon staying alive for up to 3 seconds after shutdown, or 11 seconds after stopping a module unit such as the image URL broker, once its work was done
- Reduced idle memory of the npm bundle and compiled binaries by reading the prompt perturbation pool only when a request is perturbed ([#20090](https://github.com/can1357/oh-my-pi/pull/20090) by [@iliaal](https://github.com/iliaal))
- On Linux, language-server file watching in one omp process holds at most a quarter of the user's inotify watch limit, and gives half of its watches back when the limit is reached, so large workspaces no longer break `tail -f`, systemd, or CI containers of the same user ([#20117](https://github.com/can1357/oh-my-pi/issues/20117))
- Fixed importing `@oh-my-pi/pi-coding-agent` from npm failing with `Cannot find module '../../../../../browser-relay/extension/messages'` ([#20058](https://github.com/can1357/oh-my-pi/issues/20058))
- Fixed the `read` tool's `:raw` description claiming line anchors and prefixes are omitted even when the active session does not emit them ([#20101](https://github.com/can1357/oh-my-pi/pull/20101) by [@eggpeat](https://github.com/eggpeat))
- In SDK, RPC and ACP sessions, MCP servers rediscovered after a mid-session settings change (project MCP config or the built-in browser) now come from the session's own extension paths and honor `disableExtensionDiscovery`, instead of the globally discovered extensions ([#20116](https://github.com/can1357/oh-my-pi/pull/20116) by [@eggpeat](https://github.com/eggpeat))
- Fixed TTSR discard mode dropping messages admitted after an interrupted assistant, while ensuring the interrupted assistant, its tool results, and any empty aborted tail are cleanly removed ([#20131](https://github.com/can1357/oh-my-pi/pull/20131) by [@harshaygadekar](https://github.com/harshaygadekar))
- Fixed the `computer` tool's instructions listing `(selected)` as a macOS-only `ax()` state; Linux elements now show it too ([#20110](https://github.com/can1357/oh-my-pi/pull/20110) by [@will-bogusz](https://github.com/will-bogusz))
- Fixed published SDK and extension examples that used removed APIs, and included them in the package typecheck ([#20060](https://github.com/can1357/oh-my-pi/pull/20060) by [@eggpeat](https://github.com/eggpeat))
- Speculative compaction no longer re-sends a `compaction.remoteEndpoint` request after the endpoint rejects it with a non-retriable error, such as a 404 or 400 for the session's model; it speculates the next configured method until a compaction commits ([#20011](https://github.com/can1357/oh-my-pi/pull/20011) by [@nick-maderight](https://github.com/nick-maderight)).
- Fixed X and YouTube URL reads ignoring SDK session settings or failing when global settings were not initialized ([#20057](https://github.com/can1357/oh-my-pi/pull/20057) by [@eggpeat](https://github.com/eggpeat))
- Spotlight now keeps edit results and tool error responses whole instead of replacing repeated lines with references to earlier output ([#20032](https://github.com/can1357/oh-my-pi/pull/20032) by [@eggpeat](https://github.com/eggpeat))
- Restored sessions now report background bash jobs left unfinished when the previous OMP process exited through `wait` and `proc://` as having an unknown outcome instead of claiming they never existed ([#20026](https://github.com/can1357/oh-my-pi/pull/20026) by [@eggpeat](https://github.com/eggpeat))
- `omp --restore` no longer resends a finished turn when the session was compacted while idle, or when an earlier resume marked that turn as interrupted ([#19867](https://github.com/can1357/oh-my-pi/pull/19867) by [@enieuwy](https://github.com/enieuwy))
- The quick model picker (alt+p) in a session open for hours now shows models a provider added since the session started: once the catalog is two hours old, opening the picker re-runs discovery in the background; built-in providers fetch again, while custom `discovery:` and extension providers (cached for 24 h) pick up what another session fetched ([#19878](https://github.com/can1357/oh-my-pi/pull/19878) by [@will-bogusz](https://github.com/will-bogusz))
- A selective commit of a binary, non-text, or oversized file now keeps Git's clean-filter result for the bytes captured in the draft, including Git LFS pointers and line-ending rules, instead of the raw worktree bytes ([#19392](https://github.com/can1357/oh-my-pi/pull/19392) by [@eggpeat](https://github.com/eggpeat))
- A selective commit of a binary or non-text file now stops when a newer commit changed that file, and leaves a different staged copy in place, instead of overwriting either one ([#19392](https://github.com/can1357/oh-my-pi/pull/19392) by [@eggpeat](https://github.com/eggpeat))
- Whole-file changes in selective commits (binary, non-UTF-8, or over 4 MiB) now commit the content captured when the draft was built, instead of whatever another process left in the worktree by commit time ([#19392](https://github.com/can1357/oh-my-pi/pull/19392) by [@eggpeat](https://github.com/eggpeat))
- Fixed `read` hanging indefinitely on images and other non-text files when speculative execution is enabled with `beforeToolCall` hooks ([#19359](https://github.com/can1357/oh-my-pi/issues/19359), [#19361](https://github.com/can1357/oh-my-pi/pull/19361) by [@gtoxlili](https://github.com/gtoxlili))
- Fixed the "agent turn ended with provider error" log omitting the provider request id; Anthropic refusals now log the `request-id` that support asks for ([#19383](https://github.com/can1357/oh-my-pi/pull/19383) by [@nnnnoel](https://github.com/nnnnoel))
- Fixed sessions started from a collab peer's prompt never getting an automatic title; title reviews and the unexpected-stop judge now read collab prompts as operator requests ([#19365](https://github.com/can1357/oh-my-pi/pull/19365) by [@DaddyMonster](https://github.com/DaddyMonster))
- The `eval` tool now tells the model its default cell deadline (30 s) in the `timeout` parameter and the tool prompt ([#18856](https://github.com/can1357/oh-my-pi/issues/18856)) ([#19349](https://github.com/can1357/oh-my-pi/pull/19349) by [@Alex-Wengg](https://github.com/Alex-Wengg)).

#### Module: `@oh-my-pi/natives`

##### **Fixed**
- Fixed `grep()`, `glob()`, `fuzzyFind()`, `astGrep()`, `astEdit()`, and recursive shell search commands occasionally hanging on machines with many CPUs.
- Fixed cancellation and timeout races in native search, file-matching, fuzzy-search, AST, and editing operations that could cause crashes or use-after-free errors.
- Fixed `grep()` with a match limit reporting incomplete results instead of rejecting when its directory walk failed.
- Fixed `@oh-my-pi/pi-natives` failing to load when installed from Bun's cache or when standalone binaries had extracted native addons from another build.
- Fixed Linux Wayland accessibility and automation support for GTK dialogs, control values, and selected rows, list items, and tabs.
- Fixed Linux PTY output occasionally including an extra blank line after a command exits.
- Fixed keypad navigation keys being dropped when NumLock is off under the kitty keyboard protocol.
- Fixed Wayland screenshots incorrectly timing out while waiting for the screen-share picker.
- Improved Windows accessibility action reliability by reporting uncertain dispatches accurately and preventing actions from being sent after their reply wait has expired.
- Fixed Windows automation of classic Win32 and WinForms buttons and checkboxes incorrectly activating the application or reporting success without performing the click.
- Fixed macOS computer-control takeover restoration so the previously active window is restored correctly after automation ends, with failures reported when restoration cannot be confirmed.
- Fixed macOS background keyboard and scroll events, including events sent through iPhone Mirroring, being lost or unexpectedly activating another window.
- Fixed X11 typing of non-Latin and other characters outside the active keyboard layout.
- Binary patches now refuse to apply when the target file does not match the version the patch was created from, preventing accidental replacement of changed files.
- On Windows, aborting or timing out an in-process utility blocked on an open empty stdin pipe now terminates it without waiting for the pipe writer.

##### **Removed**
- Removed the startup warning shown when a source checkout loads a native addon from another release; incompatible addons still produce an actionable error when a required symbol is unavailable.

#### Module: `@oh-my-pi/snapcompact`

##### **Fixed**
- Fixed snapcompact archive summaries so they accurately report the grid layout of dense middle frames.

#### Module: `@oh-my-pi/stats`

##### **Added**
- Added `readDailyActivity()` for reading stored daily activity without being blocked by another process writing to the stats database; it returns `null` when no stats database exists.

##### **Fixed**
- Fixed Spotlight baseline and adjusted-net calculations to use consistent result sets, improving headline and step-row accuracy.

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
1. **Fetch Upstream Tags (into makepkg bare mirror, without touching `src/`)**:
   ```bash
   git -C oh-my-pi-git/oh-my-pi fetch origin '+refs/heads/*:refs/heads/*' '+refs/tags/*:refs/tags/*'
   # Query tags from the last 7 days sorted chronologically (oldest to newest)
   git -C oh-my-pi-git/oh-my-pi tag -l --sort=creatordate --format='%(creatordate:short) %(refname:short)'
   ```
2. **Inspect Monorepo Package Changelogs (directly from git objects)**:
   `can1357/oh-my-pi` maintains modular changelogs under `packages/*/CHANGELOG.md`. Inspect them directly from the bare mirror at `refs/heads/main` without checking out a working tree:
   ```bash
   for dir in $(git -C oh-my-pi-git/oh-my-pi ls-tree -d --name-only refs/heads/main packages/); do
       echo "=== $dir/CHANGELOG.md ==="
       git -C oh-my-pi-git/oh-my-pi show "refs/heads/main:$dir/CHANGELOG.md" 2>/dev/null | sed -n '/## \[17.3.0\]/,/## \[/p'
   done
   ```
3. **Filter and Group by Category**:
   - Prioritize **`Breaking Changes`**, **`Added`**, and **`Changed`** under each `@oh-my-pi/<package>` module.
   - Include relevant **`Fixed`** and **`Removed`** sections to capture behavioral adjustments and deprecations.
4. **Format Markdown & Distill Summary**:
   - Present releases in chronological order (`v17.3.0` → `v17.4.0`).
   - Read the distilled content and write an Executive Summary highlighting the top cross-cutting changes.
