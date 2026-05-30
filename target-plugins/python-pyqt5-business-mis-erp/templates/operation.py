from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class OperationResult:
    ok: bool
    message: str
    entity_id: str | None = None


@runtime_checkable
class UnitOfWork(Protocol):
    def __enter__(self) -> "UnitOfWork": ...
    def __exit__(self, exc_type, exc, tb) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


@dataclass(frozen=True, slots=True)
class OperationInput:
    actor_id: str


class BusinessOperation:
    name = "BusinessOperation"

    def execute(self, data: OperationInput, uow: UnitOfWork) -> OperationResult:
        self.validate(data)
        with uow:
            try:
                result = self._apply(data, uow)
                uow.commit()
                return result
            except Exception:
                uow.rollback()
                raise

    def validate(self, data: OperationInput) -> None:
        if not data.actor_id:
            raise ValueError("actor_id is required")

    def _apply(self, data: OperationInput, uow: UnitOfWork) -> OperationResult:
        raise NotImplementedError
