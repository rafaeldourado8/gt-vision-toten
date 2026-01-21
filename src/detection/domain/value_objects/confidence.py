"""Confidence value object."""
from src.core.domain.base import ValueObject
from src.core.domain.errors import ValidationException


class Confidence(ValueObject):
    """Confidence level (0.0 to 1.0)."""

    def __init__(self, value: float) -> None:
        if not 0.0 <= value <= 1.0:
            raise ValidationException(f"Confidence must be between 0.0 and 1.0, got {value}")
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    @property
    def percentage(self) -> float:
        """Get confidence as percentage."""
        return self._value * 100

    @property
    def is_high(self) -> bool:
        """Check if confidence is high (>= 0.8)."""
        return self._value >= 0.8

    @property
    def is_medium(self) -> bool:
        """Check if confidence is medium (0.5 - 0.8)."""
        return 0.5 <= self._value < 0.8

    @property
    def is_low(self) -> bool:
        """Check if confidence is low (< 0.5)."""
        return self._value < 0.5

    def __str__(self) -> str:
        return f"{self.percentage:.2f}%"
