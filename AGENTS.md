# AGENTS.md

## Overview

This is an **AUR (Arch User Repository) packages** repository containing:
- PKGBUILD files for building Arch Linux packages

## Repository Structure

```
aur-packages/
├── README.md             # Human targeted README.md , list of currently available pkgs
├── libggml-git-hip/      # HIP/ROCm accelerated GGML + llama.cpp + whisper.cpp
├── python-torch*-rocm/   # PyTorch ROCm builds
|__ scripts/              # utility scripts
|__ research/             # `weekly-devel-activity.md`,  `tei-and-mlc-build.md` , `research-crispasr-ggml-mod.md`
|__ scratch/              # scratch space for agents to work or research (checkedout source code for package or build testing, etc)
└── ...                   # Other AUR packages (each AUR package has its own directory with PKGBUILD)
```

## Code Style Guidelines and Build/Lint/Test Commands

### Shell Scripts (PKGBUILD, .sh)
- **Shebang**: `#!/usr/bin/env bash`
- **Indentation**: 4 spaces (no tabs)
- **Variables**: lowercase_with_underscores
- **Constants**: UPPERCASE
- **Error handling**: Use `set -euo pipefail` at script top
- **Quotes**: Always quote variables: `"$var"`
- **Command substitution**: Use `$(...)` not backticks
- **Lint**: `shellcheck scripts/*.sh`
- **Format**: `shfmt -i 4 -w scripts/*.sh`
  - format requires -i 4 to enforce the 4-space indentation style

### Python Scripts
- **Shebang**: `#!/usr/bin/env python`
- **Imports**: stdlib, third-party, local
- **Indentation**: 4 spaces
- **Types**: Use type hints where practical
- **Naming**: `snake_case` functions/variables, `PascalCase` classes
- **Docstrings**: Triple quotes `"""docstring"""`
- **Error handling**: Use specific exceptions, not bare `except:`
- **Lint**: `ruff check scripts/*.py`
- **Format**: `ruff format scripts/*.py`
- **Type check**: `mypy scripts/*.py`
- **Run a single test**: `pytest tests/test_file.py::test_function -v`

### PKGBUILD Files
- **Maintainer**: Include at top
- **Indentation**: 4 spaces
- **pkgver**: Use `pkgver()` function for git packages
- **Functions**: `prepare()`, `build()`, `check()`, `package_<pkgname>()`
- **Quotes**: Quote all variable expansions
- **Arrays**: Use `()` syntax, reference with `${arr[@]}`
- **Local vars**: Use `local` keyword
- **Clean and update Sources and PKGSUMS and apply patches**: `updpkgsums && makepkg -Co`
- **Regenerate .SRCINFO**: `makepkg --printsrcinfo > .SRCINFO`
- **Force a full rebuild**: `makepkg -Cf`
- **Run namcap on built package**: `namcap <package>.pkg.tar.zst`

### Desktop Files (.desktop)
- **Exec**: Use `%h` for home directory (e.g., `%h/.local/bin/app`)
- **TryExec**: Check if command exists before showing in menu
- **Categories**: Follow FreeDesktop.org standards

## Working with This Repository
- This Repository contains custom builds of complex software (llama.cpp, PyTorch with ROCm)
- Many packages have HIP/ROCm hardware acceleration requirements
- Some packages are experimental or personal forks
- Update README.md if significant changes or additions are made
- Verify dependencies when modifying PKGBUILDs, ask human to install needed dependencies.
- Test PKGBUILDs with `makepkg --nobuild` first
- Be Smart how to build: Large packages (such as `llama.cpp` or vllm) take substantial time to compile. During optimization, debugging, or iteration, avoid running clean builds or forcing a full rebuild (`makepkg -Cf`) repeatedly.
   - Use `makepkg -e` (or `makepkg --noextract`) to compile while preserving the existing `src` build tree and avoiding re-extracting or re-downloading.
   - Run tests directly against binaries in the `src/build_*` directories (or staging folders) without executing system-wide installations.
   - Use environment overrides (such as `GGML_BACKEND_PATH`, `LLAMA_SERVER_BIN`, etc.) to test custom-built dynamic libraries/binaries.
- Follow existing package directory structure
- Place patches in package directory, reference in `source` array
- To regenerate the report about the development activity of the upstream sources for the PKGBUILD's of this repo: Run the script on demand to research upstream change statistics. First execute without "--write", if all worked, use "--write" to directly write the updated tables back into `research/weekly-devel-activity.md`:
   ```bash
   python scripts/update-activity.py [--write]
   ```
