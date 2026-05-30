#!/usr/bin/env python3
"""Claude Code Stop hook: require a passing verification for the exact current diff."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
STATE = ROOT / ".claude" / "state"
LAST = STATE / "last-verification.json"


def git_ok() -> bool:
    try:
        subprocess.check_call(["git", "rev-parse", "--is-inside-work-tree"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def git(args: list[str]) -> bytes:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL)
    except Exception:
        return b""


def current_head() -> str:
    return git(["rev-parse", "HEAD"]).decode("utf-8", "replace").strip()


def diff_material() -> bytes:
    material = bytearray()
    material.extend(git(["diff", "--binary", "--", ".", ":(exclude).claude/state"]))
    material.extend(b"\n--STAGED--\n")
    material.extend(git(["diff", "--cached", "--binary", "--", ".", ":(exclude).claude/state"]))
    material.extend(b"\n--UNTRACKED--\n")
    untracked = git(["ls-files", "--others", "--exclude-standard"]).decode("utf-8", "replace").splitlines()
    for rel in sorted(p for p in untracked if not p.startswith(".claude/state/")):
        p = ROOT / rel
        if p.is_file():
            material.extend(rel.encode())
            material.extend(b"\0")
            try:
                material.extend(p.read_bytes())
            except OSError:
                pass
            material.extend(b"\0")
    return bytes(material)


def current_diff_hash() -> str:
    return hashlib.sha256(diff_material()).hexdigest()


def dirty() -> bool:
    return bool(diff_material().strip())


def block(reason: str) -> int:
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


def main() -> int:
    if not git_ok():
        return 0
    if not dirty():
        return 0
    try:
        last = json.loads(LAST.read_text(encoding="utf-8"))
    except Exception:
        return block("Working tree has changes but no passing verification record. Run scripts/claude-harness/verify.py before final response.")
    head = current_head()
    dh = current_diff_hash()
    if last.get("status") != "pass":
        return block("Last verification did not pass. Fix failures and re-run verification before final response.")
    if last.get("head") != head or last.get("diff_hash") != dh:
        return block("Current diff hash does not match last passing verification. Run scripts/claude-harness/verify.py again before final response.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
