#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block destructive git and unauthorised push.

Reads Claude Code hook JSON from stdin. Emits structured PreToolUse decisions.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.cwd()
STATE = ROOT / ".claude" / "state"


def deny(reason: str) -> int:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    return 0


def allow() -> int:
    return 0


def run_git(args: list[str]) -> bytes:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL)
    except Exception:
        return b""


def current_head() -> str:
    return run_git(["rev-parse", "HEAD"]).decode("utf-8", "replace").strip()


def current_diff_hash() -> str:
    h = hashlib.sha256()
    for args in (["diff", "--binary", "--", ".", ":(exclude).claude/state"],
                 ["diff", "--cached", "--binary", "--", ".", ":(exclude).claude/state"]):
        h.update(run_git(list(args)))
    untracked = run_git(["ls-files", "--others", "--exclude-standard"]).decode("utf-8", "replace").splitlines()
    for rel in sorted(p for p in untracked if not p.startswith(".claude/state/")):
        p = ROOT / rel
        if p.is_file():
            h.update(rel.encode())
            try:
                h.update(p.read_bytes())
            except OSError:
                pass
    return h.hexdigest()


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def push_is_authorized() -> bool:
    auth = load_json(STATE / "push-authorized.json")
    ver = load_json(STATE / "last-verification.json")
    now = time.time()
    if not auth or not ver:
        return False
    if auth.get("expires_at", 0) < now:
        return False
    head = current_head()
    diff_hash = current_diff_hash()
    return (
        auth.get("head") == head and
        auth.get("diff_hash") == diff_hash and
        ver.get("head") == head and
        ver.get("diff_hash") == diff_hash and
        ver.get("status") == "pass"
    )


def git_commands(command: str) -> list[str]:
    # Split on shell control operators first, then find command fragments beginning with git.
    fragments = re.split(r"(?:&&|\|\||;|\n)", command)
    found: list[str] = []
    for fragment in fragments:
        m = re.search(r"(^|\s)(git\s+[^;&|\n]+)", fragment)
        if m:
            found.append(m.group(2).strip())
    return found


def is_force_push(cmd: str) -> bool:
    return bool(re.search(r"\bgit\s+push(?![\w-])", cmd)) and bool(re.search(r"\s(-f|--force|--force-with-lease)(\s|$)", cmd))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return allow()

    if payload.get("tool_name") != "Bash":
        return allow()
    command = (payload.get("tool_input") or {}).get("command", "")
    if not isinstance(command, str) or not command.strip():
        return allow()

    if re.search(r"rm\s+-[^\n;]*r[^\n;]*\s+\.git(\s|$|/)", command):
        return deny("Blocked: deleting .git is destructive.")

    for cmd in git_commands(command):
        if is_force_push(cmd):
            return deny("Blocked: force push is not allowed from Claude Code.")
        if re.search(r"\bgit\s+push(?![\w-])", cmd):
            if not push_is_authorized():
                return deny("Blocked: git push requires fresh verification and explicit authorization. Run scripts/claude-harness/verify.py, then scripts/claude-harness/authorize-push.py.")
        blocked_patterns = [
            (r"\bgit\s+reset(?![\w-])\s+--hard\b", "git reset --hard"),
            (r"\bgit\s+clean(?![\w-])\s+.*(?:^|\s)-[A-Za-z]*f", "git clean -f"),
            (r"\bgit\s+branch(?![\w-])\s+-D\b", "git branch -D"),
            (r"\bgit\s+checkout(?![\w-])\s+\.\s*$", "git checkout ."),
            (r"\bgit\s+restore(?![\w-])\s+\.\s*$", "git restore ."),
            (r"\bgit\s+restore(?![\w-])\s+--source\b", "git restore --source"),
        ]
        for pattern, label in blocked_patterns:
            if re.search(pattern, cmd):
                return deny(f"Blocked: {label} is destructive or can discard work.")

    return allow()


if __name__ == "__main__":
    raise SystemExit(main())
