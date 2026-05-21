# Agent Isolation Requirements

Agent runtimes in this repository operate under strict, layered sandboxing configurations to protect the host system while allowing agents to execute their tools securely. 

## Systemd User Service Confinement

All agents are wrapped in systemd user services that enforce resource and permission boundaries. Depending on the runtime's internal mechanics for spawning tools, two different profiles are used:

### 1. Strict Confinement Profile (PicoClaw, NanoBot)
For agents that execute tools directly or use internal sandboxing mechanisms that do not require creating new user namespaces, the strictest profile is applied.

**Key Settings:**
- `ProtectProc=invisible` and `ProcSubset=pid`: Hides other system processes from the daemon.
- `RestrictNamespaces=yes`: Prevents the creation of new namespaces.
- `MemoryDenyWriteExecute=yes`: Prevents creating W^X memory mappings (some interpreters like JVM require this to be disabled).
- `PrivateTmp=yes`, `ProtectSystem=strict`, `PrivateDevices=yes`: Standard filesystem hardening.

### 2. Relaxed Namespaces Profile (OpenFang, Hermes, ZeroClaw, NanoClaw)
For agents that orchestrate sub-agents or use tools like Bubblewrap (`bwrap`), Podman, or Docker for internal sandboxing, the systemd unit must relax specific restrictions to allow nested virtualization.

**Key Settings:**
- **Namespaces**: `RestrictNamespaces=yes` is **omitted**. Sandboxing tools (like `bwrap` or Rootless Podman) rely on unprivileged user namespaces (`CLONE_NEWUSER` and `CLONE_NEWNS`) to build their sandboxes.
- **Process Info**: `ProtectProc=invisible` and `ProcSubset=pid` are **omitted**. This allows `bwrap` to securely bind its own `/proc` filesystem without crashing due to lack of visibility.
- **Elevation**: `NoNewPrivileges=yes` is maintained as it is compatible with modern `bwrap` and enhances overall security.
- **Device Access**: If GPU access or Docker socket mapping is required, `PrivateDevices` may be disabled or explicitly configured.

## Agent-Specific Mechanisms

- **ZeroClaw**: Supports multiple sandbox backends. By default (`sandbox_backend = "auto"`), it prefers Landlock or Bubblewrap on Linux. If Bubblewrap is used, the systemd service uses the Relaxed Namespaces Profile.
- **NanoClaw**: Spawns Docker/Podman containers to execute tools (e.g., `nanoclaw-agent:latest`). It requires access to the container daemon and the ability to spawn namespaces, utilizing the Relaxed Namespaces Profile.
- **Hermes & OpenFang**: Standardize on the Relaxed Namespaces Profile to support nested `bwrap` orchestration.
