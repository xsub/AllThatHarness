#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path.cwd()


def git(args: list[str]) -> bytes:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL)
    except Exception:
        return b""


def main() -> int:
    h = hashlib.sha256()
    for args in (["diff", "--binary", "--", ".", ":(exclude).claude/state"], ["diff", "--cached", "--binary", "--", ".", ":(exclude).claude/state"]):
        h.update(git(list(args)))
    untracked = git(["ls-files", "--others", "--exclude-standard"]).decode("utf-8", "replace").splitlines()
    for rel in sorted(p for p in untracked if not p.startswith(".claude/state/")):
        p = ROOT / rel
        if p.is_file():
            h.update(rel.encode())
            h.update(b"\0")
            try:
                h.update(p.read_bytes())
            except OSError:
                pass
    print(h.hexdigest())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
