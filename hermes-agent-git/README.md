# hermes-agent-git

Locally-run AI agent with tool use, web browsing, and automation — built from the latest Git main branch.

## System Package Adaptations

This AUR package installs to `/opt/hermes-agent/` as a system package. Several upstream behaviors are modified to work correctly in this context.

### Self-Update Disabled (`HERMES_SYSTEM_PKG=1`)

The wrapper script (`/usr/bin/hermes`) sets `HERMES_SYSTEM_PKG=1`. This blocks:

- **`hermes update`** — prints "Use your package manager to update" instead of running `git pull` + `pip install` into the read-only install directory
- **Runtime npm installs** — the `_run_post_setup()` hooks for `agent_browser`, `browserbase`, and `camofox` skip `npm install` when the install dir is not writable. The root `node_modules/` (containing `agent-browser`, `@streamdown/math`) is pre-built at package build time and shipped with the package

Normal user operations (`hermes setup`, `hermes config set`, `.env` editing) are **not affected** — those write to `~/.hermes/` which is user-owned.

### Desktop App Update Gate (PR #57668)

PR [#57668](https://github.com/NousResearch/hermes-agent/pull/57668) adds the `HERMES_DISABLE_UPDATES` env var for the Electron desktop app. When set:
- The "Check for Updates…" menu item is removed
- The `hermes:updates:*` IPC handlers are not registered
- The `hermes:uninstall:*` IPC handlers are not registered

This is orthogonal to `HERMES_SYSTEM_PKG` (which handles CLI-side concerns).

### Managed System Registration (pacman/AUR)

The patch adds `pacman` and `aur` to hermes' `_MANAGED_SYSTEM_NAMES` registry. This is **not activated** by the wrapper (we don't set `HERMES_MANAGED`), but is available for locked-down multi-user deployments where an admin sets `HERMES_MANAGED=pacman` to fully lock down config writes.

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
| [#57668](https://github.com/NousResearch/hermes-agent/pull/57668) | `feat(desktop)`: gate self-update and uninstall behind `HERMES_DISABLE_UPDATES` env var |

## Patch Files

| Patch | Description |
|-------|-------------|
| `hermes-managed-pacman.patch` | Registers pacman/AUR in managed system names, blocks `cmd_update()` via `HERMES_SYSTEM_PKG`, gates runtime npm installs behind writable-dir check |
| `python314-daemon-pool.patch` | Fixes Python 3.14 compatibility bug in `DaemonThreadPoolExecutor` caused by CPython internal changes (removal of `_initializer`/`_initargs`) |

