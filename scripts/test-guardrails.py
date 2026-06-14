#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(
    args: list[str],
    cwd: Path,
    *,
    input_text: str | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed: {' '.join(args)}\n"
            f"cwd: {cwd}\n"
            f"returncode: {result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], repo)


def prepare_repo(tmp: Path) -> Path:
    repo = tmp / "target"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "harness@example.invalid")
    git(repo, "config", "user.name", "Harness Test")
    run(["bash", str(ROOT / "scripts" / "install-harness.sh"), "--target", str(repo), "--apply"], ROOT)
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "initial harness install")
    return repo


def hook_payload(command: str) -> str:
    return json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})


def run_push_hook(repo: Path, command: str) -> subprocess.CompletedProcess[str]:
    return run(
        [PYTHON, ".claude/hooks/block-dangerous-git.py"],
        repo,
        input_text=hook_payload(command),
    )


def assert_denied(result: subprocess.CompletedProcess[str], expected: str) -> None:
    if expected not in result.stdout:
        raise AssertionError(f"expected denial containing {expected!r}, got stdout:\n{result.stdout}")


def test_verify_authorize_and_push_hook_share_one_diff_hash() -> None:
    with tempfile.TemporaryDirectory(prefix="allthat-guardrails-") as tmp_name:
        repo = prepare_repo(Path(tmp_name))
        (repo / "work.txt").write_text("untracked change\n", encoding="utf-8")

        run([PYTHON, "scripts/claude-harness/verify.py", "--profile", "generic", "--phase", "check"], repo)
        last = json.loads((repo / ".claude/state/last-verification.json").read_text(encoding="utf-8"))
        diff_hash = run([PYTHON, "scripts/claude-harness/diff-hash.py"], repo).stdout.strip()
        if last["diff_hash"] != diff_hash:
            raise AssertionError(f"verification hash {last['diff_hash']} != script hash {diff_hash}")

        run([PYTHON, "scripts/claude-harness/authorize-push.py"], repo)
        allowed = run_push_hook(repo, "git -C . push")
        if allowed.stdout.strip():
            raise AssertionError(f"expected authorized push hook to allow, got stdout:\n{allowed.stdout}")

        (repo / "work.txt").write_text("changed after authorization\n", encoding="utf-8")
        denied = run_push_hook(repo, "git push")
        assert_denied(denied, "git push requires fresh verification")


def test_stop_hook_allows_clean_tree_and_blocks_unverified_changes() -> None:
    with tempfile.TemporaryDirectory(prefix="allthat-stop-hook-") as tmp_name:
        repo = prepare_repo(Path(tmp_name))
        clean = run([PYTHON, ".claude/hooks/require-verified-diff.py"], repo)
        if clean.stdout.strip():
            raise AssertionError(f"expected clean tree to pass Stop hook, got stdout:\n{clean.stdout}")

        (repo / "work.txt").write_text("unverified change\n", encoding="utf-8")
        blocked = run([PYTHON, ".claude/hooks/require-verified-diff.py"], repo)
        if "no passing verification record" not in blocked.stdout:
            raise AssertionError(f"expected Stop hook block, got stdout:\n{blocked.stdout}")


def test_git_hook_blocks_destructive_variants_without_false_positive() -> None:
    with tempfile.TemporaryDirectory(prefix="allthat-git-hook-") as tmp_name:
        repo = prepare_repo(Path(tmp_name))
        reset = run_push_hook(repo, "git -C . reset --hard HEAD")
        assert_denied(reset, "git reset --hard")

        force = run_push_hook(repo, "git push --force-with-lease")
        assert_denied(force, "force push")

        harmless = run_push_hook(repo, "git push-worktree status")
        if harmless.stdout.strip():
            raise AssertionError(f"expected push-worktree command to pass, got stdout:\n{harmless.stdout}")


def main() -> int:
    test_verify_authorize_and_push_hook_share_one_diff_hash()
    test_stop_hook_allows_clean_tree_and_blocks_unverified_changes()
    test_git_hook_blocks_destructive_variants_without_false_positive()
    print("PASS guardrail hook and verification tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
