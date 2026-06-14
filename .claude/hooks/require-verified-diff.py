#!/usr/bin/env python3
"""Claude Code Stop hook: require a passing verification for the exact current diff."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
STATE = ROOT / ".claude" / "state"
LAST = STATE / "last-verification.json"

for candidate in (ROOT / "scripts" / "claude-harness", ROOT / "scripts"):
    if (candidate / "harness_diff.py").exists():
        sys.path.insert(0, str(candidate))
        break

from harness_diff import current_diff_hash, current_head, has_material_changes  # noqa: E402


def git_ok() -> bool:
    try:
        subprocess.check_call(["git", "rev-parse", "--is-inside-work-tree"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def block(reason: str) -> int:
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


def main() -> int:
    if not git_ok():
        return 0
    if not has_material_changes(ROOT):
        return 0
    try:
        last = json.loads(LAST.read_text(encoding="utf-8"))
    except Exception:
        return block("Working tree has changes but no passing verification record. Run scripts/claude-harness/verify.py before final response.")
    head = current_head(ROOT)
    dh = current_diff_hash(ROOT)
    if last.get("status") != "pass":
        return block("Last verification did not pass. Fix failures and re-run verification before final response.")
    if last.get("head") != head or last.get("diff_hash") != dh:
        return block("Current diff hash does not match last passing verification. Run scripts/claude-harness/verify.py again before final response.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
