#!/usr/bin/env python
"""update-oh-my-pi-status.py

A script to extract release notes from can1357/oh-my-pi over a specified
rolling window (default: 7 days) and compile a chronological module-by-module
analysis focusing on Breaking Changes, Added, Changed, Fixed, and Removed entries.

Usage:
    python scripts/update-oh-my-pi-status.py [--days 7] [--write]
"""

import argparse
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional


def run_cmd(cmd: List[str], cwd: Optional[str] = None) -> str:
    """Run a shell command and return its stdout as a string."""
    try:
        res = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def ensure_repo_sources() -> str:
    """Ensure the oh-my-pi repository is cloned/fetched and return its path."""
    pkg_src = "oh-my-pi-git-tag/src/oh-my-pi"
    bare_path = "oh-my-pi-git-tag/oh-my-pi"
    target_url = "https://github.com/can1357/oh-my-pi.git"

    if os.path.exists(pkg_src) and run_cmd(["git", "-C", pkg_src, "rev-parse", "HEAD"]):
        run_cmd(["git", "-C", pkg_src, "fetch", "origin"])
        return pkg_src

    if os.path.exists(bare_path) and run_cmd(["git", "-C", bare_path, "rev-parse", "HEAD"]):
        run_cmd(["git", "-C", bare_path, "fetch", "origin", "+refs/heads/*:refs/heads/*", "+refs/tags/*:refs/tags/*"])
        return bare_path

    os.makedirs("scratch", exist_ok=True)
    scratch_dir = os.path.join("scratch", "oh-my-pi")
    if not os.path.exists(scratch_dir):
        print(f"Cloning oh-my-pi into {scratch_dir}...")
        run_cmd(["git", "clone", "--depth", "3000", target_url, scratch_dir])
    else:
        run_cmd(["git", "-C", scratch_dir, "fetch", "origin"])
    return scratch_dir


