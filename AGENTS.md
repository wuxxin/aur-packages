# AGENTS.md

## Repository Structure

- `README.md` — Human documentation, package list, AUR-synced vs. private forks.
- `libggml-git-hip/` — ROCm/HIP accelerated GGML, llama.cpp, whisper.cpp.
- `python-torch*-rocm/` — PyTorch ROCm builds.
- `<package-dir>/` — AUR package directories containing PKGBUILDs.
- `scripts/` — Repository utility scripts.
- `research/` — Development stats, build notes, and research reports.
- `scratch/` — Agent workspace (checkout sources, build logs, scratch testing).

## Working with This Repository

**Context:** Custom Arch PKGBUILDs for ROCm/HIP software (`llama.cpp`, PyTorch, vLLM) and experimental forks.

### Rules & Workflow

- **Workspace Isolation:** Use `scratch/` for temporary files, research, and git checkouts (`scratch/*-sources`). Always use the top-level repository root `scratch/`: if checked out independently, use its own root `scratch/`; if checked out as a git submodule, use the parent repository's root `scratch/`.
- **PKGBUILD Verification:** Run `makepkg --nobuild` first. Verify dependencies and ask user to install missing build deps.
- **Incremental Builds:** Avoid clean rebuilds (`makepkg -Cf`) on large packages.
  - Use `makepkg -e` (`--noextract`) to preserve the `src/` tree and avoid re-downloading/re-extracting.
  - Test binaries directly in `src/build_*` or staging folders without installing system-wide.
  - Use env overrides (`GGML_BACKEND_PATH`, `LLAMA_SERVER_BIN`) to test custom dynamic libs.
- **Package Layout:** Follow existing folder structures. Put patches in the package directory and reference them in `source=()`.
- **New Packages:** Include a `.gitignore` excluding source/package tarballs (`*.tar*`, `*.pkg.tar*`).
- **Docs** Update `README.md` on major changes.
- **Upstream Activity Stats**: if asked to do so, update upstream activity stats, first dry-run `python scripts/update-activity.py`, then run with `--write` to update `research/weekly-devel-activity.md`.


### Code Style & Tooling

#### Shell & PKGBUILDs (`.sh`, `PKGBUILD`)
- **Style:** `#!/usr/bin/env bash`, 4-space indent, `set -euo pipefail`, quote `"$var"`, use `$(...)`, use `local` in functions.
- **PKGBUILD Rules:** Top `# Maintainer:`, use `pkgver()` for git packages, quote arrays `${arr[@]}`.
- **Commands:**
  - Lint/Format `.sh`: `shellcheck scripts/*.sh` | `shfmt -i 4 -w scripts/*.sh`
  - Update sums/sources: `updpkgsums && makepkg -Co`
  - Regenerate `.SRCINFO`: `makepkg --printsrcinfo > .SRCINFO`
  - Force rebuild: `makepkg -Co`
  - Audit package: `namcap <package>.pkg.tar.zst`

#### Python Scripts
- **Style:** `#!/usr/bin/env python`, 4-space indent, type hints, `snake_case` (functions/vars), `PascalCase` (classes), triple-quote docstrings, specific exceptions.
- **Commands:** `ruff check scripts/*.py` | `ruff format scripts/*.py` | `mypy scripts/*.py` | `pytest tests/test_file.py::test_fn -v`

#### Desktop Files (`.desktop`)
- Use `%h` for home paths (`%h/.local/bin/app`), define `TryExec`, follow FreeDesktop.org categories.


### Shell Command Discipline (Log Management)

**CRITICAL Rule:** Never dump large command output (>100 lines) into context context. Redirect outputs (compilations, benchmarks) to `scratch/` logs and filter via `tail`/`grep`.

```bash
# General logging pattern
command > scratch/log 2>&1; grep -i "error\|warning\|EXIT" scratch/log | tail -20

# Build logging pattern
makepkg ... > scratch/build.log 2>&1 || grep -i "error" scratch/build.log | tail -30
```

Keep stderr separate when needed for debugging, but never print full unfiltered build streams.

