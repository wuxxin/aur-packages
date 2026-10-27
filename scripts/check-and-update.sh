#!/usr/bin/env bash
#
# Check upstream releases for AUR PKGBUILDs using nvchecker.
# If newer releases are available, updates PKGBUILD, regenerates
# checksums with updpkgsums, updates .SRCINFO, and optionally creates a PR.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Ensure scripts directory is in PATH (provides scripts/updpkgsums fallback)
export PATH="${SCRIPT_DIR}:${PATH}"

DEFAULT_PACKAGES=(
    "coreos-installer"
    "python-torchao-rocm"
    "python-torchaudio-rocm"
    "python-torchvision-rocm"
    "salt"
)

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS] [PACKAGE...]

Check upstream versions using nvchecker and update PKGBUILDs when newer.

Options:
  -d, --dry-run     Check versions without making any changes
      --no-pr       Update files locally without committing, pushing, or creating PRs
      --pr          Commit changes to a branch, push, and create a Pull Request via gh
  -h, --help        Show this help message and exit

Default packages checked:
  ${DEFAULT_PACKAGES[*]}
EOF
}

MODE="no-pr"
TARGET_PACKAGES=()

while [[ $# -gt 0 ]]; do
    case "$1" in
    -h | --help)
        usage
        exit 0
        ;;
    -d | --dry-run)
        MODE="dry-run"
        shift
        ;;
    --no-pr)
        MODE="no-pr"
        shift
        ;;
    --pr)
        MODE="pr"
        shift
        ;;
    -*)
        echo "Unknown option: $1" >&2
        usage
        exit 1
        ;;
    *)
        TARGET_PACKAGES+=("$1")
        shift
        ;;
    esac
done

