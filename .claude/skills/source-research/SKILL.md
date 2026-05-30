---
name: source-research
description: Audit external sources used by the harness. Use when updating skills, target plugins, or source-map.lock.
---
# Source Research

Every external source entry must record:

```text
URL:
Repo/path:
Branch or version:
Commit SHA if available:
Retrieval date:
Local target:
Extracted rules:
Rejected rules:
License/terms note:
Status: vendored | adapted | referenced | omitted
```

Do not claim integration when a source was only referenced.
