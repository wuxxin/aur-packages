#!/usr/bin/env bash
# Cleanup temporary and build files in aur-packages based on .gitignore rules.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

usage() {
    cat <<EOF
Usage: ${0##*/} [OPTIONS]

Scans the root .gitignore and all package-level .gitignore files,
combines and prefixes their patterns, filters out 'scratch' and '*pkg*' patterns,
discovers matching build/temporary artifacts on disk, and optionally deletes them.

OPTIONS:
    -d, --delete     Delete all matched temporary and build files/directories
    -n, --dry-run    Preview matching patterns and files without deleting (default)
    -h, --help       Show this usage message

EXAMPLES:
    ${0##*/}              # Preview artifacts to be cleaned
    ${0##*/} --delete     # Delete matching artifacts
EOF
}

DO_DELETE=0

while [[ $# -gt 0 ]]; do
    case "$1" in
    -d | --delete)
        DO_DELETE=1
        shift
        ;;
    -n | --dry-run)
        DO_DELETE=0
        shift
        ;;
    -h | --help)
        usage
        exit 0
        ;;
    *)
        echo "Error: Unknown option '$1'" >&2
        usage
        exit 1
        ;;
    esac
done

echo "==> Scanning .gitignore files in ${REPO_ROOT}..."

# Collect .gitignore files: root level and 1 level down (package directories)
GITIGNORE_FILES=()
if [[ -f "${REPO_ROOT}/.gitignore" ]]; then
    GITIGNORE_FILES+=("${REPO_ROOT}/.gitignore")
fi

while IFS= read -r -d '' f; do
    GITIGNORE_FILES+=("$f")
done < <(find "${REPO_ROOT}" -mindepth 2 -maxdepth 2 -name ".gitignore" -print0 | sort -z)

echo "Found ${#GITIGNORE_FILES[@]} .gitignore files."

# Extract and prefix patterns
RAW_PATTERNS=()
for gifile in "${GITIGNORE_FILES[@]}"; do
    rel_dir="$(dirname "${gifile#"${REPO_ROOT}/"}")"
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Trim leading and trailing whitespace
        line="$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

        # Skip empty lines and comments
        if [[ -z "$line" || "$line" =~ ^# ]]; then
            continue
        fi

        # Strip leading slash
        clean_pat="${line#/}"

        # Prefix with relative directory if not root
        if [[ "$rel_dir" != "." && -n "$rel_dir" ]]; then
            full_pat="${rel_dir}/${clean_pat}"
        else
            full_pat="${clean_pat}"
        fi

        # Filter out scratch patterns
        pat_lower="$(echo "$full_pat" | tr '[:upper:]' '[:lower:]')"
        if [[ "$pat_lower" == *scratch* ]]; then
            continue
        fi

        # Filter out any pattern containing pkg
        if [[ "$pat_lower" == *pkg* ]]; then
            continue
        fi

        RAW_PATTERNS+=("$full_pat")
    done <"$gifile"
done

# Sort and deduplicate patterns
mapfile -t UNIQUE_PATTERNS < <(printf '%s\n' "${RAW_PATTERNS[@]}" | sort -u)

echo ""
echo "==> Clean patterns (${#UNIQUE_PATTERNS[@]} unique patterns, excluding 'scratch' and '*pkg*'):"
for pat in "${UNIQUE_PATTERNS[@]}"; do
    echo "  - ${pat}"
done

echo ""
echo "==> Traversing filesystem for matching build/temporary artifacts..."

MATCHES=()
for pat in "${UNIQUE_PATTERNS[@]}"; do
    # Strip trailing slashes for glob matching
    clean_target="${pat%/}"

    # Use nullglob to expand glob cleanly
    shopt -s nullglob globstar dotglob
    # shellcheck disable=SC2206
    expanded=("${REPO_ROOT}"/${clean_target})
    shopt -u nullglob globstar dotglob

    for item in "${expanded[@]}"; do
        if [[ -e "$item" || -L "$item" ]]; then
            rel_path="${item#"${REPO_ROOT}/"}"
            rel_lower="$(echo "$rel_path" | tr '[:upper:]' '[:lower:]')"

            # Safety guard: Never touch scratch or pkg paths
            if [[ "$rel_lower" == *scratch* || "$rel_lower" == *pkg* ]]; then
                continue
            fi

            MATCHES+=("$rel_path")
        fi
    done
done

# Sort and deduplicate matches
if [[ ${#MATCHES[@]} -gt 0 ]]; then
    mapfile -t UNIQUE_MATCHES < <(printf '%s\n' "${MATCHES[@]}" | sort -u)
else
    UNIQUE_MATCHES=()
fi

echo ""
if [[ ${#UNIQUE_MATCHES[@]} -eq 0 ]]; then
    echo "==> No matching temporary or build files found on disk."
    exit 0
fi

echo "==> Matches found (${#UNIQUE_MATCHES[@]} items):"
TOTAL_BYTES=0
for rel in "${UNIQUE_MATCHES[@]}"; do
    full_path="${REPO_ROOT}/${rel}"
    if [[ -d "$full_path" && ! -L "$full_path" ]]; then
        type_str="DIR "
        size_bytes="$(du -sb "$full_path" 2>/dev/null | cut -f1 || echo 0)"
        size_hr="$(du -sh "$full_path" 2>/dev/null | cut -f1 || echo "0B")"
    else
        type_str="FILE"
        size_bytes="$(stat -c%s "$full_path" 2>/dev/null || echo 0)"
        size_hr="$(numfmt --to=iec-i --suffix=B "$size_bytes" 2>/dev/null || echo "${size_bytes}B")"
    fi
    TOTAL_BYTES=$((TOTAL_BYTES + size_bytes))
    printf "  [%s] %-55s (%s)\n" "$type_str" "$rel" "$size_hr"
done

TOTAL_HR="$(numfmt --to=iec-i --suffix=B "$TOTAL_BYTES" 2>/dev/null || echo "${TOTAL_BYTES}B")"
echo ""
echo "Total disk space occupied: ${TOTAL_HR}"

if [[ $DO_DELETE -eq 1 ]]; then
    echo ""
    echo "==> Deleting ${#UNIQUE_MATCHES[@]} matching targets..."
    for rel in "${UNIQUE_MATCHES[@]}"; do
        full_path="${REPO_ROOT}/${rel}"
        # Safety checks before removal
        if [[ "$rel" == *scratch* || "$rel" == *pkg* || "$rel" == "." || "$rel" == ".." || -z "$rel" ]]; then
            echo "  [SKIPPED] Refusing to delete safety-restricted path: ${rel}"
            continue
        fi

        if [[ -e "$full_path" || -L "$full_path" ]]; then
            rm -rf "$full_path"
            echo "  [DELETED] ${rel}"
        fi
    done
    echo ""
    echo "==> Cleanup complete. Freed ${TOTAL_HR}."
else
    echo ""
    echo "==> Dry-run mode: No files were deleted."
    echo "==> To delete these files, re-run with: ${0##*/} --delete"
fi
