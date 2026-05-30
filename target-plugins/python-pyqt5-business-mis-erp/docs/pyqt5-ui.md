# PyQt5 UI Rules

Widgets are presentation and intent capture.

Allowed in widgets:

- collect text/selection/check state
- trigger Operations
- display Operation results
- show validation errors
- bind models to views

Forbidden in widgets:

- invoice total calculation
- tax calculation
- stock movement business rules
- database transactions
- audit decisions
- authorization logic

Use Qt model/view for grids. Keep domain calculation importable without PyQt5.
