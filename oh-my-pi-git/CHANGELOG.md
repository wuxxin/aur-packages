# oh-my-pi-git — system-facing changelog

What each harness upgrade brings to **our system** (the mypai omp sandbox: the LifeOS hooks bridge, the local
llama.cpp router, the Pulse voice pipeline, multi-session agent mesh). Privacy-neutral by design: no hostnames,
users, or home paths. Other mypai infrastructure may consume and extend this file; entries are append-only at the
top, one per upgrade: version range, commit range, curated upstream changes with breaking ones first.

How to re-derive an entry: see "Maintenance" in [README.md](README.md) — diff the installed pkgver's commit to
HEAD, curate from upstream, regenerate patches via snapshot chain, then append here.

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
