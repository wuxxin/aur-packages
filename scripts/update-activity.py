#!/usr/bin/env python
"""update-activity.py

A script to automate gathering statistics and recent git history for AUR packages.
This script checks local pacman installations, fetches upstream repository
updates, queries GitHub metrics, compiles activity tables, and can optionally
write them directly to weekly-devel-activity.md.
"""

import datetime
import json
import os
import re
import subprocess
import sys
import urllib.request
from typing import Any, Dict, List, Optional

# Define the repositories to track
TRACKED_REPOS: List[Dict[str, Any]] = [
    {
        "name": "llama.cpp",
        "github": "ggml-org/llama.cpp",
        "pkg": "libggml-git-hip",
        "branch": "master",
        "src_path": "libggml-git-hip/src/llama.cpp",
        "category": "ai",
        "default_ref": "c576070",
    },
    {
        "name": "llama-cpp-python",
        "github": "abetlen/llama-cpp-python",
        "pkg": "python-llama-cpp-git-ggml-hip",
        "branch": "main",
        "src_path": "libggml-git-hip/src/llama-cpp-python",
        "category": "ai",
        "default_ref": "b11fe07",
    },
    {
        "name": "stable-diffusion.cpp",
        "github": "leejet/stable-diffusion.cpp",
        "pkg": "stable-diffusion.cpp-git-ggml-hip",
        "branch": "master",
        "src_path": "libggml-git-hip/src/stable-diffusion.cpp",
        "category": "ai",
        "default_ref": "7f0e728",
    },
    {
        "name": "whisper.cpp",
        "github": "ggerganov/whisper.cpp",
        "pkg": "whisper.cpp-git-ggml-hip",
        "branch": "master",
        "src_path": "libggml-git-hip/src/whisper.cpp",
        "category": "ai",
        "default_ref": "5ed76e9a",
    },
    {
        "name": "qwen3-tts.cpp",
        "github": "khimaros/qwen3-tts.cpp",
        "pkg": "qwen3-tts.cpp-git-ggml-hip",
        "branch": "main",
        "src_path": "libggml-git-hip/src/qwen3-tts.cpp",
        "category": "ai",
        "default_ref": "0c8b2ba",
    },
    {
        "name": "qwen3-tts-upstream",
        "github": "predict-woo/qwen3-tts.cpp",
        "pkg": "",
        "branch": "main",
        "src_path": "",
        "category": "ai",
        "default_ref": "",
    },
    {
        "name": "bitsandbytes",
        "github": "bitsandbytes-foundation/bitsandbytes",
        "pkg": "python-bitsandbytes-rocm-git",
        "branch": "main",
        "src_path": "python-bitsandbytes-rocm-git/src/bitsandbytes",
        "category": "ai",
        "default_ref": "435b8b3",
    },
    {
        "name": "vllm",
        "github": "vllm-project/vllm",
        "pkg": "python-vllm-rocm-git",
        "branch": "main",
        "src_path": "",
        "category": "ai",
        "default_ref": "6bdabba",
    },
    {
        "name": "vllm-omni",
        "github": "vllm-project/vllm-omni",
        "pkg": "python-vllm-omni-rocm-git",
        "branch": "main",
        "src_path": "",
        "category": "ai",
        "default_ref": "5dfdf58",
    },
    {
        "name": "pockettts.cpp",
        "github": "VolgaGerm/PocketTTS.cpp",
        "pkg": "pocket-tts.cpp-git",
        "branch": "master",
        "src_path": "pocket-tts.cpp-git/src/pockettts.cpp",
        "category": "ai",
        "default_ref": "e801e7d",
    },
    {
        "name": "pocket-tts",
        "github": "kyutai-labs/pocket-tts",
        "pkg": "python-pocket-tts",
        "branch": "main",
        "src_path": "",
        "category": "ai",
        "default_ref": "v2.1.0",
    },
    {
        "name": "ironclaw",
        "github": "nearai/ironclaw",
        "pkg": "ironclaw-git",
        "pkgs": ["ironclaw-git", "ironclaw-reborn-git"],
        "branch": "main",
        "src_path": "ironclaw-git/src/ironclaw",
        "src_paths": ["ironclaw-git/src/ironclaw", "ironclaw-reborn-git/src/ironclaw"],
        "category": "ai",
        "default_ref": "811763f",
    },
    {
        "name": "signal-cli-rest-api",
        "github": "bbernhard/signal-cli-rest-api",
        "pkg": "signal-cli-rest-api-git",
        "branch": "master",
        "src_path": "signal-cli-rest-api-git/src/signal-cli-rest-api",
        "category": "other",
        "default_ref": "a4f5855",
    },
]


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


