from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, Context, ROUND_HALF_UP, FloatOperation, InvalidOperation, localcontext

MONEY_QUANT = Decimal("0.01")
MONEY_CONTEXT = Context(prec=28, rounding=ROUND_HALF_UP, traps=[FloatOperation])


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    @classmethod
    def parse(cls, value: str, currency: str) -> "Money":
        if not isinstance(value, str):
            raise TypeError("Money.parse requires a string input")
        with localcontext(MONEY_CONTEXT) as ctx:
            try:
                amount = Decimal(value).quantize(MONEY_QUANT, context=ctx)
            except (InvalidOperation, ValueError) as exc:
                raise ValueError(f"invalid money value: {value!r}") from exc
        return cls(amount=amount, currency=currency)

    def add(self, other: "Money") -> "Money":
        self._same_currency(other)
        with localcontext(MONEY_CONTEXT) as ctx:
            return Money((self.amount + other.amount).quantize(MONEY_QUANT, context=ctx), self.currency)

    def subtract(self, other: "Money") -> "Money":
        self._same_currency(other)
        with localcontext(MONEY_CONTEXT) as ctx:
            return Money((self.amount - other.amount).quantize(MONEY_QUANT, context=ctx), self.currency)

    def _same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"currency mismatch: {self.currency} != {other.currency}")
