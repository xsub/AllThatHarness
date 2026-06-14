# Target: Generic Software Project

This target keeps the harness neutral for projects that do not need a domain-specific plugin.

## Rules

1. Prefer project-native build, lint, and test commands.
2. Keep changes small and directly tied to the requested outcome.
3. Record durable project facts in `memory/` and volatile run evidence in `.claude/state/`.
4. Add domain-specific rules only when the project actually needs them.
5. If a more specific target plugin applies, install it explicitly with `--plugin <name>`.

## Verification shape

Start with the generic profile, then replace or extend it with project-native commands:

```text
format:
check:
test:
pre-push:
```
