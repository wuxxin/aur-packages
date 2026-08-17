#!/usr/bin/env bash
# Push maintained packages to AUR using archosaur.
# shellcheck shell=bash disable=SC2034

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

usage() {
    cat <<EOF
Usage: ${0##*/} [OPTIONS] [PACKAGE...]
       ${0##*/} -a|--all [OPTIONS]

Pushes official AUR-maintained packages to the AUR via archosaur.
By default, only packages with changes compared to live AUR are pushed.

OPTIONS:
    -a, --all        Process all maintained packages from README.md
    -n, --dry-run    Show what would be pushed without invoking archosaur
    -l, --list       List maintained packages and their AUR sync status
    -f, --force      Force push even if package matches live AUR
    -s, --speedup    Pass --speedup (-s) to archosaur (records subtree history)
    -h, --help       Show this usage message

EXAMPLES:
    ${0##*/} -l                      # List sync status against AUR
    ${0##*/} -a -n                   # Dry-run on all changed packages
    ${0##*/} -a                      # Push all modified maintained packages
    ${0##*/} python-torchao-rocm     # Push single package if changed
    ${0##*/} -f python-torchao-rocm  # Force push single package
EOF
}

# No arguments provided: display usage and exit
if [[ $# -eq 0 ]]; then
    usage
    exit 0
fi

# Extract maintained packages from README.md
get_maintained_packages() {
    local readme="${REPO_ROOT}/README.md"
    if [[ ! -f "${readme}" ]]; then
        echo "Error: README.md not found in ${REPO_ROOT}" >&2
        exit 1
    fi

    awk '
        /^## AUR Maintained Packages/ { in_section = 1; next }
        /^## / && in_section { in_section = 0 }
        in_section && /^- \[[a-zA-Z0-9._-]+\]\([a-zA-Z0-9._-]+\)/ {
            match($0, /^- \[([^\]]+)\]/, arr)
            if (arr[1] != "") {
                print arr[1]
            }
        }
    ' "${readme}"
}

# Fetch remote .SRCINFO from AUR for a given package
get_remote_srcinfo() {
    local pkg="$1"
    local url="https://aur.archlinux.org/cgit/aur.git/plain/.SRCINFO?h=${pkg}"
    curl -fsSL --max-time 6 "${url}" 2>/dev/null || true
}

# Compare local .SRCINFO against live AUR
# Returns:
#   0: identical (UP-TO-DATE)
#   1: modified (DIFFERS)
#   2: not found on AUR (NOT-ON-AUR)
check_aur_diff() {
    local pkg="$1"
    local local_srcinfo="$2"
    local remote_srcinfo

    remote_srcinfo="$(get_remote_srcinfo "${pkg}")"
    if [[ -z "${remote_srcinfo}" ]]; then
        return 2
    fi

    local clean_local clean_remote
    clean_local="$(echo "${local_srcinfo}" | tr -d '\r' | sed -e 's/[[:space:]]*$//' -e '/^$/d')"
    clean_remote="$(echo "${remote_srcinfo}" | tr -d '\r' | sed -e 's/[[:space:]]*$//' -e '/^$/d')"

    if [[ "${clean_local}" == "${clean_remote}" ]]; then
        return 0
    else
        return 1
    fi
}

DRY_RUN=0
LIST_ONLY=0
FORCE=0
PROCESS_ALL=0
SPEEDUP_FLAG=""
TARGET_PACKAGES=()

while [[ $# -gt 0 ]]; do
    case "$1" in
    -h | --help)
        usage
        exit 0
        ;;
    -a | --all)
        PROCESS_ALL=1
        shift
        ;;
    -n | --dry-run)
        DRY_RUN=1
        shift
        ;;
    -l | --list)
        LIST_ONLY=1
        shift
        ;;
    -f | --force)
        FORCE=1
        shift
        ;;
    -s | --speedup)
        SPEEDUP_FLAG="-s"
        shift
        ;;
    -*)
        echo "Error: Unknown option '$1'" >&2
        usage >&2
        exit 1
        ;;
    *)
        TARGET_PACKAGES+=("$1")
        shift
        ;;
    esac
done

if ! command -v archosaur >/dev/null 2>&1; then
    echo "Error: 'archosaur' utility not found in PATH." >&2
    exit 1
fi

cd "${REPO_ROOT}"

if [[ ${PROCESS_ALL} -eq 1 || ${LIST_ONLY} -eq 1 ]]; then
    mapfile -t MAINTAINED < <(get_maintained_packages)
    if [[ ${#TARGET_PACKAGES[@]} -eq 0 ]]; then
        TARGET_PACKAGES=("${MAINTAINED[@]}")
    fi
fi

if [[ ${#TARGET_PACKAGES[@]} -eq 0 ]]; then
    echo "Error: No target packages specified. Use -a/--all or specify package names." >&2
    usage >&2
    exit 1
fi

# List mode: query and print status for each target
if [[ ${LIST_ONLY} -eq 1 ]]; then
    printf "%-32s %s\n" "PACKAGE" "AUR STATUS"
    for pkg in "${TARGET_PACKAGES[@]}"; do
        pkg_dir="${REPO_ROOT}/${pkg}"
        if [[ ! -d "${pkg_dir}" || ! -f "${pkg_dir}/PKGBUILD" ]]; then
            printf "%-32s %s\n" "${pkg}" "MISSING-LOCAL"
            continue
        fi

        local_srcinfo="$(cd "${pkg_dir}" && makepkg --printsrcinfo 2>/dev/null || true)"
        if [[ -z "${local_srcinfo}" ]]; then
            printf "%-32s %s\n" "${pkg}" "INVALID-SRCINFO"
            continue
        fi

        if check_aur_diff "${pkg}" "${local_srcinfo}"; then
            printf "%-32s %s\n" "${pkg}" "UP-TO-DATE"
        else
            status_code=$?
            if [[ ${status_code} -eq 1 ]]; then
                printf "%-32s %s\n" "${pkg}" "DIFFERS (needs push)"
            else
                printf "%-32s %s\n" "${pkg}" "NOT-ON-AUR"
            fi
        fi
    done
    exit 0
fi

echo "Processing ${#TARGET_PACKAGES[@]} package(s) (dry-run: ${DRY_RUN}, force: ${FORCE})..."

FAILED_PKGS=()
SUCCESS_PKGS=()
SKIPPED_PKGS=()

for pkg in "${TARGET_PACKAGES[@]}"; do
    pkg_dir="${REPO_ROOT}/${pkg}"

    if [[ ! -d "${pkg_dir}" || ! -f "${pkg_dir}/PKGBUILD" ]]; then
        echo "[SKIP] '${pkg}' not found in repo."
        SKIPPED_PKGS+=("${pkg}")
        continue
    fi

    # Generate current .SRCINFO content
    local_srcinfo="$(cd "${pkg_dir}" && makepkg --printsrcinfo 2>/dev/null || true)"
    if [[ -z "${local_srcinfo}" ]]; then
        echo "[FAIL] Could not generate .SRCINFO for '${pkg}'."
        FAILED_PKGS+=("${pkg}")
        continue
    fi

    # Check diff against live AUR
    needs_push=0
    if [[ ${FORCE} -eq 1 ]]; then
        echo "[FORCE] Pushing '${pkg}' without AUR diff check."
        needs_push=1
    else
        if check_aur_diff "${pkg}" "${local_srcinfo}"; then
            echo "[UP-TO-DATE] '${pkg}' matches live AUR. Skipping."
            SKIPPED_PKGS+=("${pkg}")
            continue
        else
            status_code=$?
            if [[ ${status_code} -eq 1 ]]; then
                echo "[DIFFERS] '${pkg}' has changes compared to live AUR."
                needs_push=1
            else
                echo "[NOT-ON-AUR] '${pkg}' is not registered on AUR."
                # Only push unregistered if explicitly given on CLI or forced
                if [[ ${PROCESS_ALL} -eq 0 ]]; then
                    needs_push=1
                else
                    echo "  Skipping unregistered package in bulk push mode."
                    SKIPPED_PKGS+=("${pkg}")
                    continue
                fi
            fi
        fi
    fi

    if [[ ${needs_push} -eq 1 ]]; then
        # Ensure .SRCINFO file on disk is updated
        echo "${local_srcinfo}" >"${pkg_dir}/.SRCINFO"

        cmd=(archosaur)
        if [[ -n "${SPEEDUP_FLAG}" ]]; then
            cmd+=("${SPEEDUP_FLAG}")
        fi
        cmd+=("${pkg}")

        if [[ ${DRY_RUN} -eq 1 ]]; then
            echo "  [DRY-RUN] Would run: ${cmd[*]}"
            SUCCESS_PKGS+=("${pkg}")
        else
            echo "  Running: ${cmd[*]}"
            if "${cmd[@]}"; then
                echo "  [SUCCESS] Pushed '${pkg}'."
                SUCCESS_PKGS+=("${pkg}")
            else
                echo "  [FAIL] Failed pushing '${pkg}'." >&2
                FAILED_PKGS+=("${pkg}")
            fi
        fi
    fi
done

echo "Done: ${#SUCCESS_PKGS[@]} pushed, ${#SKIPPED_PKGS[@]} up-to-date/skipped, ${#FAILED_PKGS[@]} failed."

if [[ ${#FAILED_PKGS[@]} -gt 0 ]]; then
    exit 1
fi

exit 0
