from __future__ import annotations

from decimal import Decimal
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("money_template", ROOT / "templates" / "money.py")
assert SPEC and SPEC.loader
money_template = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = money_template
SPEC.loader.exec_module(money_template)
Money = money_template.Money


def test_money_parse_quantizes_two_places():
    assert Money.parse("1.235", "EUR").amount == Decimal("1.24")


def test_money_add_requires_same_currency():
    assert Money.parse("1.00", "EUR").add(Money.parse("2.00", "EUR")).amount == Decimal("3.00")
