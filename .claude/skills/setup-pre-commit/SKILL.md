---
name: setup-pre-commit
description: Set up project pre-commit checks. Use when adding commit-time formatting, linting, typechecking, or tests.
---
# Setup Pre-Commit

Never overwrite existing hooks blindly.

Detect ecosystem:

- Node: package manager lockfile; Husky/lint-staged if appropriate
- Python: `.pre-commit-config.yaml`, Ruff, mypy, pytest
- Go: gofmt/go vet/go test
- C/C++: clang-format/clang-tidy/build smoke

Steps:

1. Inspect existing hooks and config.
2. Present proposed commands.
3. Create or merge config with backup.
4. Run the pre-commit command directly before declaring done.
5. Record verification evidence.
