"""Shared non-destructive git peek helpers for AUR package status scripts.

Resolves and inspects existing makepkg sources (bare mirrors and patched src/
trees) without running updpkgsums, makepkg -Co, or mutating any working tree.
"""

import os
import re
import subprocess
from dataclasses import dataclass
from typing import List, Optional


class MissingMakepkgSourceError(RuntimeError):
    """Raised in strict mode when a git+ PKGBUILD has no local makepkg source."""


@dataclass(frozen=True)
class PeekResult:
    """Resolved git repository location and ref to inspect."""

    repo_dir: str
    ref: str
    source_kind: str
    warning: Optional[str] = None


def run_cmd(cmd: List[str], cwd: Optional[str] = None) -> str:
    """Run a command and return stripped stdout, or empty string on failure."""
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
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def run_cmd_ok(cmd: List[str], cwd: Optional[str] = None) -> bool:
    """Run a command and return True iff it exits with status 0."""
    try:
        res = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return res.returncode == 0
    except FileNotFoundError:
        return False


def _run_fetch(cmd: List[str], label: str) -> bool:
    """Run a git fetch command and warn on stderr if it fails."""
    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if res.returncode != 0:
            err_lines = [line.strip() for line in res.stderr.splitlines() if line.strip()]
            detail = err_lines[-1] if err_lines else f"exit code {res.returncode}"
            print(f"  [warn] git fetch failed for {label}: {detail}")
            return False
        return True
    except FileNotFoundError:
        return False


