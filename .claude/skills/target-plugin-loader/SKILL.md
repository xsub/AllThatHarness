---
name: target-plugin-loader
description: Activate, inspect, or build target plugins under target-plugins/. Use when user mentions target plugins, domain-specific overlays, or active target setup.
---
# Target Plugin Loader

Target plugins live under:

```text
target-plugins/<target-name>/
```

A target plugin contains:

```text
PLUGIN.json
TARGET.md
verify.toml
skills/*/SKILL.md
docs/*
templates/*
```

Activation writes `.claude/active-target-plugin` and installs/copies plugin skills into `.claude/skills/` when using the installer.

When active:

1. Read `.claude/active-target-plugin`.
2. Read `target-plugins/<name>/TARGET.md`.
3. Use `target-plugins/<name>/verify.toml` with `scripts/verify.py --profile <name>`.
4. Prefer target skills over generic skills for target-specific choices.
