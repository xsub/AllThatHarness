# Module Design

A module has one interface and one implementation. The interface includes more than type signatures: invariants, error modes, ordering, performance expectations, and configuration.

Deep module test:

```text
Can callers do a lot while knowing little?
```

Deletion test:

```text
If this module is deleted, does complexity vanish or reappear across callers?
```

If complexity vanishes, the module was likely pass-through. If complexity reappears, the module earns its seam.
