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
| `exec` | Run `openfang` commands in the same restricted sandbox. |
| `shell` | Spawn an interactive shell for debugging within the daemon's sandbox. |

## Implementation Considerations

### Nested Sandboxing (Bubblewrap Support)
OpenFang often orchestrates sub-agents that require their own isolation. To support **bubblewrap (`bwrap`)** nested sandboxing:
- **Namespaces**: `RestrictNamespaces=yes` is **omitted**. `bwrap` relies on unprivileged user namespaces (`CLONE_NEWUSER` and `CLONE_NEWNS`) to build its sandbox.
- **Process Info**: `ProtectProc=invisible` and `ProcSubset=pid` are **omitted**. This allows `bwrap` to securely bind its own `/proc` filesystem without crashing due to lack of visibility.
- **Elevation**: `NoNewPrivileges=yes` is maintained as it is compatible with modern `bwrap` and enhances overall security.

### Filesystem Hardening
- **Strict Protection**: Uses `ProtectSystem=strict` and `TemporaryFileSystem=%h` to ensure the daemon cannot see or modify the user's real home directory by default.
- **Explicit Mounts**:
    - `~/.local/share/openfang`: Persistent data and state store.
    - `~/agent-shared`: Shared integration directory.
- **Read-Only System Paths**: SSL certificates and network configuration are mounted as read-only.

### Environment
- **HOME Redirection**: `HOME` is set to `%h/.local/share/openfang` within the service to isolate user-level configuration (like `.ssh` or `.gitconfig`) that might be created by the agent.
- **Secrets**: Environment variables are loaded from `~/.config/systemd/user/openfang.env`.
