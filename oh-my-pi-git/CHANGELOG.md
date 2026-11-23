# oh-my-pi-git — system-facing changelog

What each harness upgrade brings to **our system** (the mypai omp sandbox: the LifeOS hooks bridge, the local
llama.cpp router, the Pulse voice pipeline, multi-session agent mesh). Privacy-neutral by design: no hostnames,
users, or home paths. Other mypai infrastructure may consume and extend this file; entries are append-only at the
top, one per upgrade: version range, commit range, curated upstream changes with breaking ones first.

How to re-derive an entry: see "Maintenance" in [README.md](README.md) — diff the installed pkgver's commit to
HEAD, curate from upstream, regenerate patches via snapshot chain, then append here.

## 2026-11-23 — 19.0.0.r1.gd4ebe4d → 19.1.1.r184.g0aefd54 (1,387 commits)

Upstream window `d4ebe4d..0aefd54`: covers releases **v19.0.1**, **v19.1.0**, **v19.1.1**, plus 184 post-tag
commits on `main`. Curated for this system; full upstream text lives in `packages/coding-agent/CHANGELOG.md`.

### Breaking / architecture — needs action on our side

- **`xd://` virtual tool devices replaced by tool commands (19.1.0)**: discoverable tools now run as bash
  commands (`<tool> --help`, `<tool> <args>`) while `bash` is active (top-level otherwise). Staged previews,
  plan submission, and Auto-QA reports use `resolve`, `reject`, `propose`, and `report_issue`; doc topics moved
  from `xd://<tool>/<topic>` to `help://<tool>/<topic>`. All profile agent prompts and skills must migrate off
  `xd://`.
- **Settings renamed/replaced**: `tools.xdev*` → `tools.commands` / `tools.commandDocs` / `tools.commandInline`
  / `tools.commandNotices` (19.1.0); `computer.backgroundFallback` → `computer.takeover`
  (`fallback|refuse|foreground|always`, 19.1.1); `tui.completeScrollback` removed (19.1.0, always-on).
- **Browser relay moved to Chrome native messaging host (19.1.0)**: `omp browser-relay` server command removed;
  `omp browser-relay install` writes the unpacked extension and Chrome `NativeMessagingHosts` manifests and
  auto-syncs on upgrades. Reload the Chrome extension once after upgrading.
