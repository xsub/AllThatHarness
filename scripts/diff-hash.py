#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from harness_diff import current_diff_hash

ROOT = Path.cwd()


def main() -> int:
    print(current_diff_hash(ROOT))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
