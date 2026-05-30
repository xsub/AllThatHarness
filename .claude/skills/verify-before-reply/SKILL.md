---
name: verify-before-reply
description: Require concrete verification evidence before final answer. Use when code, config, tests, hooks, or generated artifacts changed.
---
# Verify Before Reply

Before final reply:

1. Run the narrowest meaningful verification.
2. If code changed, run tests or compile checks.
3. If hooks changed, test hook inputs.
4. If installer changed, dry-run it.
5. If artifact changed, validate integrity.
6. Record exact command, result, head, and diff hash in `.claude/state/last-verification.json`.

Do not say done without command evidence.
