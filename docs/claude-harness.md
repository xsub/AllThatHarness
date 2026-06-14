# Claude Harness Installation Notes

This document is copied into target repos as documentation. It is intentionally not copied as the root `README.md`.

## Core behavior

- durable memory in `memory/`
- volatile state in `.claude/state/`
- hooks in `.claude/hooks/`
- skills in `.claude/skills/`
- target plugins in `target-plugins/`
- verification by exact diff hash

## Target plugins

`generic` is the neutral default target plugin.

`python-pyqt5-business-mis-erp` specializes the harness for business MIS/ERP applications built with Python and PyQt5.

Its hard rules:

- use Decimal for money and exact calculations
- make business actions explicit Operation objects/functions
- keep business rules out of widgets
- use Qt model/view separation
- define transaction boundaries explicitly
- emit audit events for state-changing Operations
- test calculations with deterministic vectors
