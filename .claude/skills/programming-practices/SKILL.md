---
name: programming-practices
description: Apply general programming discipline: readable naming, modularity, tests, errors, documentation, security, performance, data structures, version control, and refactoring. Use for any code review or implementation.
---
# Programming Practices

For every code change answer:

- What public behavior changed?
- What invariant is protected?
- What test proves it?
- What error path changed?
- What input is untrusted?
- What state is hidden?
- What dependency was added?
- What would make this fail in production?

Rules:

- descriptive names over clever names
- comments explain why, not obvious what
- no duplication without reason
- unit tests for pure logic; integration tests for workflows
- consistent style via formatter
- explicit error handling
- public functions/types documented
- optimize only after measuring or when invariant requires it
- validate and sanitize inputs
- version-control every meaningful change
- plan before programming
- choose simplest suitable data structure
- cohesive modules, low coupling
- edge and error scenarios tested
- refactor regularly while tests are green
- avoid global mutable state
- record significant changes
- single responsibility per function/class/module
- consider time and space efficiency
- learn from failures by recording prevention patterns
