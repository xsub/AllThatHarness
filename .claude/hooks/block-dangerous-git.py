#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block destructive git and unauthorised push.

Reads Claude Code hook JSON from stdin. Emits structured PreToolUse decisions.
"""
from __future__ import annotations

import json
import re
import shlex
import sys
import time
from pathlib import Path

ROOT = Path.cwd()
STATE = ROOT / ".claude" / "state"

for candidate in (ROOT / "scripts" / "claude-harness", ROOT / "scripts"):
    if (candidate / "harness_diff.py").exists():
        sys.path.insert(0, str(candidate))
        break

from harness_diff import current_diff_hash, current_head  # noqa: E402


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
    head = current_head(ROOT)
    diff_hash = current_diff_hash(ROOT)
    return (
        auth.get("head") == head and
        auth.get("diff_hash") == diff_hash and
        ver.get("head") == head and
        ver.get("diff_hash") == diff_hash and
        ver.get("status") == "pass"
    )


def git_commands(command: str) -> list[list[str]]:
    fragments = re.split(r"(?:&&|\|\||\||;|\n)", command)
    found: list[list[str]] = []
    for fragment in fragments:
        try:
            tokens = shlex.split(fragment)
        except ValueError:
            tokens = fragment.split()
        for index, token in enumerate(tokens):
            if token == "git":
                found.append(tokens[index:])
                break
    return found


def git_subcommand(tokens: list[str]) -> tuple[str, list[str]]:
    options_with_value = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env"}
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token in options_with_value:
            index += 2
            continue
        if token.startswith("--git-dir=") or token.startswith("--work-tree=") or token.startswith("--namespace="):
            index += 1
            continue
        if token.startswith("-"):
            index += 1
            continue
        return token, tokens[index + 1 :]
    return "", []


def has_force_flag(args: list[str]) -> bool:
    for arg in args:
        if arg in {"-f", "--force", "--force-with-lease"} or arg.startswith("--force-with-lease="):
            return True
        if arg.startswith("-") and not arg.startswith("--") and "f" in arg:
            return True
    return False


def has_clean_force_flag(args: list[str]) -> bool:
    return any(arg.startswith("-") and "f" in arg for arg in args)


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
        subcommand, args = git_subcommand(cmd)
        if subcommand == "push" and has_force_flag(args):
            return deny("Blocked: force push is not allowed from Claude Code.")
        if subcommand == "push":
            if not push_is_authorized():
                return deny("Blocked: git push requires fresh verification and explicit authorization. Run scripts/claude-harness/verify.py, then scripts/claude-harness/authorize-push.py.")
        if subcommand == "reset" and "--hard" in args:
            return deny("Blocked: git reset --hard is destructive or can discard work.")
        if subcommand == "clean" and has_clean_force_flag(args):
            return deny("Blocked: git clean -f is destructive or can discard work.")
        if subcommand == "branch" and "-D" in args:
            return deny("Blocked: git branch -D is destructive or can discard work.")
        if subcommand == "checkout" and args == ["."]:
            return deny("Blocked: git checkout . is destructive or can discard work.")
        if subcommand == "restore" and args == ["."]:
            return deny("Blocked: git restore . is destructive or can discard work.")
        if subcommand == "restore" and "--source" in args:
            return deny("Blocked: git restore --source is destructive or can discard work.")

    return allow()


if __name__ == "__main__":
    raise SystemExit(main())