def get_git_installed_ref(repo_cfg: Dict[str, Any]) -> str:
    """Resolve the git ref of the currently installed package."""
    src_paths = repo_cfg.get("src_paths") or (
        [repo_cfg.get("src_path")] if repo_cfg.get("src_path") else []
    )
    pkgs = repo_cfg.get("pkgs") or (
        [repo_cfg.get("pkg")] if repo_cfg.get("pkg") else []
    )
    default_ref = repo_cfg.get("default_ref", "")

    # 1. Check if git repo exists in package src directory
    for src_path in src_paths:
        if src_path and os.path.isdir(os.path.join(src_path, ".git")):
            short_ref = run_cmd(
                ["git", "-C", src_path, "rev-parse", "--short=7", "HEAD"]
            )
            if short_ref:
                return short_ref

    # 2. Extract git suffix from pacman version
    for pkg in pkgs:
        if pkg:
            pkg_ver = run_cmd(["pacman", "-Q", pkg])
            if pkg_ver:
                # Extract suffix after ".g" or "-g" followed by hex characters
                ver_part = pkg_ver.split()[-1]
                match = re.search(r"\.g([0-9a-f]{7,})(-.*)?$", ver_part)
                if match:
                    return match.group(1)

    return default_ref


def query_github_api(repo_slug: str) -> Dict[str, int]:
    """Query GitHub API for stargazers and forks counts."""
    url = f"https://api.github.com/repos/{repo_slug}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (AUR weekly report generator)",
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
            }
    except Exception:
        # Fallback to zeros if offline or rate-limited
        return {"stars": 0, "forks": 0}


def get_repo_tags(repo_dir: str) -> List[str]:
    """Find tags/releases in the last 7 days."""
    output = run_cmd(
        [
            "git",
            "-C",
            repo_dir,
            "log",
            "--tags",
            "--since=7 days ago",
            "--simplify-by-decoration",
            "--pretty=format:%d",
        ]
    )
    tags = []
    for line in output.split("\n"):
        line = line.strip(" ()")
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        for p in parts:
            if p.startswith("tag:"):
                tags.append(p[4:])
            elif not p.startswith("origin/") and p != "HEAD":
                tags.append(p)
    return sorted(list(set(tags)))


def make_status_line(stats: Dict[str, Any]) -> str:
    """Format the Status line for package breakdown."""
    commits = stats["commits"]
    status = stats["status"]

    tag_count = len(stats["tags"])
    tag_word = "tag/release" if tag_count == 1 else "tags/releases"
    tag_phrase = f"{tag_count} {tag_word} in the last week"

    pkg_phrase = ""
    if (
        stats.get("installed_ver")
        and stats["installed_ver"] != "not installed"
        and stats["installed_ver"] != "—"
    ):
        ref_suffix = (
            f" (ref `{stats['installed_ref']}`)" if stats["installed_ref"] else ""
        )
        pkg_phrase = f" **{stats['since_commits']} commits since installed {stats['installed_ver']}{ref_suffix}.**"

    return f"* **Status**: {status} ({commits} commits, {tag_phrase}).{pkg_phrase}"


