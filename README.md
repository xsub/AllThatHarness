# AllThatHarness

This package is a project harness for Claude Code. It installs core Karpathy-inspired coding guidelines, engineering skills, external-memory discipline, deterministic hooks, verification scripts, and target-specific plugins.

This version fixes the earlier prototype defects:

- no blind `cp -a` installer
- no root README or Makefile overwrite in target projects
- upstream skills preserved more faithfully and separated from local overlays
- durable project memory separated from volatile `.claude/state/`
- Stop hook verifies the exact diff hash instead of using file mtimes
- git hook uses structured Claude Code hook decisions
- push requires fresh verification plus explicit authorization marker
- target plugin system added under `target-plugins/`
- first target plugin: Python PyQt5 business MIS/ERP with decimal precision and explicit business operations
- core Karpathy guidelines added as `.claude/skills/karpathy-guidelines`

## Install into a repository

Dry run first:

```bash
./scripts/install-harness.sh --target /path/to/repo --plugin python-pyqt5-business-mis-erp --dry-run
```

Apply:

```bash
./scripts/install-harness.sh --target /path/to/repo --plugin python-pyqt5-business-mis-erp --apply --backup-existing
```

The installer copies harness files into safe locations, appends a marked block to `CLAUDE.md`, writes examples instead of overwriting live settings, and uses backups when modifying existing files.

## Verify this harness package

```bash
python3 scripts/check-harness.py
python3 scripts/verify.py --profile harness
```

## Verify a target repo after install

```bash
python3 scripts/claude-harness/verify.py --profile python-pyqt5-business-mis-erp
```

Run a push authorization only after verification passes:

```bash
python3 scripts/claude-harness/authorize-push.py
```

Then a normal `git push` is allowed by the hook. Force pushes remain blocked.
