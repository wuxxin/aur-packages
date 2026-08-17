# push-aur.sh

Automated synchronization and publishing tool for official AUR-maintained packages within this monorepo using `archosaur`.

## Overview

`push-aur.sh` streamlines publishing packages to the Arch User Repository (AUR). Instead of blindly pushing all directories, it:
1. **Identifies Maintained Packages**: Dynamically extracts packages listed in the `## AUR Maintained Packages` section of `README.md` (ignoring private/testing forks).
2. **Performs Live AUR Diffing**: Queries `https://aur.archlinux.org` for each package's live `.SRCINFO` and skips packages that are already identical and up to date.
3. **Pushes Modified Packages**: Invokes `archosaur <package>` only on packages that have actual local changes (version bumps, dependency edits, checksum updates).

---

## Syntax & Options

```bash
./scripts/push-aur.sh [OPTIONS] [PACKAGE...]
./scripts/push-aur.sh -a|--all [OPTIONS]
```

### Options

| Flag | Name | Description |
| :--- | :--- | :--- |
| `-a` | `--all` | Target all packages listed under `## AUR Maintained Packages` in `README.md`. |
| `-n` | `--dry-run` | Preview which packages differ and would be pushed without executing `archosaur`. |
| `-l` | `--list` | Query live AUR status for all maintained packages and display a sync status table. |
| `-f` | `--force` | Bypass the live AUR diff check and force-push the package(s). |
| `-s` | `--speedup` | Pass `--speedup` (`-s`) to `archosaur` to record subtree history (`git subtree --rejoin`). |
| `-h` | `--help` | Show usage and options. |

> [!NOTE]
> Running `./scripts/push-aur.sh` without arguments displays usage instructions and exits safely without performing any network or git operations.

---

## Usage Examples

### 1. Check Live Sync Status
Displays a table of all maintained packages and whether they match what is live on the AUR:
```bash
./scripts/push-aur.sh -l
```

### 2. Dry-Run Bulk Sync
Simulates pushing all modified packages without publishing anything:
```bash
./scripts/push-aur.sh -a -n
```

### 3. Push All Modified Packages
Pushes only the packages that have changed compared to the AUR:
```bash
./scripts/push-aur.sh -a
```

### 4. Push a Specific Package
Checks if a specific package has changed, and pushes it if it differs:
```bash
./scripts/push-aur.sh python-torchao-rocm
```

### 5. Force Push
Pushes a package even if its `.SRCINFO` matches the remote version:
```bash
./scripts/push-aur.sh -f python-torchao-rocm
```

---

## Prerequisites & Setup

1. **`archosaur`**: Ensure `archosaur` is installed on your system (`which archosaur`).
2. **Git Hooks**: Ensure `archosaur setup` has been run in the repository root to enable automated `.SRCINFO` generation on git commits.
3. **SSH Access**: Ensure your AUR SSH key is configured in `~/.ssh/config` for `aur.archlinux.org`.
