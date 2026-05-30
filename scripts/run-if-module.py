#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: run-if-module.py MODULE COMMAND...", file=sys.stderr)
        return 2
    module = sys.argv[1]
    command = " ".join(sys.argv[2:])
    if importlib.util.find_spec(module) is None:
        print(f"SKIP optional module not installed: {module}")
        return 0
    return subprocess.call(command, shell=True, env=os.environ.copy())


if __name__ == "__main__":
    raise SystemExit(main())
