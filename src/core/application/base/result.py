"""Result pattern for use cases."""
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    """Result pattern."""

    success: bool
    value: T | None = None
    error: str | None = None

    @staticmethod
    def ok(value: T) -> "Result[T]":
        return Result(success=True, value=value)

    @staticmethod
    def fail(error: str) -> "Result[T]":
        return Result(success=False, error=error)

    @property
    def is_success(self) -> bool:
        return self.success

    @property
    def is_failure(self) -> bool:
        return not self.success
