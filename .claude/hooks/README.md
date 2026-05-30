# Hooks

These are deterministic guardrails. They are not suggestions.

- `session-start-context.py` injects durable memory and target plugin pointers.
- `block-dangerous-git.py` blocks destructive git and unauthorised push using structured PreToolUse decisions.
- `require-verified-diff.py` blocks Stop when the current diff hash does not match the last passing verification.

Use `.claude/settings.example.json` as the template. Merge into `.claude/settings.json`; never overwrite an existing project settings file blindly.
