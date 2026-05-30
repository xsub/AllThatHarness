---
name: pyqt5-gui-testing
description: Test PyQt5 GUI behavior, Qt models, and business operations with pytest, pytest-qt, offscreen Qt, and deterministic calculation vectors. Use when adding or changing PyQt5 UI.
---
# PyQt5 GUI Testing

Testing pyramid for this target:

1. Domain calculation tests without Qt.
2. Operation tests with fake/in-memory UnitOfWork.
3. Qt model tests for row/column/data/setData/signal behavior.
4. Widget smoke tests with `pytest-qt` and `QT_QPA_PLATFORM=offscreen`.

Rules:

- calculation tests use golden vectors
- GUI tests do not prove business correctness alone
- qtbot tests verify user-visible behavior and signal wiring
- test invalid input rejection paths
- test locale/decimal separator policy when relevant
- tests must not depend on wall clock or random order unless pinned
