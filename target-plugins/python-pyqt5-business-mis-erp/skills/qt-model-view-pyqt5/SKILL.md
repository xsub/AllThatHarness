---
name: qt-model-view-pyqt5
description: Apply Qt/PyQt5 model-view separation for business grids, forms, delegates, and editable tables. Use when touching QTableView, QTreeView, QAbstractTableModel, delegates, validators, or PyQt5 widgets.
---
# Qt Model/View for PyQt5

Qt model/view separates stored data from presentation. Preserve that separation.

Rules:

- use `QAbstractTableModel`/`QAbstractItemModel` for business tables, not ad-hoc widget item mutation for real data
- `data()` formats display only; it does not calculate business facts
- `setData()` validates UI edit shape, then delegates business validation to an Operation
- emit correct model signals for data/structure changes
- delegates handle editing mechanics, not domain rules
- use `QDoubleValidator` only as UI input assistance; it is locale-sensitive and double-based
- parse business numbers into Decimal through a domain parser
- keep domain and calculation tests independent of Qt

For editable financial grids, the model should expose domain DTOs and call Operations. It should not become the business layer.
