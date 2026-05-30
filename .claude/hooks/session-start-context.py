#!/usr/bin/env python3
"""Inject concise external-memory pointers at Claude Code session start."""
from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
MAX_BYTES = 12000


def read_limited(path: Path, limit: int = MAX_BYTES) -> str:
    try:
        data = path.read_bytes()[:limit]
        return data.decode("utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def main() -> int:
    active = (ROOT / ".claude" / "active-target-plugin")
    active_name = active.read_text(encoding="utf-8").strip() if active.exists() else ""
    parts: list[str] = []
    parts.append("# Claude harness session-start context")
    parts.append("Read durable memory before making changes. Do not rely on chat history alone.")
    for rel in ["memory/MEMORY.md", "memory/active-plan.md", "CONTEXT.md", "CONTEXT-MAP.md"]:
        text = read_limited(ROOT / rel)
        if text:
            parts.append(f"\n## {rel}\n{text}")
    if active_name:
        target = ROOT / "target-plugins" / active_name / "TARGET.md"
        text = read_limited(target)
        parts.append(f"\n## Active target plugin\n{active_name}")
        if text:
            parts.append(f"\n## target-plugins/{active_name}/TARGET.md\n{text}")
    print("\n".join(parts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
