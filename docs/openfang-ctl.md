# OpenFang Agent OS Management Guide

`openfang-ctl` manages the OpenFang Agent OS daemon, providing a hardened execution environment for agentic workloads.

## Installation

```bash
./scripts/openfang-ctl install
```

## Commands

| Command | Description |
|---|---|
| `install` | Sets up `~/.local/share/openfang` and the systemd unit. |
| `uninstall` | Tears down the service while preserving data. |
| `logs` | Monitor the agent's background activities. |
| `exec` / `shell` | Run commands in the same restricted sandbox as the daemon. |

## Implementation Considerations

### Nested Sandboxing (Bubblewrap)
OpenFang is designed to run child agents inside their own `bwrap` sandboxes. To support this:
- `RestrictNamespaces=yes` is **omitted**: `bwrap` requires `CLONE_NEWUSER` and `CLONE_NEWNS`.
- `ProtectProc=invisible` and `ProcSubset=pid` are **omitted**: Allows the agent to mount its own `/proc` within the nested sandbox.
- `NoNewPrivileges=yes`: Retained for security as it is compatible with unprivileged `bwrap` usage.

### Filesystem Hardening
- `ProtectSystem=strict` and `TemporaryFileSystem=%h`: Prevents the daemon from seeing or modifying the user's real home directory except for explicitly bound paths.
- `BindPaths=%h/.local/share/openfang`: The primary persistent data store.
- `BindPaths=%h/agent-shared`: Integration point for sharing state with other tools.

### Environment
Configured via `~/.config/systemd/user/openfang.env`. The home directory for the process is redirected to its isolated data path via the `HOME` environment variable within the unit.
