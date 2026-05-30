---
name: external-memory
description: Maintain durable repo-local memory and volatile operational state. Use when starting sessions, switching tasks, recording decisions, or preventing context loss.
---
# External Memory

Read before work:

```text
memory/MEMORY.md
memory/active-plan.md
memory/decisions.md
CONTEXT.md
CONTEXT-MAP.md
.claude/active-target-plugin
```

Write durable facts to versioned memory. Write run logs and verification records to `.claude/state/`.

Do not compress project state into chat. Use chat summaries only as navigation. Files are source of truth.

After compaction or resume, reload memory and active target plugin.
