---
name: pyqt5-business-mis-erp
description: Target-level rules for Python PyQt5 MIS/ERP systems. Use when implementing business desktop workflows, forms, grids, reports, invoices, stock, accounting-adjacent operations, or admin back-office features.
---
# Python PyQt5 Business MIS/ERP

Read `target-plugins/python-pyqt5-business-mis-erp/TARGET.md` first.

Default architecture:

```text
PyQt5 Widget/View/Delegate -> Qt Model/Presenter -> Operation -> Domain -> Repository/UnitOfWork -> DB
```

Hard separation:

- UI captures intent and displays state.
- Qt model adapts domain data to views.
- Operation performs validation, calculation, transaction, audit.
- Domain code is importable and testable without PyQt5.

Before editing:

1. Identify the Operation.
2. Identify affected documents/entities.
3. Identify invariants.
4. Identify Decimal policies.
5. Identify transaction boundary.
6. Identify audit record.
7. Add or update tests.

Never hide business behavior in button callbacks, table delegates, display formatters, or SQL triggers unless explicitly documented and tested.
