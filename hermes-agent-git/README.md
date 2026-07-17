# hermes-agent-git

Locally-run AI agent with tool use, web browsing, and automation — built from the latest Git main branch.

## System Package Adaptations

This AUR package installs to `/opt/hermes-agent/` as a system package. Several upstream behaviors are modified to work correctly in this context.

### Self-Update Disabled (`HERMES_SYSTEM_PKG=1`)

The wrapper script (`/usr/bin/hermes`) sets `HERMES_SYSTEM_PKG=1`. This blocks:

- **`hermes update`** — prints "Use your package manager to update" instead of running `git pull` + `pip install` into the read-only install directory
- **Runtime npm installs** — the `_run_post_setup()` hooks for `agent_browser`, `browserbase`, and `camofox` skip `npm install` when the install dir is not writable. The root `node_modules/` (containing `agent-browser`, `@streamdown/math`) is pre-built at package build time and shipped with the package

Normal user operations (`hermes setup`, `hermes config set`, `.env` editing) are **not affected** — those write to `~/.hermes/` which is user-owned.

### Managed System Registration (pacman/AUR)

The patch adds `pacman` and `aur` to hermes' `_MANAGED_SYSTEM_NAMES` registry. This is **not activated** by the wrapper (we don't set `HERMES_MANAGED`), but is available for locked-down multi-user deployments where an admin sets `HERMES_MANAGED=pacman` to fully lock down config writes.

### Process Title Rewriting Disabled (`disable-setproctitle.patch`)

The gateway process liveness checks (used by the WebUI, Signal channel, and CLI) rely on reading `/proc/<pid>/cmdline` to confirm that the running process is indeed the gateway daemon. Under system-site-package inheritance on Arch Linux, the `setproctitle` module is imported and rewrites the process command line to `"hermes"`. This breaks the liveness check (causing status checks to falsely report the gateway as stopped). This patch disables `setproctitle` to keep the original command line arguments intact.

### Hindsight Memory Configuration (Environment Variables)

Hindsight memory behavior and constraints can be dynamically configured on a per-profile level by adding overrides to the profile's `.env` file (e.g. `~/.hermes/profiles/<profile_name>/.env`). Supported environment variables include:

* **`HINDSIGHT_MODE`**: Connection mode (choices: `cloud`, `local_embedded`, `local_external`; default: `cloud`).
* **`HINDSIGHT_API_URL`**: Target server URL (default: `https://api.hindsight.vectorize.io` for cloud, `http://localhost:8888` for local modes).
* **`HINDSIGHT_API_KEY`**: Cloud or custom server API authorization key, no default, should be empty for compatibility

Patched Support for:
* **`HINDSIGHT_BUDGET`** / **`HINDSIGHT_RECALL_BUDGET`**: Thoroughness level for recall and reflection generation (choices: `low`, `mid`, `high`; default: `mid`).
* **`HINDSIGHT_RECALL_MAX_TOKENS`**: Limit on the maximum tokens returned by recall/reflection results (default: `4096`).

## PR Patching Mechanism

The `_prs` array in the PKGBUILD allows on-demand application of GitHub pull requests as patches:

```bash
# In PKGBUILD — edit this array to add/remove PRs:
_prs=(57668)
```

During `prepare()`, each PR number is:
1. Downloaded as `https://github.com/NousResearch/hermes-agent/pull/<N>.patch`
2. Applied with `git apply`

To add a PR: append its number to the `_prs` array and rebuild.
To remove a PR: remove its number from the array and rebuild.

### Currently Applied PRs

| PR | Description |
|----|-------------|

## Patch Files

| Patch | Description |
|-------|-------------|
| `hermes-managed-pacman.patch` | Registers pacman/AUR in managed system names, blocks `cmd_update()` via `HERMES_SYSTEM_PKG`, gates runtime npm installs behind writable-dir check |
| `python314-daemon-pool.patch` | Fixes Python 3.14 compatibility bug in `DaemonThreadPoolExecutor` caused by CPython internal changes (removal of `_initializer`/`_initargs`) |
| `skills-install-slug-resolution.patch` | Fixes short skill name resolution to match against identifiers/slugs in addition to exact display names |
| `hindsight-provider-patches.patch` | Fixes local_external Hindsight mode (splits initialization, implements connection health probing, improves setup wizard logic, relaxes dependency version limits, and handles hermes system package environment checks) |
| `disable-setproctitle.patch` | Disables Strategy 1 (setproctitle) in `_set_process_title` to prevent rewriting the process command line in `/proc/<pid>/cmdline`, which was breaking gateway liveness checks (WebUI/TUI/Signal status detection) |


