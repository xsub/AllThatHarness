---
name: setup-matt-pocock-skills
description: Scaffold per-repo issue tracker, triage labels, and domain-doc config consumed by engineering skills. Run before triage, to-issues, to-prd, diagnose, tdd, architecture review, or zoom-out.
disable-model-invocation: true
---
# Setup Engineering Skills Scaffold

Configure:

- issue tracker: GitHub, GitLab, local markdown, or other
- triage labels: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix
- domain docs: single `CONTEXT.md` or multi-context `CONTEXT-MAP.md`

## Process

1. Explore repo: git remotes, `CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, `docs/agents/`, `.scratch/`.
2. Present findings and missing parts.
3. Walk three decisions one at a time: issue tracker, label mapping, domain-doc layout.
4. Draft the `## Agent skills` block and `docs/agents/*.md` files.
5. Edit existing `CLAUDE.md` if present; else `AGENTS.md` if present; do not create the other when one already exists.
6. Update an existing `## Agent skills` block in place instead of appending duplicates.

## Files produced

```text
docs/agents/issue-tracker.md
docs/agents/triage-labels.md
docs/agents/domain.md
```