def get_makepkg_srcdest() -> Optional[str]:
    """Resolve SRCDEST from environment or makepkg.conf files, if configured."""
    env_srcdest = os.environ.get("SRCDEST", "").strip()
    if env_srcdest:
        return os.path.expanduser(env_srcdest)

    conf_paths = [
        "/etc/makepkg.conf",
        os.path.expanduser("~/.config/pacman/makepkg.conf"),
        os.path.expanduser("~/.makepkg.conf"),
    ]
    srcdest: Optional[str] = None
    pattern = re.compile(r"^\s*SRCDEST\s*=\s*(.+?)\s*$")

    for conf in conf_paths:
        if not os.path.isfile(conf):
            continue
        try:
            with open(conf, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#"):
                        continue
                    match = pattern.match(stripped)
                    if match:
                        val = match.group(1).strip().strip("\"'")
                        if val:
                            srcdest = os.path.expanduser(os.path.expandvars(val))
        except OSError:
            continue

    return srcdest


def _has_broken_alternates(repo_dir: str) -> bool:
    """Return True if the repo declares any missing git alternates object dir."""
    git_dir = run_cmd(["git", "-C", repo_dir, "rev-parse", "--git-dir"])
    if not git_dir:
        return True
    if not os.path.isabs(git_dir):
        git_dir = os.path.join(repo_dir, git_dir)

    alt_file = os.path.join(git_dir, "objects", "info", "alternates")
    if not os.path.isfile(alt_file):
        return False

    try:
        with open(alt_file, "r", encoding="utf-8") as f:
            for line in f:
                entry = line.strip()
                if not entry or entry.startswith("#"):
                    continue
                alt_path = entry if os.path.isabs(entry) else os.path.join(git_dir, "objects", entry)
                if not os.path.isdir(alt_path):
                    return True
    except OSError:
        return True
    return False


def is_git_repo(path: str) -> bool:
    """Return True if path is a readable git repository with healthy objects."""
    if not path or not os.path.isdir(path):
        return False
    if _has_broken_alternates(path):
        return False
    return run_cmd_ok(["git", "-C", path, "cat-file", "-e", "HEAD^{commit}"])


def is_bare_git_repo(path: str) -> bool:
    """Return True if path is a valid bare git repository with healthy objects."""
    if not path or not os.path.isdir(path):
        return False
    if run_cmd(["git", "-C", path, "rev-parse", "--is-bare-repository"]) != "true":
        return False
    return not _has_broken_alternates(path)


def _resolve_existing_ref(repo_dir: str, candidates: List[str]) -> str:
    """Return the first ref from candidates that resolves to a commit, else HEAD."""
    for cand in candidates:
        if cand and run_cmd_ok(["git", "-C", repo_dir, "rev-parse", "--verify", f"{cand}^{{commit}}"]):
            return cand
    return "HEAD"


def _ensure_blobless_scratch(
    name: str,
    target_url: str,
    branch: str,
    scratch_root: str,
    fetch: bool,
) -> PeekResult:
    """Maintain a lightweight blobless bare clone under scratch/<name>.git."""
    os.makedirs(scratch_root, exist_ok=True)
    scratch_bare = os.path.join(scratch_root, f"{name}.git")

    if is_bare_git_repo(scratch_bare):
        current_remote = run_cmd(["git", "-C", scratch_bare, "remote", "get-url", "origin"])
        if current_remote and current_remote.rstrip("/") not in (
            target_url.rstrip("/"),
            target_url[:-4].rstrip("/"),
        ):
            run_cmd(["git", "-C", scratch_bare, "remote", "set-url", "origin", target_url])
    elif fetch:
        print(f"Creating blobless bare peek cache for {name} in {scratch_bare}...")
        run_cmd(
            [
                "git",
                "clone",
                "--bare",
                "--filter=blob:none",
                target_url,
                scratch_bare,
            ]
        )

    if fetch and is_bare_git_repo(scratch_bare):
        _run_fetch(
            [
                "git",
                "-C",
                scratch_bare,
                "fetch",
                "--no-recurse-submodules",
                "--filter=blob:none",
                "origin",
                f"+refs/heads/{branch}:refs/heads/{branch}",
                "+refs/tags/*:refs/tags/*",
            ],
            name,
        )

    ref = _resolve_existing_ref(scratch_bare, [f"refs/heads/{branch}", "HEAD"])
    return PeekResult(
        repo_dir=scratch_bare,
        ref=ref,
        source_kind="scratch-blobless-bare",
    )


def resolve_and_peek_repo(
    *,
    name: str,
    github: str,
    branch: str = "main",
    pkg_dir: str = "",
    src_name: str = "",
    repo_type: str = "git",
    scratch_root: str = "scratch",
    fetch: bool = True,
    strict_pkgbuild: bool = False,
) -> PeekResult:
    """Resolve the best git repo to inspect without mutating any working tree.

    For git+ PKGBUILDs:
      1. Reuse makepkg's bare mirror ($SRCDEST/<src_name> or <pkg_dir>/<src_name>).
      2. Else peek via <pkg_dir>/src/<src_name> if its git object store is healthy
         (not broken by a deleted bare mirror's alternates), using an isolated ref
         (refs/remotes/upstream-peek/<branch>), never touching HEAD or patches.
      3. Else abort (if strict_pkgbuild=True) or fall back to a lightweight
         blobless bare cache in scratch/<name>.git with a warning.

    For tarball/release repos (no git source in PKGBUILD):
      Use a lightweight blobless bare cache in scratch/<name>.git.
    """
    target_url = f"https://github.com/{github}.git"
    effective_src_name = src_name or name
    has_pkgbuild = bool(pkg_dir and os.path.isfile(os.path.join(pkg_dir, "PKGBUILD")))

    if repo_type == "git" and has_pkgbuild:
        srcdest = get_makepkg_srcdest()
        bare_candidates: List[str] = []
        if srcdest:
            bare_candidates.append(os.path.join(srcdest, effective_src_name))
        bare_candidates.append(os.path.join(pkg_dir, effective_src_name))

        for bare_path in bare_candidates:
            if is_bare_git_repo(bare_path):
                if fetch:
                    _run_fetch(
                        [
                            "git",
                            "-C",
                            bare_path,
                            "fetch",
                            "--no-recurse-submodules",
                            "origin",
                            f"+refs/heads/{branch}:refs/heads/{branch}",
                            "+refs/tags/*:refs/tags/*",
                        ],
                        name,
                    )
                ref = _resolve_existing_ref(bare_path, [f"refs/heads/{branch}", "HEAD"])
                return PeekResult(
                    repo_dir=bare_path,
                    ref=ref,
                    source_kind="makepkg-bare",
                )

        src_path = os.path.join(pkg_dir, "src", effective_src_name)
        src_broken_alt = os.path.isdir(src_path) and _has_broken_alternates(src_path)
        if not src_broken_alt and is_git_repo(src_path):
            peek_ref = f"refs/remotes/upstream-peek/{branch}"
            if fetch:
                _run_fetch(
                    [
                        "git",
                        "-C",
                        src_path,
                        "fetch",
                        "--no-recurse-submodules",
                        target_url,
                        f"+refs/heads/{branch}:{peek_ref}",
                        "+refs/tags/*:refs/tags/*",
                    ],
                    name,
                )
            ref = _resolve_existing_ref(
                src_path,
                [peek_ref, f"refs/remotes/origin/{branch}", "HEAD"],
            )
            return PeekResult(
                repo_dir=src_path,
                ref=ref,
                source_kind="makepkg-src-peek",
            )

        if src_broken_alt:
            msg = (
                f"{src_path} has a broken git alternates pointer (its makepkg bare mirror was deleted). "
                f"Run 'cd {pkg_dir} && updpkgsums && makepkg -Co' when ready to restore local sources."
            )
        else:
            msg = (
                f"No makepkg source found for {pkg_dir} (checked bare mirror and src/{effective_src_name}). "
                f"Run 'cd {pkg_dir} && updpkgsums && makepkg -Co' when ready to populate local sources."
            )
        if strict_pkgbuild:
            raise MissingMakepkgSourceError(msg)

        print(f"[note] {msg} Falling back to blobless peek cache.")
        result = _ensure_blobless_scratch(name, target_url, branch, scratch_root, fetch)
        return PeekResult(
            repo_dir=result.repo_dir,
            ref=result.ref,
            source_kind=result.source_kind,
            warning=msg,
        )

    return _ensure_blobless_scratch(name, target_url, branch, scratch_root, fetch)


def list_tree_subdirs(repo_dir: str, ref: str, path: str) -> List[str]:
    """List immediate subdirectory paths under `path` at git `ref`."""
    prefix = path.rstrip("/") + "/"
    output = run_cmd(["git", "-C", repo_dir, "ls-tree", "-d", "--name-only", ref, prefix])
    return [line.strip() for line in output.splitlines() if line.strip()]


def read_blob(repo_dir: str, ref: str, path: str) -> Optional[str]:
    """Read a UTF-8 file directly from the git object store at `ref:path`."""
    try:
        res = subprocess.run(
            ["git", "-C", repo_dir, "show", f"{ref}:{path}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return res.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
