# Validation

Performed before packaging AllThatHarness:

```text
PASS python3 scripts/check-harness.py
PASS python3 scripts/verify.py --profile harness
PASS python3 scripts/verify.py --profile python-pyqt5-business-mis-erp --phase check
PASS python3 scripts/verify.py --profile python-pyqt5-business-mis-erp --phase test
PASS install-harness.sh --dry-run into empty target
PASS install-harness.sh --apply --backup-existing into empty target
PASS installed target profile check
PASS installed target profile test
PASS hook blocks git push
PASS hook blocks cd x && git reset --hard HEAD
PASS hook does not false-positive git push-worktree status
```

The artifact intentionally does not include `.claude/state/`, `.pytest_cache/`, or Python `__pycache__` output.
