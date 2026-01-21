"""Student name value object."""
from src.core.domain.base import ValueObject
from src.core.domain.errors import ValidationException


class StudentName(ValueObject):
    """Student name value object."""

    def __init__(self, value: str) -> None:
        if not value or len(value.strip()) < 3:
            raise ValidationException("Student name must have at least 3 characters")
        if len(value) > 100:
            raise ValidationException("Student name must have at most 100 characters")
        self._value = value.strip()

    @property
    def value(self) -> str:
        return self._value

    @property
    def first_name(self) -> str:
        """Get first name."""
        return self._value.split()[0] if self._value else ""

    def __str__(self) -> str:
        return self._value
