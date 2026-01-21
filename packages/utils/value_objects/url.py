"""URL value object."""
from urllib.parse import urlparse

from ...core.exceptions import ValidationException
from ...core.value_object import ValueObject


class URL(ValueObject):
    """URL value object with validation."""

    def __init__(self, value: str, allowed_schemes: list[str] | None = None) -> None:
        self.allowed_schemes = allowed_schemes or ["http", "https"]
        self._validate(value)
        self.value = value

    def _validate(self, value: str) -> None:
        if not value:
            raise ValidationException("URL cannot be empty")
        parsed = urlparse(value)
        if parsed.scheme not in self.allowed_schemes:
            raise ValidationException(f"URL must use {', '.join(self.allowed_schemes)}")
        if not parsed.netloc:
            raise ValidationException("Invalid URL")

    def __str__(self) -> str:
        return self.value
