# amux-git (with Oh-My-Pi Provider & Local Workflow Patches)

Arch Linux PKGBUILD for [amux](https://github.com/mixpeek/amux) — the multi-session AI agent orchestrator and control plane.

This package includes custom enhancements to support **Oh-My-Pi (`omp`)** as a first-class agent provider alongside Claude Code, Codex, and Gemini, as well as UI patches optimized for local/offline agent environments.

---

## Included Patches

### 1. `omp-provider.patch`
Adds native support for the **Oh-My-Pi (`omp`)** CLI provider across the entire `amux` stack:

- **Server Provider Engine (`amux-server`):**
  - Implements `OmpAdapter` conforming to `ProviderAdapter` with standard capabilities and conformance test coverage.
  - Registers `omp` in the default provider registry with alias resolution (`oh-my-pi` -> `omp`).
  - Extends `SESSION_PROVIDERS` to include `"omp"`, ensuring session configuration (`CC_PROVIDER=omp`) and REST endpoints (`POST /api/sessions`, `PATCH /api/sessions/<name>`) recognize `omp` without falling back to Claude.
  - Configures provider execution commands (`omp` interactive, `omp exec` headless).
  - Configures YOLO permission flag mapping (`--approval-mode=yolo`).
  - Sets default model mapping (`auto`).
  - Preserves environment credentials during session startup without unsetting non-Claude environment variables.

- **Web Dashboard (`amux-dashboard`):**
  - Adds an **"Oh-My-Pi"** provider selection button to the **New Worker** modal (`index.html`).
  - Adds `omp` to the card provider menu (`editField`) and session detail views.
  - Adds UI badges and archived card chip styling for `omp` (`app.css`).

### 2. `disable-no-apikey-banner.patch`
- Suppresses the "No Anthropic API key set — Claude workers won't work" warning banner in the WebUI on local (non-cloud) instances.
- Prevents UI clutter when using local LLMs, Ollama, Gemini, or Oh-My-Pi without Anthropic API keys.

---

## Building and Installing

### Standard Build (Clean)
```bash
cd submodules/aur-packages/amux-git
makepkg -si
```

### Incremental Build (Preserve Source Tree)
```bash
cd submodules/aur-packages/amux-git
makepkg -ef
sudo pacman -U amux-git-*.pkg.tar.zst
```

### Updating Checksums & SRCINFO
When modifying patches:
```bash
updpkgsums
makepkg --printsrcinfo > .SRCINFO
```

---

## Usage with MyPAI & Oh-My-Pi

1. **Creating an Oh-My-Pi Worker via WebUI:**
   - Open the WebUI (`https://127.0.0.1:8824`).
   - Click **New worker**.
   - Select the **Oh-My-Pi** provider button.
   - Enter worker name and project directory, then click **Create**.

2. **Creating an Oh-My-Pi Worker via REST API:**
   ```bash
   curl -k -X POST https://127.0.0.1:8824/api/sessions \
     -H "Content-Type: application/json" \
     -d '{"name": "worker-1", "dir": "/path/to/project", "provider": "omp"}'
   ```

3. **Running inside MyPAI Sandbox (`omp.env`):**
   Ensure your `omp.env` sets:
   ```bash
   LAUNCHER_SERVICE_CMD="amux-server"
   # Leave AMUX_HERDR_SESSION unset or empty when not using herdr
   ```