if [[ ${#TARGET_PACKAGES[@]} -eq 0 ]]; then
    TARGET_PACKAGES=("${DEFAULT_PACKAGES[@]}")
fi

# Dependency checks
check_dependencies() {
    local missing=()
    if ! command -v nvchecker >/dev/null 2>&1; then
        missing+=("nvchecker (install via 'pip install nvchecker' or pacman)")
    fi
    if ! command -v makepkg >/dev/null 2>&1; then
        missing+=("makepkg (install via apt 'makepkg' on Ubuntu or 'base-devel' on Arch)")
    fi
    if ! command -v updpkgsums >/dev/null 2>&1; then
        missing+=("updpkgsums (provided in scripts/updpkgsums or via pacman-contrib)")
    fi
    if ! command -v git >/dev/null 2>&1; then
        missing+=("git")
    fi
    if [[ "${MODE}" == "pr" ]] && ! command -v gh >/dev/null 2>&1; then
        missing+=("gh (GitHub CLI)")
    fi

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Error: Missing required dependencies:" >&2
        for dep in "${missing[@]}"; do
            echo "  - ${dep}" >&2
        done
        exit 1
    fi
}

check_dependencies

# Setup temporary nvchecker keyfile if GITHUB_TOKEN is available
KEYFILE=""
NVCHECKER_OPTS=()
TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
if [[ -n "${TOKEN}" ]]; then
    KEYFILE="$(mktemp "${TMPDIR:-/tmp}/nvchecker-key.XXXXXX.toml")"
    cat <<EOF >"${KEYFILE}"
[keys]
github = "${TOKEN}"
EOF
    NVCHECKER_OPTS+=("-k" "${KEYFILE}")
fi

# shellcheck disable=SC2329
cleanup() {
    if [[ -n "${KEYFILE}" && -f "${KEYFILE}" ]]; then
        rm -f "${KEYFILE}"
    fi
}
trap cleanup EXIT

# Version compare helper (vercmp or python packaging fallback)
compare_versions() {
    local v1="$1"
    local v2="$2"

    if command -v vercmp >/dev/null 2>&1; then
        vercmp "${v1}" "${v2}"
        return
    fi

    python3 -c "
import sys
try:
    from pyalpm import vercmp
    print(vercmp(sys.argv[1], sys.argv[2]))
except Exception:
    import subprocess
    try:
        res = subprocess.run(['vercmp', sys.argv[1], sys.argv[2]], capture_output=True, text=True, check=True)
        print(res.stdout.strip())
    except Exception:
        from packaging.version import parse
        v1, v2 = parse(sys.argv[1]), parse(sys.argv[2])
        print(1 if v1 > v2 else (-1 if v1 < v2 else 0))
" "${v1}" "${v2}"
}

cd "${REPO_ROOT}"

BASE_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")"
if [[ "${BASE_BRANCH}" == "HEAD" ]]; then
    BASE_BRANCH="main"
fi

echo "==> Running upstream version check (mode: ${MODE}, base branch: ${BASE_BRANCH})..."

UPDATED_PKGS=()
UPTODATE_PKGS=()
FAILED_PKGS=()
SKIPPED_PKGS=()

for pkg in "${TARGET_PACKAGES[@]}"; do
    pkg_dir="${REPO_ROOT}/${pkg}"
    if [[ ! -d "${pkg_dir}" ]]; then
        echo "Warning: Directory not found for '${pkg}', skipping." >&2
        FAILED_PKGS+=("${pkg}: directory not found")
        continue
    fi

    pkgbuild="${pkg_dir}/PKGBUILD"
    nvconfig="${pkg_dir}/nvchecker.toml"

    if [[ ! -f "${pkgbuild}" ]]; then
        echo "Warning: '${pkgbuild}' not found, skipping." >&2
        FAILED_PKGS+=("${pkg}: PKGBUILD not found")
        continue
    fi

    if [[ ! -f "${nvconfig}" ]]; then
        echo "Warning: '${nvconfig}' not found, skipping." >&2
        FAILED_PKGS+=("${pkg}: nvchecker.toml not found")
        continue
    fi

    current_ver="$(grep -E '^[[:space:]]*pkgver=' "${pkgbuild}" | head -n1 | cut -d= -f2 | tr -d "'\"[:space:]")"
    if [[ -z "${current_ver}" ]]; then
        echo "Warning: Could not parse current pkgver from '${pkgbuild}', skipping." >&2
        FAILED_PKGS+=("${pkg}: failed to parse pkgver")
        continue
    fi

    echo "--> Checking ${pkg} (current: ${current_ver})..."

    # Run nvchecker
    nv_out="$(nvchecker --logger json "${NVCHECKER_OPTS[@]}" -c "${nvconfig}" 2>/dev/null || true)"
    upstream_ver="$(printf "%s\n" "${nv_out}" | python3 -c '
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        data = json.loads(line)
        if "version" in data and data.get("level") != "debug":
            print(data["version"])
            sys.exit(0)
    except Exception:
        pass
sys.exit(1)
' 2>/dev/null || true)"

    if [[ -z "${upstream_ver}" ]]; then
        echo "Warning: Failed to retrieve upstream version for '${pkg}' from nvchecker." >&2
        FAILED_PKGS+=("${pkg}: nvchecker returned no version")
        continue
    fi

    cmp="$(compare_versions "${upstream_ver}" "${current_ver}")"
    if [[ "${cmp}" -le 0 ]]; then
        echo "    Up-to-date: ${pkg} (upstream: ${upstream_ver}, local: ${current_ver})"
        UPTODATE_PKGS+=("${pkg} (${current_ver})")
        continue
    fi

    echo "    Update available for ${pkg}: ${current_ver} -> ${upstream_ver}"

    if [[ "${MODE}" == "dry-run" ]]; then
        UPDATED_PKGS+=("${pkg} (${current_ver} -> ${upstream_ver})")
        continue
    fi

    branch_name="update/${pkg}-${upstream_ver}"

    if [[ "${MODE}" == "pr" ]]; then
        # Check if an open or closed PR already exists
        existing_pr="$(gh pr list --head "${branch_name}" --state all --json number,url --jq '.[0].url // empty' 2>/dev/null || true)"
        if [[ -n "${existing_pr}" ]]; then
            echo "    PR already exists for ${pkg} ${upstream_ver}: ${existing_pr}"
            SKIPPED_PKGS+=("${pkg} (${existing_pr})")
            continue
        fi

        # Switch to branch created from base branch
        git checkout -B "${branch_name}" "${BASE_BRANCH}"
    fi

    # Update pkgver and reset pkgrel in PKGBUILD
    sed -i -E "s/^[[:space:]]*pkgver=.*/pkgver=${upstream_ver}/" "${pkgbuild}"
    sed -i -E "s/^[[:space:]]*pkgrel=.*/pkgrel=1/" "${pkgbuild}"

    # Run updpkgsums
    echo "    Running updpkgsums in ${pkg}..."
    if ! (cd "${pkg_dir}" && updpkgsums); then
        echo "==> ERROR: updpkgsums failed for ${pkg}!" >&2
        git checkout -- "${pkg_dir}"
        if [[ "${MODE}" == "pr" ]]; then
            git checkout "${BASE_BRANCH}"
            git branch -D "${branch_name}" 2>/dev/null || true
        fi
        FAILED_PKGS+=("${pkg}: updpkgsums failed")
        continue
    fi

    # Regenerate .SRCINFO
    echo "    Regenerating .SRCINFO in ${pkg}..."
    if ! (cd "${pkg_dir}" && makepkg --printsrcinfo >.SRCINFO); then
        echo "==> ERROR: makepkg --printsrcinfo failed for ${pkg}!" >&2
        git checkout -- "${pkg_dir}"
        if [[ "${MODE}" == "pr" ]]; then
            git checkout "${BASE_BRANCH}"
            git branch -D "${branch_name}" 2>/dev/null || true
        fi
        FAILED_PKGS+=("${pkg}: makepkg --printsrcinfo failed")
        continue
    fi

    if [[ "${MODE}" == "pr" ]]; then
        git add "${pkg_dir}/PKGBUILD" "${pkg_dir}/.SRCINFO"
        git commit -m "chore(${pkg}): update to ${upstream_ver}"
        echo "    Pushing branch ${branch_name}..."
        git push origin "${branch_name}" --force

        echo "    Creating pull request..."
        pr_body="$(
            cat <<EOF
## Automated Upstream Version Bump

- **Package:** \`${pkg}\`
- **Previous version:** \`${current_ver}\`
- **New version:** \`${upstream_ver}\`

### Changes
- Updated \`pkgver\` to \`${upstream_ver}\` and reset \`pkgrel\` to \`1\` in \`PKGBUILD\`
- Updated source checksums via \`updpkgsums\`
- Regenerated \`.SRCINFO\` via \`makepkg --printsrcinfo\`

*Automated by upstream version check action.*
EOF
        )"
        pr_url="$(
            gh pr create \
                --base "${BASE_BRANCH}" \
                --head "${branch_name}" \
                --title "chore(${pkg}): update to ${upstream_ver}" \
                --body "${pr_body}"
        )"

        echo "==> Opened PR: ${pr_url}"
        git checkout "${BASE_BRANCH}"
        UPDATED_PKGS+=("${pkg} (${current_ver} -> ${upstream_ver}) - ${pr_url}")
    else
        UPDATED_PKGS+=("${pkg} (${current_ver} -> ${upstream_ver})")
    fi
done

echo ""
echo "================ Summary ================"
echo "Up-to-date: ${#UPTODATE_PKGS[@]}"
for item in "${UPTODATE_PKGS[@]}"; do
    echo "  - ${item}"
done

echo "Updated: ${#UPDATED_PKGS[@]}"
for item in "${UPDATED_PKGS[@]}"; do
    echo "  - ${item}"
done

if [[ ${#SKIPPED_PKGS[@]} -gt 0 ]]; then
    echo "Skipped: ${#SKIPPED_PKGS[@]}"
    for item in "${SKIPPED_PKGS[@]}"; do
        echo "  - ${item}"
    done
fi

if [[ ${#FAILED_PKGS[@]} -gt 0 ]]; then
    echo "Failed: ${#FAILED_PKGS[@]}"
    for item in "${FAILED_PKGS[@]}"; do
        echo "  - ${item}"
    done
    exit 1
fi

exit 0
