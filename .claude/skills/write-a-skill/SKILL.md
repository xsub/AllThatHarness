---
name: write-a-skill
description: Create new skills with proper structure, concise frontmatter, progressive disclosure, references, and deterministic scripts. Use when writing or revising skills.
---
# Write A Skill

A skill directory contains `SKILL.md` and optional references/scripts.

`SKILL.md` should stay focused. Move long or rare material into adjacent files.

Frontmatter:

```yaml
---
name: skill-name
description: What the skill does. Use when specific triggers apply.
---
```

Review checklist:

- description tells Claude when to load it
- no vague trigger language
- instructions are procedural and testable
- supporting files are referenced one level deep
- deterministic work is moved to scripts
- no stale time-sensitive claims
- no duplicate skill names
