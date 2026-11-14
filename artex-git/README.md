# ARTEX Global — Arch Linux Packaging & Onboarding Guide

`artex-git` packages the autonomous penetration-testing multi-agent framework [jiwoochris/artex-global](https://github.com/jiwoochris/artex-global) (Go backend with embedded Next.js static UI, PostgreSQL store, and local/cloud LLM routing) for Arch Linux.

---

## 1. Overview & Authorized Use Notice

> **LEGAL AND ETHICAL NOTICE:**  
> ARTEX is designed exclusively for authorized penetration testing, vulnerability assessment, and defensive security auditing on systems you own or have explicit written permission to test. Unauthorized access to computer systems, networks, or data is illegal.

License: **GNU Affero General Public License v3.0** (`AGPL-3.0-only`).

---

## 2. Package Architecture & File Destinations

The package compiles the static Next.js frontend (`web/`) and embeds it into the Go binary (`cmd/artex`) via Go's `//go:embed` mechanism (`-tags embedui`). At runtime, no Node.js daemon is required.

### Filesystem Layout

| Path | Purpose |
|------|---------|
| `/usr/bin/artex` | Compiled single-binary executable (Go + embedded Next.js SPA) |
| `/usr/share/artex/skills/` | Stock security skills catalog (`scopesentry`, `playwright-cli`, `api-recon`) |
| `/etc/artex/config.json` | Default system configuration (`backup=()` preserved on upgrade) |
| `/etc/artex/artex.env` | Optional environment variable overrides file (`EnvironmentFile=-...`) |
| `/usr/lib/systemd/system/artex.service` | Hardened systemd daemon unit |
| `/usr/lib/sysusers.d/artex.conf` | System user/group allocation (`artex:artex`) |
| `/usr/lib/tmpfiles.d/artex.conf` | Runtime and state directory provisioning |
| `/var/lib/artex/data/` | Persistent state (JWT key, SQLite event stores, CA proxy certs) |
| `/usr/share/licenses/artex-git/LICENSE` | AGPL-3.0 license copy |
| `/usr/share/doc/artex-git/` | Upstream documentation |

---

## 3. Dependencies

### Build Dependencies (`makedepends`)
- `go` (>= 1.22): Compiles the backend Go executable (`cmd/artex`).
- `nodejs` (>= 20) & `npm`: Compiles and exports the Next.js static frontend (`npm run build:static`).
- `rsync`: Synchronizes `web/out/` into `server/webui/dist/` for Go embedding.
- `git`: Sources upstream repository snapshot and resolves VCS versioning tags.

### Runtime Dependencies (`depends` & `optdepends`)
- **Core Runtime**:
  - `glibc`: Standard C library.
  - `ca-certificates`: TLS trust anchors for outbound LLM and target connections.
- **Database (`optdepends`)**:
  - `postgresql`: Required persistent store. ARTEX uses PostgreSQL for findings, scans, configurations, and tasks. Schema migrations run automatically on startup via advisory locks.
- **Autonomous Recon & Assessment Tooling (`optdepends`)**:
  - `ripgrep`: Rapid file/text search during local codebase audits.
  - `nmap`: Network port and vulnerability scanning.
  - `bind` (or `dnsutils`): DNS enumeration tools (`dig`, `nslookup`).
  - `whois`: Domain and IP registration lookups.
  - `iputils`: Network reachability checks (`ping`).
  - `openbsd-netcat`: Raw TCP/UDP connections and banner grabbing.
  - `curl` & `wget`: Web fetching, spidering, and HTTP interaction.
  - `jq`: JSON processing in tool pipelines.
  - `playwright`: Headless browser automation via Playwright MCP (`npx @playwright/mcp`).

---

## 4. Installation

Build and install using `makepkg`:

```bash
cd submodules/aur-packages/artex-git
makepkg -si
```

Or using an AUR helper:

```bash
paru -S artex-git
# or: yay -S artex-git
```

---

## 5. PostgreSQL Database Setup

ARTEX requires a PostgreSQL database. Follow these steps to configure a local database on Arch Linux:

### 1. Initialize PostgreSQL (if not previously configured)

```bash
sudo -u postgres initdb -D /var/lib/postgres/data
```

### 2. Enable and Start PostgreSQL Service

```bash
sudo systemctl enable --now postgresql
```

### 3. Create Dedicated User and Database

Connect as the `postgres` administrative user:

```bash
sudo -u postgres psql
```

Execute SQL commands:

```sql
CREATE USER artex WITH ENCRYPTED PASSWORD 'artex_secure_password';
CREATE DATABASE artex OWNER artex;
GRANT ALL PRIVILEGES ON DATABASE artex TO artex;
\q
```

---

## 6. Configuration

### Configuration File (`/etc/artex/config.json`)

The default configuration file installed at `/etc/artex/config.json` is preconfigured for the local database:

```json
{
  "database": {
    "host": "127.0.0.1",
    "port": 5432,
    "user": "artex",
    "password": "artex_secure_password",
    "dbname": "artex",
    "sslmode": "disable"
  },
  "skill_dir": "/usr/share/artex/skills",
  "language": "en"
}
```

Update `"password"` to match the password configured in PostgreSQL.

Alternatively, a full connection string can be supplied:

```json
{
  "database": {
    "dsn": "postgres://artex:artex_secure_password@127.0.0.1:5432/artex?sslmode=disable"
  },
  "skill_dir": "/usr/share/artex/skills",
  "language": "en"
}
```

### Environment Overrides (`/etc/artex/artex.env`)

For sensitive keys (LLM credentials, DB overrides), create `/etc/artex/artex.env` (mode `0600`, owned by `artex:artex`):

```bash
sudo touch /etc/artex/artex.env
sudo chown artex:artex /etc/artex/artex.env
sudo chmod 0600 /etc/artex/artex.env
```

Populate `/etc/artex/artex.env` as needed:

```bash
# Database DSN override (optional)
# ARTEX_PG_DSN=postgres://artex:artex_secure_password@127.0.0.1:5432/artex?sslmode=disable

# Bootstrap / First-run admin credentials (optional)
# ARTEX_SETUP_TOKEN=my-secure-setup-token
# ARTEX_ADMIN_PASSWORD=my-initial-admin-password

# Output language ("en", "ko", "zh", "es", "ja")
ARTEX_LANG=en
```

---

## 7. Systemd Service Management

The package provides a hardened systemd service running under the unprivileged `artex` user.

### Enable and Start the Service

```bash
sudo systemctl enable --now artex
```

### Check Service Status and Logs

```bash
sudo systemctl status artex
sudo journalctl -u artex -f
```

---

## 8. First-Run Onboarding & Admin Setup

On initial startup, ARTEX generates a single-use setup bootstrap token and logs it to the system journal:

1. Retrieve the bootstrap token:
   ```bash
   sudo journalctl -u artex -e | grep -F '[auth]'
   ```
   You will see an entry similar to:
   ```
   [auth] initial admin setup required: navigate to http://127.0.0.1:8787/setup with token <SETUP_TOKEN>
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8787/setup
   ```

3. Paste the setup token, and create the administrator account (`admin`) and master password.

---

## 9. LLM Provider Configuration

ARTEX supports both local inference engines (such as `local-router`, vLLM, Ollama, llama.cpp) and cloud APIs.

### Option A: Local Inference (`local-router` / OpenAI-compatible on `http://localhost:21080`)

#### Method 1: Via Web UI (Recommended)
1. Log in to the web console at `http://127.0.0.1:8787`.
2. Navigate to **System → Settings → LLM**.
3. Select provider: **OpenAI-compatible** (or **Custom**).
4. Set **Base URL**:
   ```
   http://localhost:21080/v1
   ```
5. Set **API Key**: Any non-empty placeholder string (e.g. `sk-local-router` or `local`).
6. Set **Model**: Enter your local model identifier (e.g., `qwen2.5-coder-32b`, `deepseek-r1`, or configured chat model).
7. Set **Max Tokens**: Set to `8192` or `16384` to prevent OpenAI-path context limit errors during complex multi-turn evaluations.
8. Save settings and test the connection.

#### Method 2: Via Environment Variables
Add the following to `/etc/artex/artex.env`:

```bash
OPENAI_API_KEY=sk-local-router
ARTEX_LLM_PROVIDER=openai
ARTEX_LLM_BASE_URL=http://localhost:21080/v1
ARTEX_LLM_MODEL=default
```

Restart the service:

```bash
sudo systemctl restart artex
```

### Option B: Cloud Providers

To use Anthropic Claude or OpenAI cloud models, configure `/etc/artex/artex.env`:

```bash
# Anthropic
ANTHROPIC_API_KEY=sk-ant-api03-...

# OpenAI
OPENAI_API_KEY=sk-proj-...
```

---

## 10. Intercepting Proxy & HTTPS CA Certificate

ARTEX includes an integrated recording proxy on port `8788` (`127.0.0.1:8788`) for capturing HTTP/HTTPS traffic.

1. When proxying HTTPS traffic, the proxy dynamically generates certificates signed by a local Root CA stored in `/var/lib/artex/data/ca/`.
2. To inspect HTTPS traffic from tools or browsers without certificate warnings:
   - Export root certificate:
     ```bash
     sudo cp /var/lib/artex/data/ca/mitmproxy-ca-cert.pem /etc/ca-certificates/trust-source/anchors/artex-proxy-ca.crt
     sudo trust extract-compat
     ```
   - For browser profiles (Firefox/Chromium), import `mitmproxy-ca-cert.pem` as an Authorities trust anchor.

---

## 11. Security & Sandboxing Details

The `artex.service` unit implements Arch Linux systemd sandboxing:
- `User=artex` & `Group=artex`: Process executes under an unprivileged daemon account.
- `ProtectSystem=strict`: System directories (`/usr`, `/boot`, `/etc`) are mounted read-only.
- `ProtectHome=yes`: Denies all access to `/home` and `/root`.
- `ReadWritePaths=/var/lib/artex`: Explicit write isolation to ARTEX state and data directories.
- `ReadOnlyPaths=/etc/artex`: Configuration files are readable but immutable to the service.
- `PrivateTmp=yes` & `PrivateDevices=yes`: Private namespace for `/tmp` and physical device masking.
- `NoNewPrivileges=yes`: Prevents privilege escalation.
- `RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX`: Network restricted to IPv4, IPv6, and local Unix domain sockets.
- `SystemCallFilter=@system-service`: Syscall whitelist filtering out dangerous/privileged kernel calls.