- **MCP servers moved into the per-user omp daemon (19.1.0)**: `mcp.shared` (default on) + `mcp.idleStopMinutes`
  (default 5), lazy startup, shared discovery cache, MCP `2026-07-28` + handshake fallback (#20208). Daemon no
  longer loads the model catalog, AI providers, or most TUI (~24 MB less RSS, #20224).
- **RPC `ask` form breaking change (19.1.0)**: RPC hosts must handle `ask` as one complete HTML-form request
  (no impact on `--mode=json` shims).

### Hooks-bridge & local-stack fixes

- **OmpHooksBridge: zero adapter work.** All mapped extension events unchanged; additive `parentToolCallId` on
  `tool_call`/`tool_result`, `pi.registerTodoBackend()` + `todo.backend`, and `registerProvider` overrides.
- Fixed `read` hanging on images/non-text files when `speculativeExecution` and `beforeToolCall` hooks are both
  enabled (19.1.1).
- LSP servers without progress (`pyright`, `ty`, `ruff`, `typescript-language-server`) no longer stall 15 s on
  first diagnostics — ends after 2 s (#20204); Linux LSP file watching adapts to inotify limits (19.1.1).
- Claude-format plugin skills/commands/agents now resolve `${CLAUDE_PLUGIN_ROOT}` / `${OMP_PLUGIN_ROOT}` (#20186)
  and map Claude tool names (`WebFetch`, `TodoWrite`, `AskUserQuestion`, `Agent`, etc.) (19.1.1).
- `openai-completions` stream replay stops re-running HTTP 500s (#20215); speculative/auto compaction falls back
  to the next method on oversized handoffs (19.1.1); Hindsight `/tan` forks retain only new turns (#20259).

### Interactive / user-facing highlights

- New `magic` edit mode (`edit.mode: magic`, `edit.magic.model`, 19.1.0/19.1.1); opt-in `tree` status segment
  (19.1.1); `pty.notify` when a bash PTY waits for input (19.1.0); `/session` shows `local://` path & `/copy local`
  (19.0.1); `column` shell builtin (19.1.1); `/wt` runs `post-checkout` hooks (19.1.1); full-text `archive.search()`
  (19.1.0).
- Vim mode overhaul (#20037): Vim in ask forms/dialogs, `Ctrl+R` redo in Normal mode, `/` & `?` history search,
  `:` slash commands, `tui.vimStartMode`, `tui.vimShowCommand`, `tui.vimYankToClipboard` (plain `y` no longer
  copies to system clipboard by default).

### Package-side changes this iteration

- `skip-native-embed-for-aur.patch` updated for upstream's `embeddedRelayExtensionFiles()` addition in
  `compile-binary.ts`.
- Added `external-relay-extension-for-aur.patch`: externalizes the zstd-compressed browser-relay bundle out of
  the `omp` binary into `/usr/share/oh-my-pi/browser-relay-extension.json.zst` (keeping `omp browser-relay install`
  and auto-sync intact). Dropped redundant `omp-browser-relay-extension.zip` (unpacked `/usr/share/oh-my-pi/browser-relay`
  retained).
- Added runtime `optdepends`: `libpulse`, `alsa-lib`, `pipewire`.

## 2026-11-19 — 18.22.2.r190.g2cdc756 → 19.0.0.r1.gd4ebe4d (41 commits)

Upstream window `2cdc756..d4ebe4d`: the **v19.0.0 release** (`57771ae`) plus post-release fixes and one docs
commit. Most user-facing features of 19.0.0 were already recorded in the previous entry (they shipped inside
that window as unreleased commits); this entry lists what is new at or after the tag, breaking first.

### Breaking / architecture — needs action on our side

- **SDK renames now tagged**: `createAgentSession.cacheWarming` takes mode caps `"off"|"streaming"|"idle"`
  (was boolean); `session.handoff(focus)` → `session.compact(focus, {mode:"handoff"})` + `abortCompaction()`;
  `deferSkillDescriptionCompression` → `deferHintCompression`, `startSkillDescriptionCompression()` →
  `startHintCompression()` (now also covers MCP namespace hints). SDK/extension code in the workspace must audit.
- **Daemon consolidation shipped as breaking**: older daemons/services are not adopted, `omp ps` is global
  (one `{daemon, reports}` JSON); one restart of omp-managed services after install. New `OMP_DAEMON_TCP`
  keeps running services/PTYs/language servers alive across future daemon upgrades — worth enabling on the
  sandbox host.
- **Auth broker startup**: interactive no longer blocks 30 s retrying an unreachable broker; CLI/print/SDK keep
  the 30 s window with a stderr notice. Sidecar/headless launches (`omp -p` under systemd) get a defined
  behavior instead of hanging silently. `OMP_LOG_LEVEL` now also controls console output from services like
  `omp auth-broker serve`.

### Hooks-bridge feature set (OmpHooksBridge)

- **No change to any mapped event.** The v19 tag carries the #19550 payload support (`excludeFromContext`) the
  bridge's in-session stats rows were written against — rows are now zero-context on a tagged release; drop any
  `OMP_BRIDGE_SESSION=0` opt-outs.
- Extension imports of `@oh-my-pi/pi-natives` resolve again (the v19 crate rename had rewritten the npm dir to
  `omp-natives`; restored in `003818b`). Any host extension importing it was broken on unreleased tips between
  the rename and this fix.
- Compaction barrier fix (#5800): messages queued during `/compact` re-drain after the barrier clears. Adjacent
  to the queue-steering re-emission our UserPromptSubmit dedup guard compensates for — the guard stays required,
  no per-model-call re-emission was removed.

### Memory / agent-mesh relevant

- **Mnemopi: retention on yielded pauses is retained and retains are serialized (#19690)** — fixes duplicate and
  dropped memories in runs with async work, subagents, or peer messages. Directly improves the auto-learn path
  this harness uses.
- Ask forms open each question at its preselected answer; Enter accepts the recommendation (#19657). Permission
  prompts driven by bridge `ask → ui.confirm` benefit from the same flow changes (scrolling details, persistent
  Approve/Deny).
- Shell process worker owns SIGTERM/SIGHUP and lets trapped programs finish (`postmortem.exitCleanlyOnStopSignals`) —
  omp-managed services under systemd stop cleanly with exit 0 instead of orphaning children; unit configs need no
  `TimeoutStopSec` workarounds.
- Hosted judgment (>32 questions) fixed for TypeSafe/OpenRouter/Command Code/OpenCode Zen — relevant to
  gateway-fronted routers. Kiro API-key auth (`ksk_…`) works end-to-end again.

### Package-side changes this iteration

- Patches verified against `d4ebe4d` via the README snapshot chain: final tree byte-identical (chain-tip
  `git write-tree`). `relative-json-asset-paths.patch` regenerated — upstream's pi-natives rename fix touched
  its second file (`legacy-pi-virtual-module.ts`), only the index preimage line changed. The other three apply
  with zero offset in prepare() order.
- **Package rename completed**: added `replaces=('oh-my-pi-git-tag')` + matching conflict (the pkgbase rename
  c1d54a2 left no migration edge). Verified: built `.PKGINFO` carries both; `pacman -U` of the new package
  removes the old-named install in one step.

## 2026-11-18 — 18.21.0.r32.g6e8ab5f → 18.22.2.r190.g2cdc756 (795 commits)

Upstream window `6e8ab5f..2cdc756`, covering releases 18.22.0/18.22.1/18.22.2 plus unreleased commits.
The build fetched a newer tip than the curated snapshot (`08cb444`); the extra `08cb444..2cdc756` range is
fixes/docs only (auth-broker startup, catalog effort-class rules, macOS natives reads) — no feature changes.
Curated for this system; full upstream text lives in the source checkout's `packages/coding-agent/CHANGELOG.md`.

### Breaking / architecture — needs action on our side

- **One per-user daemon replaces per-project brokers + separate host processes** (services, language servers,
  disassembler DBs, local models, speech, text prediction). Daemons/services started by older versions are **not
  adopted**; a newer omp re-execs the daemon in place on update. After install: restart any long-running
  omp-managed services once; Pulse is unaffected (systemd unit, not an omp unit). `omp ps` changed (`--global`
  gone, one `{daemon, reports}` JSON object).
- **`artifact://` removed**: shaped tool output now lands as `local://N.log` at the session's `local://` root.
  Old sessions' artifact links are not migrated — prompts/docs referencing `artifact://` follow upstream text.
- **AgentSession run lifecycle** (18.21.0): `agent_end` fires once per non-resumable run, new `agent_pause`;
  `hasPendingAsyncWork()/settleAsyncWork()` replaced by `isRunActive/wakeSources/waitForRunEnd`. Extension
  streams keep the old per-loop `agent_end` — the hooks bridge is unaffected.
- `/restart` re-execs **through the launcher**, so an open session moves onto the upgraded binary (the `lifeos`
  launch path benefits).
- MCP tool calls default to a 10-minute deadline, extended up to 1 h by progress notifications — affects the
  configured MCP servers.
- STT/TTS models load **once per machine** and unload after 15 min idle (was per session) — shared with the
  Pulse/voice stack.
- Keyless-aux controls: `providers.webKeyless` off-switch; `--no-judge` / `--no-spotlight` / `--offline`;
  `find` self-disables when judge endpoints reject the account. Worth enabling for a localhost-only router to
  avoid paid/keyless fallbacks.

### Hooks-bridge feature set (OmpHooksBridge)

- **No change to any event the bridge maps** (session_start, message_start, tool_call/result, turn_end,
  session_shutdown, session_clear, tool_approval_requested, context). No adapter work required for this upgrade.
- New extension API: `pi.sendMessage` payloads can carry `excludeFromContext: true` (#19550) — drawn and saved,
  never sent to the model; a good fit for surfacing bridge audit/stats rows in-session.
- Native approval dialogs: details scroll so choices stay visible; compound bash prompts show per-segment
  allow/ask. Improves the bridge's `ask → ui.confirm` path; the "suppress duplicate Notification, keep
  PermissionRequest" rule stays correct.
- Voice stack: local TTS default is now Phonon 31M (Kokoro settings auto-migrate); `live.endpoint` /
  `live.apiKey` allow self-hosted OpenAI-Realtime-compatible voice servers; a `say` builtin speaks through omp
  speech or system voices. All overlap the existing OMP_VOICE/Pulse-notify pipeline — no bridge changes needed,
  but these are native paths to prefer over shims going forward.

### Interactive / user-facing worth knowing

- **Composer predictions are on by default** (one extra billed request per turn against the local router) —
  disable in `/settings → Interaction` if the local box should not pay for ghosts.
- `ask` renders as one inline card above a preserved composer; `?` prefix submits a `/btw` side question.
- Model switching keeps the thinking level; the switcher shows auto's settled level; provider search ranks by
  provider prefix.
- Session accounting now includes side-channel calls (compaction, recaps, memory extraction, image generation,
  web search) — `/stats` becomes honest about local inference spend; compaction spend is journaled per method.
- Cache warming bridges long tool calls: keepalive vs. priced buy-out, `providers.cacheWarmingStrategy`
  (`auto|keepalive|compact`); Anthropic on-demand compaction extends to custom-API models and opted-in
  gateways — relevant for router-fronted Claude-style endpoints.
- Providers: native **Kiro** (+credits in `/usage`), Bifrost gateway, Factory Droid models, GPT-6.2 Astra/Sol;
  Claude subscription plan shown in usage reports.
- Embedded shell gains builtins (`entr`, `fswatch`, `watchexec`, `direnv`, `file`, `say`, `open/xdg-open`,
  `flock`, `urlmap`); bare `sh/bash/zsh` run as child shells of the engine; named services and pty commands run
  inside omp's shell with internal-URL resolution — launcher scripts and build helpers should assume this.
- `task.crossInstance` (off by default): same-folder omp instances list via `agent://peers` and message each
  other by PID — a native fit for the multi-session mesh; evaluate enabling deliberately (digit-only task names
  get an `Agent` prefix while on).
- `wait` returns at once naming the deadlock chain ("B is waiting on you via C") — removes the idle-poll failure
  mode observed in long tool loops.
- `/wt` worktrees use ovnfs when installed (isolation.backend: auto); sessions stay resumable from the source
  repo after their checkout is removed.
- Tern-only UI features (subagent/job tray cards, plan-review editing) — no effect on terminal surfaces.

### Package-side changes this iteration

- All four patches regenerated against `08cb444` with zero offset/fuzz; resulting tree verified byte-identical to
  the previous chain (`git write-tree`). The old `tree-sitter-no-strict-aliasing.patch` had drifted (−2 lines,
  fuzz 1).
- `use-system-opus-pcre2.patch` extended: upstream added an addon verifier in `scripts/bazel-natives.ts` that
  rejects any `.node` with `DT_NEEDED` outside the glibc set (their builds embed vendored static opus/pcre2).
  Our intentional shared-lib links failed it, so the patch now adds `libopus.so.0` and `libpcre2-8.so.0` to the
  verifier's allow-list (`GLIBC_ADDON_NEEDED`).
- Gotcha recorded in README: a probe `makepkg --nobuild` leaves patch-created untracked files in the VCS working
  copy; makepkg's reset keeps them and prepare() then fails on "already exists". Clean with
  `rm -rf src/oh-my-pi pkg` before real builds.
