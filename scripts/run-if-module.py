#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: run-if-module.py [--required] MODULE COMMAND...", file=sys.stderr)
        return 2
    required = False
    args = sys.argv[1:]
    if args[0] == "--required":
        required = True
        args = args[1:]
    if len(args) < 2:
        print("usage: run-if-module.py [--required] MODULE COMMAND...", file=sys.stderr)
        return 2
    module = args[0]
    command = " ".join(args[1:])
    if importlib.util.find_spec(module) is None:
        if required:
            print(f"FAIL required module not installed: {module}", file=sys.stderr)
            return 2
        print(f"SKIP optional module not installed: {module}")
        return 0
    return subprocess.call(command, shell=True, env=os.environ.copy())


if __name__ == "__main__":
    raise SystemExit(main())
