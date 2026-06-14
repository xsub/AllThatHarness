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
- neutral default target plugin plus a Python PyQt5 business MIS/ERP plugin with decimal precision and explicit business operations
- core Karpathy guidelines added as `.claude/skills/karpathy-guidelines`

## Quick Start

Clone the harness:

```bash
git clone https://github.com/xsub/AllThatHarness.git
cd AllThatHarness
```

Optional sanity check:

```bash
python3 scripts/verify.py --profile harness
```

Preview an install into your project:

```bash
./scripts/install-harness.sh --target /path/to/project --dry-run
```

Apply only after the preflight looks right:

```bash
./scripts/install-harness.sh --target /path/to/project --apply
```

The default target plugin is `generic`. Use the PyQt5 MIS/ERP specialization explicitly when it fits the target project:

```bash
./scripts/install-harness.sh --target /path/to/project --apply --plugin python-pyqt5-business-mis-erp
```

## Conflict Policy

The installer always runs a preflight before writing. If it finds an existing different file, it stops before writing anything.

To keep the existing file and write the harness file beside it, rerun explicitly:

```bash
./scripts/install-harness.sh --target /path/to/project --apply --conflicts numbered
```

Numbered conflict files use `path.harness-1`, then `path.harness-2`, and so on. Existing files are not overwritten.

`CLAUDE.md` and `.gitignore` are special: the installer appends an idempotent marked block when the marker is not already present.

## What Gets Installed

- `.claude/skills/` with the core engineering skills and Karpathy guidelines.
- `.claude/hooks/` and `.claude/settings.harness.example.json` for optional Claude Code hooks.
- `scripts/claude-harness/` verification and push-authorization helpers.
- `memory/`, `docs/claude-harness/`, and the selected `target-plugins/<name>/`.
- `.claude/active-target-plugin`, unless an existing different file blocks or is handled with numbered conflict output.

After installation, review `.claude/settings.harness.example.json` and merge the hooks you want into `.claude/settings.json`.

## Verify An Installed Target

```bash
cd /path/to/project
python3 scripts/claude-harness/verify.py --profile python-pyqt5-business-mis-erp
```

For the default generic target:

```bash
python3 scripts/claude-harness/verify.py --profile generic
```

## Verify this harness package

```bash
python3 scripts/check-harness.py
python3 scripts/verify.py --profile harness
python3 scripts/verify.py --profile harness --phase test
```

Run a push authorization only after verification passes:

```bash
python3 scripts/claude-harness/authorize-push.py
```

Then a normal `git push` is allowed by the hook. Force pushes remain blocked.
