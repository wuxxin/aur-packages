#!/usr/bin/env bash
# Cleanup temporary and build files in aur-packages based on .gitignore rules.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

usage() {
    cat <<EOF
Usage: ${0##*/} [OPTIONS]

Scans the root .gitignore and all package-level .gitignore files,
combines and prefixes their patterns, filters out 'scratch' patterns,
discovers matching build/temporary artifacts on disk, and optionally deletes them.

Package files that are installable or distributable (see KEEP GLOBS below) are
never deleted, even when a .gitignore pattern matches them. Negation lines in
.gitignore files ('!pattern') are honoured as permanent keep-rules: a path that
matches a negation is excluded from cleanup.

KEEP GLOBS (basename patterns, always protected):
    *.pkg.tar.*   built installable packages
    *.src.tar.*   source package archives
    pkgver*.tar*  upstream release tarballs kept for PKGBUILD updates

OPTIONS:
    -d, --delete     Delete all matched temporary and build files/directories
    -n, --dry-run    Preview matching patterns and files without deleting (default)
    -k, --keep GLOB  Add an extra basename pattern that is never deleted
                     (repeatable; also protects the named file from negation-free cleanup)
    -h, --help       Show this usage message

EXAMPLES:
    ${0##*/}                          # Preview artifacts to be cleaned
    ${0##*/} --delete                 # Delete matching artifacts
    ${0##*/} -k '*.onnx' --delete     # Also keep every .onnx model file
EOF
}

DO_DELETE=0
KEEP_GLOBS=('*.pkg.tar.*' '*.src.tar.*' '*pkgver*.tar*')

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
    -k | --keep)
        if [[ $# -lt 2 ]]; then
            echo "Error: --keep requires a glob argument" >&2
            exit 1
        fi
        KEEP_GLOBS+=("$2")
        shift 2
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

# Paths matching one of the keep globs (basename match, plus 'dir/**' style globs).
is_kept() {
    local rel="$1" base="${1##*/}" pat pat_base
    for pat in "${KEEP_GLOBS[@]}"; do
        pat_base="${pat##*/}"
        # shellcheck disable=SC2053  # right-hand side is a glob on purpose
        if [[ "$base" == $pat || "$rel" == $pat ]]; then
            return 0
        fi
        if [[ -n "$pat_base" && "$rel" == */"$pat_base" ]]; then
            return 0
        fi
    done
    return 1
}

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

# Extract and prefix patterns; negation lines become keep-rules instead.
RAW_PATTERNS=()
RAW_KEEPS=()
for gifile in "${GITIGNORE_FILES[@]}"; do
    rel_dir="$(dirname "${gifile#"${REPO_ROOT}/"}")"
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Trim leading and trailing whitespace
        line="$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

        # Skip empty lines and comments
        if [[ -z "$line" || "$line" =~ ^# ]]; then
            continue
        fi

        is_negation=0
        if [[ "$line" == '!'* ]]; then
            is_negation=1
            line="${line#!}"
        fi

        # Strip leading slash
        clean_pat="${line#/}"

        # Prefix with relative directory if not root
        if [[ "$rel_dir" != "." && -n "$rel_dir" ]]; then
            full_pat="${rel_dir}/${clean_pat}"
        else
            full_pat="${clean_pat}"
        fi

        # Filter out scratch patterns (agent workspace, never auto-cleaned)
        pat_lower="$(echo "$full_pat" | tr '[:upper:]' '[:lower:]')"
        if [[ "$pat_lower" == *scratch* ]]; then
            continue
        fi

        if [[ $is_negation -eq 1 ]]; then
            RAW_KEEPS+=("$full_pat")
            continue
        fi

        RAW_PATTERNS+=("$full_pat")
    done <"$gifile"
done

# Sort, drop empty entries (an empty pattern would expand to REPO_ROOT), deduplicate.
mapfile -t UNIQUE_PATTERNS < <(printf '%s\n' "${RAW_PATTERNS[@]}" | grep -v '^$' || true)
if [[ ${#RAW_KEEPS[@]} -gt 0 ]]; then
    mapfile -t UNIQUE_KEEPS < <(printf '%s\n' "${RAW_KEEPS[@]}" | grep -v '^$' || true)
else
    UNIQUE_KEEPS=()
fi

echo ""
echo "==> Clean patterns (${#UNIQUE_PATTERNS[@]} unique patterns, excluding 'scratch'):"
for pat in "${UNIQUE_PATTERNS[@]}"; do
    echo "  - ${pat}"
done

echo ""
echo "==> Protected paths (.gitignore negations: ${#UNIQUE_KEEPS[@]}, keep globs: ${#KEEP_GLOBS[@]}):"
for pat in "${UNIQUE_KEEPS[@]}"; do
    echo "  ! ${pat}"
done
for pat in "${KEEP_GLOBS[@]}"; do
    echo "  # ${pat}"
done

echo ""
echo "==> Traversing filesystem for matching build/temporary artifacts..."

MATCHES=()
KEPT_COUNT=0
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

            # Safety guard: Never touch the agent scratch workspace
            if [[ "$rel_lower" == *scratch* ]]; then
                continue
            fi

            # Keep-rules: installable package files and .gitignore negations win.
            if is_kept "$rel_path"; then
                KEPT_COUNT=$((KEPT_COUNT + 1))
                continue
            fi
            kept=0
            for keep in "${UNIQUE_KEEPS[@]}"; do
                # shellcheck disable=SC2053  # left side compared as glob against negation pattern
                if [[ "$rel_path" == $keep || "${rel_path##*/}" == "${keep##*/}" ]]; then
                    kept=1
                    KEPT_COUNT=$((KEPT_COUNT + 1))
                    break
                fi
            done
            [[ $kept -eq 1 ]] && continue

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

echo "==> Matches found (${#UNIQUE_MATCHES[@]} items, ${KEPT_COUNT} protected by keep-rules):"
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
        if [[ "$rel" == *scratch* || "$rel" == "." || "$rel" == ".." || -z "$rel" ]] || is_kept "$rel"; then
            echo "  [SKIPPED] Refusing to delete protected path: ${rel}"
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
