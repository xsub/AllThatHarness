from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

STATE_PREFIX = ".claude/state/"
GENERATED_DIR_PARTS = ("/__pycache__/", "/.pytest_cache/")
GENERATED_SUFFIXES = (".pyc", ".pyo")


def git(root: Path, args: list[str]) -> bytes:
    try:
        return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL)
    except Exception:
        return b""


def current_head(root: Path | None = None) -> str:
    root = root or Path.cwd()
    return git(root, ["rev-parse", "HEAD"]).decode("utf-8", "replace").strip() or "nogit"


def ignored_generated_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    wrapped = f"/{normalized}"
    return (
        normalized.startswith(STATE_PREFIX)
        or any(part in wrapped for part in GENERATED_DIR_PARTS)
        or normalized.endswith(GENERATED_SUFFIXES)
        or normalized == ".DS_Store"
        or normalized.endswith("/.DS_Store")
    )


def _untracked_paths(root: Path) -> list[str]:
    raw = git(root, ["ls-files", "--others", "--exclude-standard"]).decode("utf-8", "replace")
    return sorted(path for path in raw.splitlines() if not ignored_generated_path(path))


def diff_material(root: Path | None = None) -> bytes:
    root = root or Path.cwd()
    material = bytearray()

    unstaged = git(root, ["diff", "--binary", "--", ".", ":(exclude).claude/state"])
    if unstaged:
        material.extend(b"UNSTAGED\0")
        material.extend(unstaged)
        material.extend(b"\0")

    staged = git(root, ["diff", "--cached", "--binary", "--", ".", ":(exclude).claude/state"])
    if staged:
        material.extend(b"STAGED\0")
        material.extend(staged)
        material.extend(b"\0")

    for rel in _untracked_paths(root):
        path = root / rel
        if not path.is_file():
            continue
        material.extend(b"UNTRACKED\0")
        material.extend(rel.encode("utf-8", "surrogateescape"))
        material.extend(b"\0")
        try:
            material.extend(path.read_bytes())
        except OSError:
            pass
        material.extend(b"\0")

    return bytes(material)


def current_diff_hash(root: Path | None = None) -> str:
    return hashlib.sha256(diff_material(root)).hexdigest()


def has_material_changes(root: Path | None = None) -> bool:
    return bool(diff_material(root))
