---
name: git-guardrails
description: Install and verify Claude Code git safety hooks. Use when configuring guardrails for push, reset, clean, branch deletion, checkout/restore, or other destructive git actions.
---
# Git Guardrails

Use `.claude/hooks/block-dangerous-git.py` and `.claude/settings.example.json`.

Blocked:

- force push
- normal push without fresh verification and explicit authorization
- `git reset --hard`
- `git clean -f`
- `git branch -D`
- `git checkout .`
- `git restore .`
- deletion of `.git`

Verification:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"git push origin main"}}' | python3 .claude/hooks/block-dangerous-git.py
```

Expected: JSON denying permission.
