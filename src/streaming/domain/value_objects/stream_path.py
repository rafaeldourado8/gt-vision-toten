"""Stream path value object."""
import re
from src.core.domain.base import ValueObject
from src.core.domain.errors import ValidationException


class StreamPath(ValueObject):
    """Stream path for MediaMTX."""

    PATH_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")

    def __init__(self, value: str) -> None:
        if not self._is_valid(value):
            raise ValidationException(
                f"Invalid stream path: {value}. "
                "Only alphanumeric, underscore and hyphen allowed."
            )
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def _is_valid(self, value: str) -> bool:
        return bool(self.PATH_PATTERN.match(value)) and 1 <= len(value) <= 50

    def __str__(self) -> str:
        return self._value