def get_tags_in_window(repo_dir: str, days: int) -> List[Dict[str, str]]:
    """Return tags created in the last N days sorted chronologically (oldest to newest)."""
    fmt = "%(creatordate:short)%09%(refname:short)"
    output = run_cmd(["git", "-C", repo_dir, "tag", "-l", "--sort=creatordate", f"--format={fmt}"])
    
    cutoff_date = (datetime.date.today() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    results = []

    for line in output.splitlines():
        if not line or "\t" not in line:
            continue
        date_str, tag_name = line.split("\t", 1)
        if date_str >= cutoff_date and tag_name.startswith("v"):
            results.append({
                "tag": tag_name,
                "version": tag_name.lstrip("v"),
                "date": date_str,
            })

    return results


def parse_package_changelogs(repo_dir: str, target_versions: List[str]) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    """Parse all packages/*/CHANGELOG.md files for the target versions."""
    changelogs = glob.glob(f"{repo_dir}/packages/*/CHANGELOG.md")
    data_by_version: Dict[str, Dict[str, Dict[str, List[str]]]] = {v: {} for v in target_versions}

    for ch in sorted(changelogs):
        pkg_name = os.path.basename(os.path.dirname(ch))
        try:
            with open(ch, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            continue

        current_ver = None
        current_cat = None

        for line in lines:
            line_str = line.rstrip()
            m_ver = re.match(r"^## \[(\d+\.\d+\.\d+)\]", line_str)
            if m_ver:
                v = m_ver.group(1)
                current_ver = v if v in target_versions else None
                current_cat = None
                continue

            if current_ver:
                m_cat = re.match(r"^### (.*)", line_str)
                if m_cat:
                    current_cat = m_cat.group(1).strip()
                    continue

                if current_cat and line_str.startswith("- "):
                    bullet = line_str[2:].strip()
                    if pkg_name not in data_by_version[current_ver]:
                        data_by_version[current_ver][pkg_name] = {}
                    if current_cat not in data_by_version[current_ver][pkg_name]:
                        data_by_version[current_ver][pkg_name][current_cat] = []
                    data_by_version[current_ver][pkg_name][current_cat].append(bullet)

    return data_by_version


def extract_existing_summary(file_path: str) -> Optional[str]:
    """Extract existing Executive Summary section if present to avoid overwriting curated notes."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r"(## 🌐 Executive Summary.*?\n)(?=---|\Z)", content, re.DOTALL)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    return None


def generate_markdown(
    tags: List[Dict[str, str]],
    data_by_version: Dict[str, Dict[str, Dict[str, List[str]]]],
    start_date: str,
    end_date: str,
    days: int,
    existing_summary: Optional[str] = None,
) -> str:
    """Generate the markdown status report without hardcoding the executive summary."""
    oldest_tag = tags[0]["tag"] if tags else "N/A"
    newest_tag = tags[-1]["tag"] if tags else "N/A"

    lines = [
        "# 📦 Oh-My-Pi: 7-Day Release Activity & Module Breakdown",
        "",
        f"This document tracks releases of [`can1357/oh-my-pi`](https://github.com/can1357/oh-my-pi) published over the last {days} days ({start_date} – {end_date}), moving chronologically from the oldest release (**{oldest_tag}**) to the newest release (**{newest_tag}**). It focuses specifically on **Breaking Changes**, **Added** features, and **Changed** behavior per module.",
        "",
        "---",
        "",
    ]

    # Executive Summary section: use existing distilled summary if present, else prompt to add one
    if existing_summary:
        lines.append(existing_summary)
    else:
        lines.extend([
            "## 🌐 Executive Summary",
            "",
            "*(Summary to be distilled after running this script. Read the detailed changelog below and synthesize key highlights here.)*",
        ])

    lines.extend([
        "",
        "---",
        "",
        "## 📅 Release-by-Release Detailed Changelog",
        "",
    ])

    cat_order = ["Breaking Changes", "Added", "Changed", "Fixed", "Removed"]

    for item in tags:
        ver = item["version"]
        tag = item["tag"]
        date_str = item["date"]
        pkgs = data_by_version.get(ver, {})

        lines.append(f"### 🚀 Release `{tag}` ({date_str})")
        lines.append("")

        if not pkgs:
            lines.append("*Maintenance release / CI tag stabilization.*")
            lines.append("")
            continue

        for pkg_name, cats in sorted(pkgs.items()):
            has_entries = any(cat in cats and len(cats[cat]) > 0 for cat in cat_order)
            if not has_entries:
                continue

            lines.append(f"#### Module: `@oh-my-pi/{pkg_name}`")
            lines.append("")

            for cat in cat_order:
                if cat in cats and cats[cat]:
                    lines.append(f"##### **{cat}**")
                    for bullet in cats[cat]:
                        lines.append(f"- {bullet}")
                    lines.append("")

        lines.append("---")
        lines.append("")

    # Instruction Guide
    lines.extend([
        "## 📋 Instruction Guide: Recreating this Analysis",
        "",
        "### Automated Reproduction",
        "1. **Run the Automated Extraction Script**:",
        "   ```bash",
        "   python scripts/update-oh-my-pi-status.py --days 7 --write",
        "   ```",
        "2. **Add / Update the Executive Summary**:",
        "   - After script generation, read through the newly generated changelog entries below.",
        "   - Synthesize and distill the key cross-cutting themes (e.g. major breaking changes, native module optimizations, UI/TUI revamps, new settings/commands) and add/update them under `## 🌐 Executive Summary`.",
        "",
        "### Manual Step-by-Step Procedure",
        "1. **Fetch Upstream Tags**:",
        "   ```bash",
        "   git -C oh-my-pi-git-tag/src/oh-my-pi fetch origin --tags",
        "   # Query tags from the last 7 days sorted chronologically (oldest to newest)",
        "   git -C oh-my-pi-git-tag/src/oh-my-pi tag -l --sort=creatordate --format='%(creatordate:short) %(refname:short)'",
        "   ```",
        "2. **Inspect Monorepo Package Changelogs**:",
        "   `can1357/oh-my-pi` maintains modular changelogs under `packages/*/CHANGELOG.md`. For each target release tag, inspect all package changelogs for the matching `## [X.Y.Z]` headings:",
        "   ```bash",
        "   for ch in oh-my-pi-git-tag/src/oh-my-pi/packages/*/CHANGELOG.md; do",
        "       echo \"=== $ch ===\"",
        "       sed -n '/## \\[17.3.0\\]/,/## \\[/p' \"$ch\"",
        "   done",
        "   ```",
        "3. **Filter and Group by Category**:",
        "   - Prioritize **`Breaking Changes`**, **`Added`**, and **`Changed`** under each `@oh-my-pi/<package>` module.",
        "   - Include relevant **`Fixed`** and **`Removed`** sections to capture behavioral adjustments and deprecations.",
        "4. **Format Markdown & Distill Summary**:",
        "   - Present releases in chronological order (`v17.3.0` → `v17.4.0`).",
        "   - Read the distilled content and write an Executive Summary highlighting the top cross-cutting changes.",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Update oh-my-pi release status report.")
    parser.add_argument("--days", type=int, default=7, help="Number of rolling days to inspect (default: 7)")
    parser.add_argument("--write", "-w", action="store_true", help="Write directly to research/oh-my-pi-status.md")
    args = parser.parse_args()

    repo_dir = ensure_repo_sources()
    tags = get_tags_in_window(repo_dir, args.days)

    if not tags:
        print(f"No release tags found in the last {args.days} days.")
        return

    start_date = (datetime.date.today() - datetime.timedelta(days=args.days)).strftime("%B %d, %Y")
    end_date = datetime.date.today().strftime("%B %d, %Y")

    print(f"Found {len(tags)} releases in the last {args.days} days ({start_date} – {end_date}):")
    for t in tags:
        print(f"  - {t['tag']} ({t['date']})")

    target_versions = [t["version"] for t in tags]
    data_by_version = parse_package_changelogs(repo_dir, target_versions)

    output_file = "research/oh-my-pi-status.md"
    existing_summary = extract_existing_summary(output_file)

    md_content = generate_markdown(tags, data_by_version, start_date, end_date, args.days, existing_summary)

    if args.write:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"\nSuccessfully wrote updated report to {output_file}!")
    else:
        print("\n" + "=" * 50)
        print("Generated Markdown Output Preview:")
        print("=" * 50)
        print(md_content[:1500] + "\n\n... [truncated] ...")


if __name__ == "__main__":
    main()
