#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path.cwd()


def fail(msg: str) -> None:
    print(f"FAIL {msg}")
    raise SystemExit(1)


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail(f"{path} missing frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        fail(f"{path} malformed frontmatter")
    raw = text[4:end]
    out: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def main() -> int:
    project_skill_paths = list((ROOT / ".claude" / "skills").glob("*/SKILL.md"))
    plugin_skill_paths = list((ROOT / "target-plugins").glob("*/skills/*/SKILL.md"))
    skill_paths = project_skill_paths + plugin_skill_paths
    if not skill_paths:
        fail("no skills found")

    def validate(path: Path) -> tuple[str, str]:
        fm = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        name = fm.get("name")
        desc = fm.get("description")
        if not name:
            fail(f"{path} missing name")
        if not desc:
            fail(f"{path} missing description")
        assert name is not None
        assert desc is not None
        if len(desc) > 1024:
            fail(f"{path} description too long")
        return name, desc

    project_names: dict[str, Path] = {}
    for path in project_skill_paths:
        name, _ = validate(path)
        if name in project_names:
            fail(f"duplicate project skill name {name}: {project_names[name]} and {path}")
        project_names[name] = path

    plugin_names_by_plugin: dict[Path, dict[str, Path]] = {}
    for path in plugin_skill_paths:
        name, _ = validate(path)
        plugin_root = path.parents[2]
        names = plugin_names_by_plugin.setdefault(plugin_root, {})
        if name in names:
            fail(f"duplicate target plugin skill name {name}: {names[name]} and {path}")
        names[name] = path

    settings_path = ROOT / ".claude" / "settings.example.json"
    if not settings_path.exists():
        settings_path = ROOT / ".claude" / "settings.harness.example.json"
    json.loads(settings_path.read_text(encoding="utf-8"))
    json.loads((ROOT / "target-plugins" / "python-pyqt5-business-mis-erp" / "PLUGIN.json").read_text(encoding="utf-8"))

    script_paths = list((ROOT / "scripts").glob("*.py")) + list((ROOT / "scripts" / "claude-harness").glob("*.py"))
    for py in list((ROOT / ".claude" / "hooks").glob("*.py")) + script_paths + list((ROOT / "target-plugins").glob("*/templates/*.py")):
        ast.parse(py.read_text(encoding="utf-8"), filename=str(py))

    required_groups = [
        ["CLAUDE.md"],
        [".claude/skills/karpathy-guidelines/SKILL.md"],
        ["memory/MEMORY.md"],
        ["memory/active-plan.md"],
        ["docs/source-map.lock", "docs/claude-harness/source-map.lock"],
        ["docs/source-extractions/andrej-karpathy-skills.md", "docs/claude-harness/source-extractions/andrej-karpathy-skills.md"],
        ["scripts/install-harness.sh", "scripts/claude-harness/install-harness.sh"],
        ["scripts/verify.py", "scripts/claude-harness/verify.py"],
        ["target-plugins/python-pyqt5-business-mis-erp/TARGET.md"],
        ["target-plugins/python-pyqt5-business-mis-erp/verify.toml"],
    ]
    for group in required_groups:
        if not any((ROOT / rel).exists() for rel in group):
            fail("missing one of: " + ", ".join(group))

    print(f"PASS skill lint: {len(skill_paths)} skills")
    print("PASS JSON validation")
    print("PASS Python syntax validation")
    print("PASS required files present")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
