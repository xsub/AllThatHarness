#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

ROOT = Path.cwd()
STATE = ROOT / ".claude" / "state"


def run(cmd: str, env: dict[str, str]) -> int:
    print(f"+ {cmd}", flush=True)
    return subprocess.call(cmd, cwd=ROOT, shell=True, env=env)


def git(args: list[str]) -> bytes:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL)
    except Exception:
        return b""


def head() -> str:
    return git(["rev-parse", "HEAD"]).decode("utf-8", "replace").strip() or "nogit"


def diff_material() -> bytes:
    b = bytearray()
    b.extend(git(["diff", "--binary", "--", ".", ":(exclude).claude/state"]))
    b.extend(b"\n--STAGED--\n")
    b.extend(git(["diff", "--cached", "--binary", "--", ".", ":(exclude).claude/state"]))
    b.extend(b"\n--UNTRACKED--\n")
    for rel in sorted(git(["ls-files", "--others", "--exclude-standard"]).decode("utf-8", "replace").splitlines()):
        if rel.startswith(".claude/state/"):
            continue
        p = ROOT / rel
        if p.is_file():
            b.extend(rel.encode())
            b.extend(b"\0")
            try:
                b.extend(p.read_bytes())
            except OSError:
                pass
    return bytes(b)


def diff_hash() -> str:
    return hashlib.sha256(diff_material()).hexdigest()


def load_configs() -> dict:
    data: dict = {"profiles": {}}
    paths = [ROOT / ".claude" / "verify.toml"]
    active_file = ROOT / ".claude" / "active-target-plugin"
    if active_file.exists():
        active = active_file.read_text(encoding="utf-8").strip()
        paths.append(ROOT / "target-plugins" / active / "verify.toml")
    for path in paths:
        if path.exists():
            parsed = tomllib.loads(path.read_text(encoding="utf-8"))
            for name, profile in parsed.get("profiles", {}).items():
                data["profiles"][name] = profile
    return data


def commands_for(profile: dict, phase: str) -> list[str]:
    if phase == "all":
        return list(profile.get("format", [])) + list(profile.get("check", [])) + list(profile.get("test", []))
    if phase == "pre-push":
        return list(profile.get("check", [])) + list(profile.get("test", [])) + list(profile.get("pre_push", []))
    return list(profile.get(phase.replace("-", "_"), []))


def write_record(status: str, profile: str, phase: str, cmds: list[str], rc: int, before: str, after: str) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    record = {
        "status": status,
        "profile": profile,
        "phase": phase,
        "returncode": rc,
        "head": head(),
        "diff_hash": after,
        "diff_hash_before": before,
        "commands": cmds,
        "timestamp": time.time(),
    }
    (STATE / "last-verification.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    with (STATE / "verification-ledger.md").open("a", encoding="utf-8") as f:
        f.write(f"\n## {time.strftime('%Y-%m-%d %H:%M:%S')} {status}\n")
        f.write(f"profile: {profile}\nphase: {phase}\nhead: {record['head']}\ndiff_hash: {after}\n")
        for cmd in cmds:
            f.write(f"- `{cmd}`\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default=None)
    parser.add_argument("--phase", choices=["all", "format", "check", "test", "pre-push"], default="all")
    args = parser.parse_args()

    cfg = load_configs()
    profile_name = args.profile
    if profile_name is None:
        active_file = ROOT / ".claude" / "active-target-plugin"
        profile_name = active_file.read_text(encoding="utf-8").strip() if active_file.exists() else "default"
    profile = cfg.get("profiles", {}).get(profile_name)
    if profile is None:
        print(f"unknown verify profile: {profile_name}", file=sys.stderr)
        return 2

    cmds = commands_for(profile, args.phase)
    if not cmds:
        print(f"no commands for profile={profile_name} phase={args.phase}")
    env = os.environ.copy()
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    before = diff_hash()
    rc = 0
    for cmd in cmds:
        rc = run(cmd, env)
        if rc != 0:
            after = diff_hash()
            write_record("fail", profile_name, args.phase, cmds, rc, before, after)
            return rc
    after = diff_hash()
    if args.phase not in {"format"} and before != after:
        print("verification command mutated the working tree; rerun after reviewing changes", file=sys.stderr)
        write_record("fail", profile_name, args.phase, cmds, 3, before, after)
        return 3
    write_record("pass", profile_name, args.phase, cmds, 0, before, after)
    print(f"PASS profile={profile_name} phase={args.phase} diff_hash={after}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
