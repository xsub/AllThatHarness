---
name: generic-project
description: Use for general software projects without a more specific target plugin; prefer project-native commands and add only necessary project rules.
---

# Generic Project

Use the existing project conventions first:

1. Read project memory and context.
2. Inspect the repository before changing files.
3. Prefer existing build, lint, test, and packaging commands.
4. Make the smallest useful change.
5. Verify with the narrowest meaningful command, then broaden only when risk requires it.

If the project has strong domain rules, create or select a more specific target plugin.
