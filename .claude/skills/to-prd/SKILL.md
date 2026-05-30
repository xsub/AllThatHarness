---
name: to-prd
description: Turn current conversation and codebase understanding into a PRD without interviewing. Use when user asks to create a PRD from current context.
---
# To PRD

Do not interview. Synthesize what is already known.

Process:

1. Explore repo if needed. Use glossary vocabulary and respect ADRs.
2. Identify modules to build or modify.
3. Look for deep modules with simple, testable interfaces.
4. Record testing decisions: external behavior, modules tested, prior art.
5. Publish through configured issue tracker with `needs-triage`.

PRD sections:

- Problem Statement
- Solution
- User Stories
- Implementation Decisions
- Testing Decisions
- Out of Scope
- Further Notes

Avoid file paths and code snippets in the PRD; they rot quickly.
