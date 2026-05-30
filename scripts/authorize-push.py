#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.cwd()
STATE = ROOT / ".claude" / "state"
LAST = STATE / "last-verification.json"
AUTH = STATE / "push-authorized.json"


def git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL).decode("utf-8", "replace").strip()


def diff_hash() -> str:
    script = "scripts/claude-harness/diff-hash.py" if (ROOT / "scripts/claude-harness/diff-hash.py").exists() else "scripts/diff-hash.py"
    return subprocess.check_output([sys.executable, script], cwd=ROOT).decode().strip()


def main() -> int:
    if not LAST.exists():
        print("No verification record found", flush=True)
        return 2
    last = json.loads(LAST.read_text(encoding="utf-8"))
    head = git(["rev-parse", "HEAD"])
    dh = diff_hash()
    if last.get("status") != "pass" or last.get("head") != head or last.get("diff_hash") != dh:
        print("Current HEAD/diff hash is not verified", flush=True)
        return 2
    STATE.mkdir(parents=True, exist_ok=True)
    record = {
        "status": "authorized",
        "head": head,
        "diff_hash": dh,
        "created_at": time.time(),
        "expires_at": time.time() + 600,
    }
    AUTH.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("push authorized for current verified HEAD/diff for 10 minutes")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
