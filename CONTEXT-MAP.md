# Context Map

## Contexts

- [Root project context](./CONTEXT.md) — global language and operating rules.
- [Generic target](./target-plugins/generic/TARGET.md) — neutral default target plugin.
- [Python PyQt5 Business MIS/ERP target](./target-plugins/python-pyqt5-business-mis-erp/TARGET.md) — specialized target plugin.

## Relationships

- Root project context defines general agent behavior.
- Target plugin context overrides or narrows behavior for a concrete software domain.
- ADRs under `docs/adr/` record hard-to-reverse decisions.
