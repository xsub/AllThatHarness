# Claude Code Engineering Harness

## Core Karpathy guidelines

Use `karpathy-guidelines` as core behavior for coding work:

1. Think before coding: surface assumptions, ambiguity, and tradeoffs.
2. Simplicity first: implement the minimum code that solves the request.
3. Surgical changes: touch only what the task requires and clean up only your own mess.
4. Goal-driven execution: define verifiable success criteria and loop until checked.

## Operating law

Use external memory. Do not rely on chat context as the source of truth. Read durable memory and context before changing code.

Default loop:

```text
read memory -> read context -> inspect repo -> state invariant -> make one semantic change -> verify exact diff -> record evidence -> continue
```

Rules:

1. Read `memory/MEMORY.md`, `memory/active-plan.md`, `CONTEXT.md`, and relevant ADRs before implementation.
2. If `.claude/active-target-plugin` exists, read that target plugin's `TARGET.md` and relevant skills/docs.
3. Do not compress project state into chat. Store durable state in files.
4. Make one semantic change at a time. No batch edits that hide causality.
5. Verify after each change using the most specific project-native check available.
6. Never claim completion unless the current diff hash was verified.
7. Never push without fresh verification and explicit push authorization.
8. Use good programming practice: descriptive names, cohesive modules, explicit errors, strong validation, unit/integration tests, security checks, version control, and regular refactoring.
9. Use design patterns only when they reduce real complexity. Record the problem, rejected simpler option, seam, and added complexity before introducing a nontrivial abstraction.
10. For business/MIS/ERP work or the PyQt5 MIS/ERP target plugin, calculations are explicit domain operations. Use exact decimal arithmetic. No hidden widget-side business math. No binary float for money.

## External memory layout

Versioned durable memory:

```text
memory/MEMORY.md
memory/active-plan.md
memory/decisions.md
memory/patterns.md
memory/open-questions.md
CONTEXT.md
docs/adr/*.md
```

Volatile operational state, gitignored after install:

```text
.claude/state/last-verification.json
.claude/state/verification-ledger.md
.claude/state/session-log.md
.claude/state/push-authorized.json
```

## Target plugins

Target plugins live under `target-plugins/<target-name>/`. They add domain-specific skills, docs, templates, and verification profiles.

Active target is read from `.claude/active-target-plugin`.

Default target:

```text
generic
```

Specialized target:

```text
python-pyqt5-business-mis-erp
```

The specialized PyQt5 MIS/ERP target requires explicit business operations, exact decimal calculation policy, Qt model/view separation, transaction boundaries, audit events, and GUI tests with deterministic calculation vectors.
