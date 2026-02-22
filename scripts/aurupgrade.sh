#!/usr/bin/env bash
set -euo pipefail

echo ":: Initializing sudo credentials..."
if ! sudo -v; then
	echo ":: Sudo failed, exiting."
	exit 1
fi

echo ":: Calculating dependency order for AUR packages..."
# Get the list (Sorted by dependency, filtered for AUR only)
# LC_ALL=C ensures we can grep for "AUR" even if system is in another language
updates=$(LC_ALL=C pamac upgrade -a --dry-run --no-confirm |
	grep -E '^\s\s\S+.*AUR' |
	awk '{print $1}' | tr "\n" " ")

if [ -z "$updates" ]; then
	echo ":: No AUR updates found."
	exit 0
fi

# Loop through the sorted list
for pkg in $updates; do
	echo "------------------------------------------------"
	echo ":: Updating: $pkg"
	echo "------------------------------------------------"
	# Build the package.
	# '|| echo' ensures the loop continues if one fails.
	pamac build "$pkg" --no-confirm || echo "!! FAILED: $pkg (Skipping to next...)"
done

echo "------------------------------------------------"
echo ":: AUR Upgrade process finished."
