# AGENTS.md - Guidelines for Agents Working in This Repository

## Overview

This is an **AUR (Arch User Repository) packages** repository containing:
- PKGBUILD files for building Arch Linux packages

## Repository Structure

```
aur-packages/
├── README.md             # Human targeted README.md , list of currently available pkgs
├── libggml-git-hip/      # HIP/ROCm accelerated GGML + llama.cpp + whisper.cpp
├── python-torch*-rocm/   # PyTorch ROCm builds
|__ scripts/              #  utility scripts
|__ scratch/              # scratch space for agents to work or research (checkedout source code for package or build testing, etc)
└── ...                   # Other AUR packages (each AUR package has its own directory with PKGBUILD)
```

## Build/Lint/Test Commands

### PKGBUILD Testing
```bash
# Dry-run build to check for errors
updpkgsums && makepkg -Co

# Force a full rebuild
makepkg -Cf

# Run namcap on built package
namcap <package>.pkg.tar.zst
```

### Python Scripts
```bash
# Lint
ruff check scripts/*.py
# Format
ruff format scripts/*.py
# Type check
mypy scripts/*.py
# Run a single test
pytest tests/test_file.py::test_function -v
```

### Shell Scripts
```bash
# Lint
shellcheck scripts/*.sh
# Format (requires -i 4 to enforce the 4-space indentation style)
shfmt -i 4 -w scripts/*.sh
```

## Code Style Guidelines

### Shell Scripts (PKGBUILD, .sh)
- **Shebang**: `#!/usr/bin/env bash`
- **Indentation**: 4 spaces (no tabs)
- **Variables**: lowercase_with_underscores
- **Constants**: UPPERCASE
- **Error handling**: Use `set -euo pipefail` at script top
- **Quotes**: Always quote variables: `"$var"`
- **Command substitution**: Use `$(...)` not backticks

### Python Scripts
- **Shebang**: `#!/usr/bin/env python`
- **Imports**: stdlib, third-party, local
- **Indentation**: 4 spaces
- **Types**: Use type hints where practical
- **Naming**: `snake_case` functions/variables, `PascalCase` classes
- **Docstrings**: Triple quotes `"""docstring"""`
- **Error handling**: Use specific exceptions, not bare `except:`

### PKGBUILD Files
- **Maintainer**: Include at top
- **pkgver**: Use `pkgver()` function for git packages
- **Functions**: `prepare()`, `build()`, `check()`, `package_<pkgname>()`
- **Quotes**: Quote all variable expansions
- **Arrays**: Use `()` syntax, reference with `${arr[@]}`
- **Local vars**: Use `local` keyword

Example:
```bash
# Maintainer: Your Name <email@example.com>
pkgbase=my-package-git
pkgname=('my-package')
pkgver=1.2.3.r4.gabcdef
pkgrel=1
pkgdesc="My package"
arch=('x86_64')

source=("my-package::git+https://github.com/user/repo.git")
sha256sums=(
    'SKIP'
)

pkgver() {
    cd my-package
    git describe --long --tags | sed 's/^v//;s/-/./g'
}

build() {
    cd my-package
    ./configure --prefix=/usr
    make
}
```

### Desktop Files (.desktop)
- **Exec**: Use `%h` for home directory (e.g., `%h/.local/bin/app`)
- **TryExec**: Check if command exists before showing in menu
- **Categories**: Follow FreeDesktop.org standards

## Common Patterns

### ROCm/HIP Builds
- Set `HIP_PLATFORM=amd` for AMD GPUs
- Use `rocm-supported-gfx` to detect GPU architectures
- Handle `GPU_TARGETS` environment variable

## Working with This Repository
1. Test PKGBUILDs with `makepkg --nobuild` first
2. Follow existing package directory structure
3. Place patches in package directory, reference in `source` array
4. Utility scripts go in `scripts/` directory

## Notes for Agents
- Contains custom builds of complex software (llama.cpp, PyTorch with ROCm)
- Many packages have HIP/ROCm acceleration requirements
- Some packages are experimental or personal forks
- Verify dependencies when modifying PKGBUILDs
- Update README.md if significant changes or additions are made
