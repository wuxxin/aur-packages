#!/usr/bin/env python
"""update-activity.py

A script to automate gathering statistics and recent git history for AUR packages.
This script checks local pacman installations, fetches upstream repository
updates, queries GitHub/PyPI metrics, compiles activity tables, and can optionally
write them directly to research/weekly-devel-activity.md.
"""

import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from typing import Any, Dict, List, Optional

# Define the repositories to track
TRACKED_REPOS: List[Dict[str, Any]] = [
    # 1. Real git repos
    {
        "name": "amux-git",
        "display_name": "amux-git",
        "github": "mixpeek/amux",
        "pkg": "amux-git",
        "branch": "main",
        "repo_type": "git",
        "pkg_dir": "amux-git",
        "src_name": "amux",
        "default_ref": "29d3c70",
    },
    {
        "name": "aoe-git-tag",
        "display_name": "aoe-git-tag",
        "github": "agent-of-empires/agent-of-empires",
        "pkg": "aoe-git-tag",
        "branch": "main",
        "repo_type": "git",
        "pkg_dir": "aoe-git-tag",
        "src_name": "agent-of-empires",
        "default_ref": "9b0d691",
    },
    {
        "name": "llama.cpp",
        "display_name": "llama.cpp",
        "parent_pkg": "libggml-git-hip",
        "github": "ggml-org/llama.cpp",
        "pkgs": ["libggml-git-hip", "llama.cpp-git-ggml-hip"],
        "branch": "master",
        "repo_type": "git",
        "pkg_dir": "libggml-git-hip",
        "src_name": "llama.cpp",
        "version_cmd": ["llama-cli", "--version"],
        "default_ref": "70aff25",
    },
    {
        "name": "whisper.cpp",
        "display_name": "whisper.cpp",
        "parent_pkg": "libggml-git-hip",
        "github": "ggerganov/whisper.cpp",
        "pkg": "whisper.cpp-git-ggml-hip",
        "branch": "master",
        "repo_type": "git",
        "pkg_dir": "libggml-git-hip",
        "src_name": "whisper.cpp",
        "version_cmd": ["whisper-cli", "--version"],
        "default_ref": "371b5a7",
    },
    {
        "name": "llama-cpp-python",
        "display_name": "llama-cpp-python",
        "parent_pkg": "libggml-git-hip",
        "github": "abetlen/llama-cpp-python",
        "pkg": "python-llama-cpp-git-ggml-hip",
        "branch": "main",
        "repo_type": "git",
        "pkg_dir": "libggml-git-hip",
        "src_name": "llama-cpp-python",
        "default_ref": "3691546",
    },
    {
        "name": "stable-diffusion.cpp",
        "display_name": "stable-diffusion.cpp",
        "parent_pkg": "libggml-git-hip",
        "github": "leejet/stable-diffusion.cpp",
        "pkg": "stable-diffusion.cpp-git-ggml-hip",
        "branch": "master",
        "repo_type": "git",
        "pkg_dir": "libggml-git-hip",
        "src_name": "stable-diffusion.cpp",
        "version_cmd": ["sd-cli", "--version"],
        "default_ref": "97d2990",
    },
    {
        "name": "qwen3-tts.cpp",
        "display_name": "qwen3-tts.cpp",
        "parent_pkg": "libggml-git-hip",
        "github": "khimaros/qwen3-tts.cpp",
        "pkg": "qwen3-tts.cpp-git-ggml-hip",
        "branch": "main",
        "repo_type": "git",
        "pkg_dir": "libggml-git-hip",
        "src_name": "qwen3-tts.cpp",
        "version_cmd": ["qwen3-tts-cli", "--version"],
        "default_ref": "0c8b2ba",
    },
    {
        "name": "parakeet.cpp",
        "display_name": "parakeet.cpp",
        "parent_pkg": "libggml-git-hip",
        "github": "mudler/parakeet.cpp",
        "pkg": "parakeet.cpp-git-ggml-hip",
        "branch": "main",
        "repo_type": "git",
        "pkg_dir": "libggml-git-hip",
        "src_name": "parakeet.cpp",
        "default_ref": "e75de9b",
    },
    {
        "name": "oh-my-pi",
        "display_name": "oh-my-pi-git-tag",
        "github": "can1357/oh-my-pi",
        "pkg": "oh-my-pi-git-tag",
        "branch": "main",
        "repo_type": "git",
        "pkg_dir": "oh-my-pi-git-tag",
        "src_name": "oh-my-pi",
        "default_ref": "45e12e5",
    },
    {
        "name": "pocket-tts.cpp",
        "display_name": "pocket-tts.cpp-git",
        "github": "VolgaGerm/PocketTTS.cpp",
        "pkg": "pocket-tts.cpp-git",
        "branch": "master",
        "repo_type": "git",
        "pkg_dir": "pocket-tts.cpp-git",
        "src_name": "pocket-tts-cpp",
        "default_ref": "e801e7d",
    },
    {
        "name": "python-bitsandbytes-rocm",
        "display_name": "python-bitsandbytes-rocm-git",
        "github": "bitsandbytes-foundation/bitsandbytes",
        "pkg": "python-bitsandbytes-rocm-git",
        "branch": "main",
        "repo_type": "git",
        "pkg_dir": "python-bitsandbytes-rocm-git",
        "src_name": "python-bitsandbytes-rocm-git",
        "default_ref": "2b6cfb79",
    },
    {
        "name": "python-gptqmodel-rocm",
        "display_name": "python-gptqmodel-rocm-git",
        "github": "ModelCloud/GPTQModel",
        "pkg": "python-gptqmodel-rocm-git",
        "branch": "main",
        "repo_type": "git",
        "pkg_dir": "python-gptqmodel-rocm-git",
        "src_name": "python-gptqmodel-rocm-git",
        "default_ref": "7df3d1e83",
    },
    {
        "name": "signal-cli-rest-api",
        "display_name": "signal-cli-rest-api-git",
        "github": "bbernhard/signal-cli-rest-api",
        "pkg": "signal-cli-rest-api-git",
        "branch": "master",
        "repo_type": "git",
        "pkg_dir": "signal-cli-rest-api-git",
        "src_name": "signal-cli-rest-api-git",
        "default_ref": "fe9df01",
    },
    {
        "name": "vllm.cpp",
        "display_name": "vllm.cpp-git-hip",
        "github": "mudler/vllm.cpp",
        "pkg": "vllm.cpp-git-hip",
        "branch": "main",
        "repo_type": "git",
        "pkg_dir": "vllm.cpp-git-hip",
        "src_name": "vllm.cpp",
        "default_ref": "65d6cda",
    },
    # 2. From git download tar.gz repos
    {
        "name": "python-optimum-amd",
        "display_name": "python-optimum-amd",
        "github": "huggingface/optimum-amd",
        "pkg": "python-optimum-amd",
        "branch": "main",
        "repo_type": "tarball",
        "pkg_dir": "python-optimum-amd",
        "default_ref": "f36a96b",
    },
    {
        "name": "smg",
        "display_name": "smg",
        "github": "lightseekorg/smg",
        "pkgs": ["smg", "python-smg"],
        "branch": "main",
        "repo_type": "tarball",
        "pkg_dir": "smg",
        "default_ref": "v1.8.0",
    },
    {
        "name": "tei-rocm",
        "display_name": "tei-rocm",
        "github": "huggingface/text-embeddings-inference",
        "pkg": "tei-rocm",
        "branch": "main",
        "repo_type": "tarball",
        "pkg_dir": "tei-rocm",
        "default_ref": "v1.9.3",
    },
    # 3. Repos that use releases
    {
        "name": "python-optimum-rocm",
        "display_name": "python-optimum-rocm",
        "github": "huggingface/optimum",
        "pkg": "python-optimum-rocm",
        "pypi_name": "optimum",
        "branch": "main",
        "repo_type": "release",
        "pkg_dir": "python-optimum-rocm",
        "default_ref": "v2.3.0",
    },
    {
        "name": "python-peft",
        "display_name": "python-peft",
        "github": "huggingface/peft",
        "pkg": "python-peft",
        "pypi_name": "peft",
        "branch": "main",
        "repo_type": "release",
        "pkg_dir": "python-peft",
        "default_ref": "v0.20.0",
    },
    {
        "name": "python-pocket-tts",
        "display_name": "python-pocket-tts",
        "github": "kyutai-labs/pocket-tts",
        "pkg": "python-pocket-tts",
        "pypi_name": "pocket-tts",
        "branch": "main",
        "repo_type": "release",
        "pkg_dir": "python-pocket-tts",
        "default_ref": "v2.1.0",
    },
    {
        "name": "python-infinity-emb",
        "display_name": "python-infinity-emb",
        "github": "michaelfeil/infinity",
        "pkg": "python-infinity-emb",
        "pypi_name": "infinity_emb",
        "branch": "main",
        "repo_type": "release",
        "pkg_dir": "python-infinity-emb",
        "default_ref": "0.0.75",
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


def is_commit_in_repo(repo_dir: str, ref: str) -> bool:
    """Check whether a git ref/commit exists in the specified repository."""
    if not ref or not repo_dir or not os.path.exists(repo_dir):
        return False
    res = subprocess.run(
        ["git", "-C", repo_dir, "cat-file", "-e", f"{ref}^{{commit}}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return res.returncode == 0


def extract_ref_from_version_cmd(cmd: List[str], repo_dir: str) -> Optional[str]:
    """Run binary --version and extract matching commit hash for libggml packages."""
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        text = res.stdout + "\n" + res.stderr
        patterns = [
            r"commit\s+([0-9a-f]{7,})",
            r"\(([0-9a-f]{7,})\)",
            r"-([0-9a-f]{7,})\+?",
            r"version\s+([0-9a-f]{7,})",
        ]
        for pat in patterns:
            m = re.search(pat, text, re.I)
            if m:
                cand = m.group(1)
                if is_commit_in_repo(repo_dir, cand):
                    return cand[:7]
    except Exception:
        pass
    return None


def get_pkgbuild_version(pkg_dir: str) -> str:
    """Extract pkgver from PKGBUILD."""
    pkgbuild_path = os.path.join(pkg_dir, "PKGBUILD")
    if not os.path.exists(pkgbuild_path):
        return ""
    try:
        with open(pkgbuild_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("pkgver="):
                    return line.split("=", 1)[1].strip().strip("\"'")
    except Exception:
        pass
    return ""


def get_git_installed_ref(repo_cfg: Dict[str, Any], repo_dir: str) -> str:
    """Resolve the git ref of the currently installed package."""
    parent_pkg = repo_cfg.get("parent_pkg")
    default_ref = repo_cfg.get("default_ref", "")

    # For libggml packages: use binary --version if configured
    if parent_pkg == "libggml-git-hip" and repo_cfg.get("version_cmd"):
        cmd_ref = extract_ref_from_version_cmd(repo_cfg["version_cmd"], repo_dir)
        if cmd_ref:
            return cmd_ref

    pkgs = repo_cfg.get("pkgs") or (
        [repo_cfg.get("pkg")] if repo_cfg.get("pkg") else []
    )

    # Extract git suffix from pacman version and verify it exists in repo_dir
    for pkg in pkgs:
        if pkg:
            pkg_ver = run_cmd(["pacman", "-Q", pkg])
            if pkg_ver:
                ver_part = pkg_ver.split()[-1]
                match = re.search(r"\.g([0-9a-f]{7,})(-.*)?$", ver_part)
                if match:
                    commit_hash = match.group(1)
                    if is_commit_in_repo(repo_dir, commit_hash):
                        return commit_hash
                tag_match = re.match(r"^([0-9]+\.[0-9]+(\.[0-9]+)?)", ver_part)
                if tag_match:
                    ver_tag = tag_match.group(1)
                    if is_commit_in_repo(repo_dir, ver_tag):
                        return ver_tag
                    if is_commit_in_repo(repo_dir, f"v{ver_tag}"):
                        return f"v{ver_tag}"
    # Fallback to default_ref if in repo
    if default_ref and is_commit_in_repo(repo_dir, default_ref):
        return default_ref

    # Fallback to git repo HEAD if present
    if repo_dir and os.path.isdir(repo_dir):
        short_ref = run_cmd(["git", "-C", repo_dir, "rev-parse", "--short=7", "HEAD"])
        if short_ref:
            return short_ref

    return default_ref


def parse_cached_metrics_from_file(file_path: str) -> Dict[str, Dict[str, int]]:
    """Parse stars and forks from previous markdown report to prevent 0s on rate limits."""
    metrics: Dict[str, Dict[str, int]] = {}
    if not os.path.exists(file_path):
        return metrics
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("|") and "github.com/" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 6:
                        link_match = re.search(r"github\.com/([^/\)]+/[^/\)]+)", parts[2])
                        if link_match:
                            slug = link_match.group(1).rstrip(")")
                            try:
                                stars = int(parts[3].replace(",", ""))
                                forks = int(parts[4].replace(",", ""))
                                if stars > 0 or forks > 0:
                                    metrics[slug] = {"stars": stars, "forks": forks}
                            except ValueError:
                                pass
    except Exception:
        pass
    return metrics


def query_github_api(
    repo_slug: str, cached_metrics: Optional[Dict[str, Dict[str, int]]] = None
) -> Dict[str, Any]:
    """Query GitHub API for stargazers, forks counts, and latest release."""
    headers = {
        "User-Agent": "Mozilla/5.0 (AUR weekly report generator)",
        "Accept": "application/vnd.github+json",
    }
    gh_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if gh_token:
        headers["Authorization"] = f"Bearer {gh_token}"

    fallback_stars = 0
    fallback_forks = 0
    if cached_metrics and repo_slug in cached_metrics:
        fallback_stars = cached_metrics[repo_slug].get("stars", 0)
        fallback_forks = cached_metrics[repo_slug].get("forks", 0)

    res_data: Dict[str, Any] = {
        "stars": fallback_stars,
        "forks": fallback_forks,
        "latest_release": "",
    }

    url = f"https://api.github.com/repos/{repo_slug}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            res_data["stars"] = data.get("stargazers_count", fallback_stars)
            res_data["forks"] = data.get("forks_count", fallback_forks)
    except Exception:
        pass

    # Query latest release
    rel_url = f"https://api.github.com/repos/{repo_slug}/releases/latest"
    rel_req = urllib.request.Request(rel_url, headers=headers)
    try:
        with urllib.request.urlopen(rel_req, timeout=5) as rel_resp:
            rel_data = json.loads(rel_resp.read().decode("utf-8"))
            res_data["latest_release"] = rel_data.get("tag_name", "")
    except Exception:
        pass

    return res_data


def query_pypi_latest(pypi_name: str) -> str:
    """Query PyPI API for the latest package version."""
    if not pypi_name:
        return ""
    url = f"https://pypi.org/pypi/{pypi_name}/json"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (AUR weekly report generator)",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("info", {}).get("version", "")
    except Exception:
        return ""


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
                clean_tag = p[4:].strip()
                if clean_tag:
                    tags.append(clean_tag)
    return sorted(list(set(tags)))


def parse_version_tuple(v: str) -> List[int]:
    """Parse version string into a list of integers for robust comparison."""
    clean = v.lstrip("v").split("-")[0]
    nums = []
    for part in clean.split("."):
        m = re.match(r"^(\d+)", part)
        if m:
            nums.append(int(m.group(1)))
        else:
            nums.append(0)
    return nums

def sync_repository(repo: Dict[str, Any]) -> str:
    """Ensure repository sources are up-to-date and return the inspectable directory."""
    repo_type = repo.get("repo_type", "git")
    github = repo["github"]
    name = repo["name"]
    branch = repo.get("branch", "main")
    pkg_dir = repo.get("pkg_dir", "")
    src_name = repo.get("src_name", name)
    target_url = f"https://github.com/{github}.git"

    if repo_type == "git" and pkg_dir:
        # Check standard PKGBUILD source locations
        src_path = os.path.join(pkg_dir, "src", src_name)
        bare_path = os.path.join(pkg_dir, src_name)

        # Check if src_path exists and is healthy
        src_valid = (
            os.path.exists(src_path)
            and run_cmd(["git", "-C", src_path, "rev-parse", "HEAD"]) != ""
        )
        bare_valid = (
            os.path.exists(bare_path)
            and run_cmd(["git", "-C", bare_path, "rev-parse", "HEAD"]) != ""
        )

        if not src_valid and not bare_valid:
            print(f"Updating PKGBUILD sources for {pkg_dir} via makepkg...")
            if os.path.exists(src_path) and not src_valid:
                shutil.rmtree(src_path, ignore_errors=True)
            run_cmd(["makepkg", "--nobuild", "-od"], cwd=pkg_dir)
            src_valid = (
                os.path.exists(src_path)
                and run_cmd(["git", "-C", src_path, "rev-parse", "HEAD"]) != ""
            )
            bare_valid = (
                os.path.exists(bare_path)
                and run_cmd(["git", "-C", bare_path, "rev-parse", "HEAD"]) != ""
            )

        # Ensure bare repository is always updated from upstream
        if bare_valid:
            run_cmd(
                [
                    "git",
                    "-C",
                    bare_path,
                    "fetch",
                    "origin",
                    "+refs/heads/*:refs/heads/*",
                    "+refs/tags/*:refs/tags/*",
                ]
            )

        # Inspect working tree if present, else bare repository
        if src_valid:
            run_cmd(
                [
                    "git",
                    "-C",
                    src_path,
                    "fetch",
                    "origin",
                    "+refs/heads/*:refs/heads/*",
                    "+refs/tags/*:refs/tags/*",
                ]
            )
            run_cmd(["git", "-C", src_path, "checkout", branch])
            run_cmd(["git", "-C", src_path, "reset", "--hard", f"origin/{branch}"])
            return src_path
        elif bare_valid:
            return bare_path
    # Fallback / tarball / release repos: maintain in scratch/<name>
    os.makedirs("scratch", exist_ok=True)
    scratch_dir = os.path.join("scratch", name)

    if os.path.exists(scratch_dir):
        current_remote = run_cmd(["git", "-C", scratch_dir, "remote", "get-url", "origin"])
        if current_remote and current_remote != target_url and current_remote != target_url[:-4]:
            print(f"Remote mismatch for {name}. Re-cloning into scratch...")
            shutil.rmtree(scratch_dir)

    if not os.path.exists(scratch_dir):
        print(f"Cloning {name} into {scratch_dir}...")
        run_cmd(["git", "clone", "--depth", "2000", target_url, scratch_dir])

    run_cmd(
        [
            "git",
            "-C",
            scratch_dir,
            "fetch",
            "origin",
            "+refs/heads/*:refs/heads/*",
            "+refs/tags/*:refs/tags/*",
        ]
    )
    run_cmd(["git", "-C", scratch_dir, "checkout", branch])
    run_cmd(["git", "-C", scratch_dir, "reset", "--hard", f"origin/{branch}"])
    return scratch_dir


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
        since_val = stats.get("since_commits", "0")
        if since_val != "-":
            pkg_phrase = f" **{since_val} commits since installed {stats['installed_ver']}{ref_suffix}.**"

    return f"* **Status**: {status} ({commits} commits, {tag_phrase}).{pkg_phrase}"


def make_recent_focus_block(stats: Dict[str, Any], repo_dir: str) -> str:
    """Fetch and format the Recent Focus block using git log or release comparison."""
    if stats.get("repo_type") == "release":
        latest_rel = stats.get("latest_release") or stats.get("pypi_latest") or "N/A"
        pkgver = stats.get("pkgbuild_ver", "N/A")
        inst_ver = stats.get("installed_ver", "not installed")

        status_flag = "✅ Up to date"
        if latest_rel and latest_rel != "N/A":
            clean_rel = latest_rel.lstrip("v")
            rel_tuple = parse_version_tuple(latest_rel)
            pkg_tuple = parse_version_tuple(pkgver) if pkgver and pkgver != "N/A" else []
            if rel_tuple and pkg_tuple and rel_tuple > pkg_tuple:
                status_flag = f"⚠️ **Newer release available: `{latest_rel}`**"
        lines = [
            "* **Release Status**:",
            f"  - {status_flag}",
            f"  - Upstream Latest: `{latest_rel}` | PKGBUILD: `{pkgver}` | Installed: `{inst_ver}`",
        ]
        return "\n".join(lines)

    installed_ref = stats.get("installed_ref")
    since_commits_str = stats.get("since_commits", "—")
    since_commits_int = int(since_commits_str) if since_commits_str.isdigit() else None
    installed_ver = stats.get("installed_ver")
    is_installed = installed_ver and installed_ver not in ("not installed", "—")

    if is_installed and installed_ref:
        if since_commits_int is not None and since_commits_int > 0:
            cmd = [
                "git",
                "-C",
                repo_dir,
                "log",
                "--no-merges",
                "--oneline",
                "-n",
                "15",
                f"{installed_ref}..HEAD",
            ]
        else:
            lines = [
                "* **Recent Focus**:",
                "  - Up to date with installed package (0 new commits).",
            ]
            return "\n".join(lines)
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


def compile_activity(write_to_file: bool = False) -> None:
    """Compile the weekly development activity report."""
    print("Starting development activity report update...")
    start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime(
        "%B %d, %Y"
    )
    end_date = datetime.date.today().strftime("%B %d, %Y")
    print(f"Reporting Period: {start_date} - {end_date}")

    file_path = "research/weekly-devel-activity.md"
    cached_metrics = parse_cached_metrics_from_file(file_path)

    results: List[Dict[str, Any]] = []

    for repo in TRACKED_REPOS:
        name = repo["name"]
        display_name = repo.get("display_name", name)
        github = repo["github"]
        branch = repo.get("branch", "main")
        pkg_dir = repo.get("pkg_dir", "")
        repo_type = repo.get("repo_type", "git")
        pypi_name = repo.get("pypi_name", "")

        print(f"\nProcessing {name} ({github}) [{repo_type}]...")
        repo_dir = sync_repository(repo)

        # Commits & Merges in last 7 days
        log_7d = run_cmd(
            [
                "git",
                "-C",
                repo_dir,
                "log",
                "--since=7 days ago",
                "--no-merges",
                "--oneline",
            ]
        )
        commits = len(log_7d.splitlines()) if log_7d else 0

        log_merges = run_cmd(
            [
                "git",
                "-C",
                repo_dir,
                "log",
                "--since=7 days ago",
                "--merges",
                "--oneline",
            ]
        )
        merges = len(log_merges.splitlines()) if log_merges else 0

        last_commit = run_cmd(
            ["git", "-C", repo_dir, "log", "-1", "--format=%ad", "--date=short"]
        )

        # 4 weeks average
        log_28d = run_cmd(
            [
                "git",
                "-C",
                repo_dir,
                "log",
                "--since=28 days ago",
                "--no-merges",
                "--oneline",
            ]
        )
        commits_28 = len(log_28d.splitlines()) if log_28d else 0
        avg_commits = f"{commits_28 / 4:.1f}"

        # Tags in last 7 days
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
            installed_ref = get_git_installed_ref(repo, repo_dir)
            if installed_ref and repo_type != "release":
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

        pkgbuild_ver = get_pkgbuild_version(pkg_dir) if pkg_dir else ""

        # GitHub metrics & release info
        github_metrics = query_github_api(github, cached_metrics)
        pypi_latest = query_pypi_latest(pypi_name) if pypi_name else ""

        # Status determination
        status = "Stale"
        if commits > 50:
            status = "Highly Active"
        elif commits > 0:
            status = "Active"

        results.append(
            {
                "name": name,
                "display_name": display_name,
                "parent_pkg": repo.get("parent_pkg", ""),
                "github": github,
                "pkg": repo.get("pkg", ""),
                "pkgs": pkgs,
                "repo_type": repo_type,
                "repo_dir": repo_dir,
                "pkgbuild_ver": pkgbuild_ver,
                "stars": github_metrics["stars"],
                "forks": github_metrics["forks"],
                "latest_release": github_metrics.get("latest_release", ""),
                "pypi_latest": pypi_latest,
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

    # Format Table
    def format_row(r: Dict[str, Any]) -> str:
        if r.get("repo_type") == "release":
            newest_rel = r.get("latest_release") or r.get("pypi_latest")
            tags_str = f"`{newest_rel}`" if newest_rel else "—"
        else:
            tags_str = ", ".join(f"`{t}`" for t in r["tags"][:2]) if r["tags"] else "—"

        name_display = f"**{r['display_name']}**"
        if r.get("parent_pkg") == "libggml-git-hip":
            name_display = f"*└─ {r['name']}*"

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

    table_lines = [
        "| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |",
    ]

    for r in results:
        table_lines.append(format_row(r))

    table_str = "\n".join(table_lines)

    # Format Details Section
    details_blocks = []
    for r in results:
        parent_prefix = f"[{r['parent_pkg']}] " if r.get("parent_pkg") else ""
        header = f"### {parent_prefix}{r['display_name']} (`{r['github']}`)"
        status_line = make_status_line(r)
        focus_block = make_recent_focus_block(r, r["repo_dir"])
        details_blocks.append(f"{header}\n{status_line}\n{focus_block}")

    details_str = "\n\n".join(details_blocks)

    if write_to_file:
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found in the current directory.")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update date anchor
        date_pattern = re.compile(
            r"<!-- START_DATE -->.*?<!-- END_DATE -->", re.DOTALL
        )
        new_date_block = f"<!-- START_DATE -->\n**Last 7 Days Activity ({start_date} – {end_date})**\n<!-- END_DATE -->"
        if date_pattern.search(content):
            content = re.sub(date_pattern, lambda m: new_date_block, content)
        else:
            # Fallback legacy regex replacement
            header_pattern = r"(## 📅 Summary.*?\n\n)(\*\*[^\n]+\*\*)"
            content = re.sub(header_pattern, f"\\1{new_date_block}", content)

        # Update table anchor
        table_pattern = re.compile(
            r"<!-- START_TABLES -->.*?<!-- END_TABLES -->", re.DOTALL
        )
        new_table_block = f"<!-- START_TABLES -->\n{table_str}\n<!-- END_TABLES -->"
        content = re.sub(table_pattern, lambda m: new_table_block, content)

        # Update details anchor
        details_pattern = re.compile(
            r"<!-- START_DETAILS -->.*?<!-- END_DETAILS -->", re.DOTALL
        )
        new_details_block = f"<!-- START_DETAILS -->\n{details_str}\n<!-- END_DETAILS -->"
        if details_pattern.search(content):
            content = re.sub(details_pattern, lambda m: new_details_block, content)
        else:
            # Locate "## 🔍 Repository Focus & Developments Details" and replace until next section or end
            focus_sec_pattern = re.compile(
                r"(## 🔍 Repository Focus & Developments Details\n\n).*?(?=\n---|\Z)",
                re.DOTALL,
            )
            content = re.sub(
                focus_sec_pattern, f"\\1{new_details_block}\n", content
            )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\nSuccessfully wrote updated activity report to {file_path}!")

    else:
        print("\n" + "=" * 40)
        print("Unified Packages Table Output:")
        print("=" * 40)
        print(table_str)

        print("\n" + "=" * 40)
        print("Repository Focus & Development Details Output:")
        print("=" * 40)
        print(details_str)


if __name__ == "__main__":
    write_flag = "--write" in sys.argv or "-w" in sys.argv
    compile_activity(write_to_file=write_flag)
