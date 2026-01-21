"""Email value object."""
import re

from ...core.exceptions import ValidationException
from ...core.value_object import ValueObject


class Email(ValueObject):
    """Email value object with validation."""

    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def __init__(self, value: str) -> None:
        self._validate(value)
        self.value = value.lower().strip()

    def _validate(self, value: str) -> None:
        if not value or not value.strip():
            raise ValidationException("Email cannot be empty")
        if not re.match(self.EMAIL_REGEX, value):
            raise ValidationException(f"Invalid email format: {value}")

    def __str__(self) -> str:
        return self.value
