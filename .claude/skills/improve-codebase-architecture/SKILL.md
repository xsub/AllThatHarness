---
name: improve-codebase-architecture
description: Find deepening opportunities, improve seams, increase locality and leverage, and make code more testable. Use for architecture review or refactoring plans.
---
# Improve Codebase Architecture

Surface architectural friction and propose deepening opportunities.

Use these terms exactly:

- **Module** — anything with an interface and implementation.
- **Interface** — everything a caller must know: types, invariants, error modes, ordering, config, performance.
- **Implementation** — code inside the module.
- **Depth** — leverage at the interface.
- **Seam** — where an interface lives; behavior can change without editing in place.
- **Adapter** — concrete thing satisfying an interface at a seam.
- **Leverage** — what callers get from depth.
- **Locality** — change, bugs, knowledge, and verification concentrated in one place.

Principles:

- deletion test: if deleting a module makes complexity vanish, it was pass-through; if complexity reappears across callers, it earned its keep
- interface is the test surface
- one adapter is hypothetical; two adapters make a real seam

## Process

1. Read domain glossary and ADRs.
2. Explore code and note friction: bouncing between modules, shallow pass-throughs, hidden coupling, poor test seams.
3. Present numbered deepening candidates with files, problem, solution, benefits in locality/leverage, and test impact.
4. Do not propose interfaces until the user picks a candidate.
5. Grill the chosen candidate: constraints, dependencies, module shape, seam placement, tests that survive.
6. Update `CONTEXT.md` and ADRs inline when domain or architectural decisions crystallize.
