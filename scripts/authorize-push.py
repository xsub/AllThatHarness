#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from pathlib import Path

from harness_diff import current_diff_hash, current_head

ROOT = Path.cwd()
STATE = ROOT / ".claude" / "state"
LAST = STATE / "last-verification.json"
AUTH = STATE / "push-authorized.json"


def main() -> int:
    if not LAST.exists():
        print("No verification record found", flush=True)
        return 2
    last = json.loads(LAST.read_text(encoding="utf-8"))
    head = current_head(ROOT)
    dh = current_diff_hash(ROOT)
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
