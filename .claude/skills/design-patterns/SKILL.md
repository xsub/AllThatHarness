---
name: design-patterns
description: Apply design patterns only when they remove concrete complexity. Use when considering Factory, Strategy, Adapter, Observer, Repository, Unit of Work, MVC/MVP, Command, or similar abstractions.
---
# Design Patterns

Patterns are vocabulary, not permission to add ceremony.

Before introducing a nontrivial pattern, record:

```text
Pattern:
Problem:
Variation isolated:
Seam created:
Callers simplified:
Test improved:
New complexity:
Rejected simpler option:
```

Reject the pattern if this record is weak.

Go/Python idiom translations:

- Strategy: function or small protocol/interface
- Factory: constructor function unless creation is truly variable
- Adapter: concrete wrapper at a real seam
- Observer: signals/events only with delivery semantics
- Repository: avoid generic CRUD dumping ground
- Singleton: usually explicit dependency/config instead
- Command/Operation: good for business actions with validation, transaction, audit
- Unit of Work: good when one business operation spans multiple repositories
- MVC/MVP: useful for PyQt; never put business rules in widgets