def update_assistant_section_with_anchor(
    content: str, name: str, stats: Dict[str, Any]
) -> str:
    """Locate and update status lists for a package section in content using comment anchors."""
    anchor_name = name.upper().replace(".", "_").replace("-", "_")
    start_tag = f"<!-- START_BD_{anchor_name} -->"
    end_tag = f"<!-- END_BD_{anchor_name} -->"

    status_line = make_status_line(stats)
    new_body = f"{status_line}"

    pattern = re.compile(rf"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
    if not pattern.search(content):
        print(f"Warning: Comment anchor {start_tag} / {end_tag} not found in markdown.")
        return content

    new_block = f"{start_tag}\n{new_body}\n{end_tag}"
    return re.sub(pattern, lambda m: new_block, content)


def make_recent_focus_block(stats: Dict[str, Any], repo_dir: str) -> str:
    """Fetch and format the Recent Focus block using git log."""
    installed_ref = stats.get("installed_ref")
    since_commits_str = stats.get("since_commits", "—")
    since_commits_int = int(since_commits_str) if since_commits_str.isdigit() else None

    use_installed_range = False
    if (
        installed_ref
        and since_commits_int is not None
        and since_commits_int < stats.get("commits", 0)
    ):
        use_installed_range = True

    if use_installed_range:
        cmd = [
            "git",
            "-C",
            repo_dir,
            "log",
            "--no-merges",
            "--oneline",
            f"{installed_ref}..HEAD",
        ]
    else:
        cmd = [
            "git",
            "-C",
            repo_dir,
            "log",
            "--since=7 days ago",
            "--no-merges",
            "--oneline",
            "-n",
            "15",
        ]

    log_output = run_cmd(cmd)

    lines = ["* **Recent Focus**:"]
    if not log_output:
        lines.append("  - No new commits in this period.")
        return "\n".join(lines)

    for line in log_output.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            commit_hash, subject = parts[0], parts[1]
            subject = subject.replace("`", "'")
            lines.append(f"  - `{commit_hash}` {subject}")
        else:
            lines.append(f"  - {line}")

    return "\n".join(lines)


def update_focus_section_with_anchor(
    content: str, name: str, stats: Dict[str, Any]
) -> str:
    """Locate and update Recent Focus lists for a section in content using comment anchors."""
    anchor_name = name.upper().replace(".", "_").replace("-", "_")
    start_tag = f"<!-- START_RF_{anchor_name} -->"
    end_tag = f"<!-- END_RF_{anchor_name} -->"

    repo_dir = os.path.join("scratch", name)
    focus_block = make_recent_focus_block(stats, repo_dir)

    pattern = re.compile(rf"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
    if not pattern.search(content):
        print(
            f"Warning: Focus comment anchor {start_tag} / {end_tag} not found in markdown."
        )
        return content

    new_block = f"{start_tag}\n{focus_block}\n{end_tag}"
    return re.sub(pattern, lambda m: new_block, content)


def compile_activity(write_to_file: bool = False) -> None:
    """Compile the weekly development activity report."""
    print("Starting development activity report update...")
    start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime(
        "%B %d, %Y"
    )
    end_date = datetime.date.today().strftime("%B %d, %Y")
    print(f"Reporting Period: {start_date} - {end_date}")

    os.makedirs("scratch", exist_ok=True)

    results: List[Dict[str, Any]] = []

    for repo in TRACKED_REPOS:
        name = repo["name"]
        github = repo["github"]
        pkg = repo["pkg"]
        branch = repo["branch"]

        repo_dir = f"scratch/{name}"
        print(f"\nProcessing {name} ({github})...")

        # Clone if missing
        if not os.path.exists(repo_dir):
            print(f"Cloning {name}...")
            run_cmd(
                [
                    "git",
                    "clone",
                    "--depth",
                    "2000",
                    f"https://github.com/{github}.git",
                    repo_dir,
                ]
            )

        # Fetch and reset
        run_cmd(["git", "-C", repo_dir, "fetch", "origin"])
        run_cmd(["git", "-C", repo_dir, "checkout", branch])
        run_cmd(["git", "-C", repo_dir, "reset", "--hard", f"origin/{branch}"])

        # Commits & Merges in last 7 days
        commits = int(
            run_cmd(
                [
                    "git",
                    "-C",
                    repo_dir,
                    "log",
                    "--since=7 days ago",
                    "--no-merges",
                    "--oneline",
                ]
            ).count("\n")
            + 1
        )
        # Fix count if output is empty
        if not run_cmd(
            [
                "git",
                "-C",
                repo_dir,
                "log",
                "--since=7 days ago",
                "--no-merges",
                "--oneline",
            ]
        ):
            commits = 0

        merges = int(
            run_cmd(
                [
                    "git",
                    "-C",
                    repo_dir,
                    "log",
                    "--since=7 days ago",
                    "--merges",
                    "--oneline",
                ]
            ).count("\n")
            + 1
        )
        if not run_cmd(
            [
                "git",
                "-C",
                repo_dir,
                "log",
                "--since=7 days ago",
                "--merges",
                "--oneline",
            ]
        ):
            merges = 0

        last_commit = run_cmd(
            ["git", "-C", repo_dir, "log", "-1", "--format=%ad", "--date=short"]
        )

        # 4 weeks average
        commits_28 = int(
            run_cmd(
                [
                    "git",
                    "-C",
                    repo_dir,
                    "log",
                    "--since=28 days ago",
                    "--no-merges",
                    "--oneline",
                ]
            ).count("\n")
            + 1
        )
        if not run_cmd(
            [
                "git",
                "-C",
                repo_dir,
                "log",
                "--since=28 days ago",
                "--no-merges",
                "--oneline",
            ]
        ):
            commits_28 = 0
        avg_commits = f"{commits_28 / 4:.1f}"

        # Tags
        tags = get_repo_tags(repo_dir)

        # Pacman version & since installed
        installed_ver = "not installed"
        since_commits = "-"
        installed_ref = ""
        pkgs = repo.get("pkgs") or ([repo.get("pkg")] if repo.get("pkg") else [])
        pkg_ver_str = ""
        for p in pkgs:
            if p:
                pkg_ver_str = run_cmd(["pacman", "-Q", p])
                if pkg_ver_str:
                    break
        if pkg_ver_str:
            installed_ver = pkg_ver_str.split()[-1]
            installed_ref = get_git_installed_ref(repo)
            if installed_ref:
                # Calculate commits since installed ref
                log_since = run_cmd(
                    [
                        "git",
                        "-C",
                        repo_dir,
                        "log",
                        "--no-merges",
                        "--oneline",
                        f"{installed_ref}..HEAD",
                    ]
                )
                since_commits = (
                    str(len(log_since.strip().splitlines())) if log_since else "0"
                )

        # GitHub Stars & Forks
        github_metrics = query_github_api(github)

        # Status
        status = "Stale"
        if commits > 50:
            status = "Highly Active"
        elif commits > 0:
            status = "Active"

        results.append(
            {
                "name": name,
                "github": github,
                "pkg": pkg,
                "category": repo["category"],
                "stars": github_metrics["stars"],
                "forks": github_metrics["forks"],
                "branch": branch,
                "last_commit": last_commit,
                "commits": commits,
                "merges": merges,
                "tags": tags,
                "avg_commits": avg_commits,
                "installed_ver": installed_ver,
                "installed_ref": installed_ref,
                "since_commits": since_commits,
                "status": status,
            }
        )

    # Format output
    def format_row(r: Dict[str, Any]) -> str:
        tags_str = ", ".join(f"`{t}`" for t in r["tags"][:2]) if r["tags"] else "—"
        # Custom indentation for split packages
        name_display = f"**{r['name']}**"
        if r["name"] in [
            "llama-cpp-python",
            "stable-diffusion.cpp",
            "whisper.cpp",
            "qwen3-tts.cpp",
        ]:
            name_display = f"*└─ {r['name']}*"
        elif r["name"] == "qwen3-tts-upstream":
            name_display = "*   └─ [Fork Origin]*"

        installed_str = r["installed_ver"]
        if r["installed_ref"]:
            installed_str = f"`{r['installed_ver']}` (ref `{r['installed_ref']}`)"
        elif installed_str != "not installed":
            installed_str = f"`{installed_str}`"

        commits_str = f"**{r['commits']}**" if r["commits"] > 0 else "0"

        return (
            f"| {name_display} | [{r['github']}](https://github.com/{r['github']}) "
            f"| {r['stars']:,} | {r['forks']:,} | `{r['branch']}` | {r['last_commit']} "
            f"| {commits_str} | {r['merges']} | {len(r['tags'])} | {r['avg_commits']} "
            f"| {tags_str} | {installed_str} | {r['since_commits']} | **{r['status']}** |"
        )

    ai_table = [
        "### AI Backend & Inference Packages",
        "",
        "| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |",
    ]
    other_table = [
        "### Other Custom Packages",
        "",
        "| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |",
    ]

    for r in results:
        if r["category"] == "ai":
            ai_table.append(format_row(r))
        else:
            other_table.append(format_row(r))

    ai_table_str = "\n".join(ai_table)
    other_table_str = "\n".join(other_table)

    note_note = (
        "\n> [!NOTE]\n"
        "> `vllm`, `bitsandbytes`, `pocket-tts`, and most split sub-repositories of the `libggml-git-hip` "
        "package squash-merge PRs directly into their primary branch instead of creating merge commits, "
        'which is why the "Merges" column displays `0`.'
    )

    other_note = (
        "\n> [!NOTE]\n"
        "> `zeroclaw-git` (upstream: [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw)) "
        "is hosted and tracked separately under the `agents-shared` repository."
    )

    new_tables_block = f"{ai_table_str}\n{note_note}\n\n{other_table_str}\n{other_note}"

    if write_to_file:
        file_path = "weekly-devel-activity.md"
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found in the current directory.")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update date header
        header_pattern = r"(## 📅 Summary of Last 7 Days Activity \()[^\)]+(\))"
        new_header = f"\\1{start_date} – {end_date}\\2"
        content = re.sub(header_pattern, new_header, content)

        # Update tables
        start_tag = "<!-- START_TABLES -->"
        end_tag = "<!-- END_TABLES -->"
        table_pattern = re.compile(
            rf"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL
        )
        new_block = f"{start_tag}\n{new_tables_block}\n{end_tag}"
        content = re.sub(table_pattern, lambda m: new_block, content)

        # Update breakdown and focus sections
        for r in results:
            content = update_assistant_section_with_anchor(content, r["name"], r)
            content = update_focus_section_with_anchor(content, r["name"], r)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\nSuccessfully wrote updated activity report to {file_path}!")

    else:
        print("\n" + "=" * 40)
        print("AI Backend & Inference Table Output:")
        print("=" * 40)
        print(ai_table_str)

        print("\n" + "=" * 40)
        print("Other Custom Packages Table Output:")
        print("=" * 40)
        print(other_table_str)

    # Print raw logs to assist summary creation
    print("\n" + "=" * 40)
    print("Recent Upstream Commit Logs:")
    print("=" * 40)
    for r in results:
        inst_ref = r.get("installed_ref")
        since_commits_str = r.get("since_commits", "—")
        since_commits_int = (
            int(since_commits_str) if since_commits_str.isdigit() else None
        )

        use_installed_range = False
        if (
            inst_ref
            and since_commits_int is not None
            and since_commits_int < r["commits"]
        ):
            use_installed_range = True

        if use_installed_range:
            print(
                f"\n### {r['name']} ({r['github']}) - {since_commits_int} commits since installed {r['installed_ver']}"
            )
            if since_commits_int is not None and since_commits_int > 0:
                log = run_cmd(
                    [
                        "git",
                        "-C",
                        f"scratch/{r['name']}",
                        "log",
                        "--no-merges",
                        "--oneline",
                        f"{inst_ref}..HEAD",
                    ]
                )
                print(log)
        else:
            if r["commits"] == 0:
                continue
            print(
                f"\n### {r['name']} ({r['github']}) - {r['commits']} commits (Last 7 Days)"
            )
            log = run_cmd(
                [
                    "git",
                    "-C",
                    f"scratch/{r['name']}",
                    "log",
                    "--since=7 days ago",
                    "--no-merges",
                    "--oneline",
                    "-n",
                    "15",
                ]
            )
            print(log)


if __name__ == "__main__":
    write_flag = "--write" in sys.argv or "-w" in sys.argv
    compile_activity(write_to_file=write_flag)
