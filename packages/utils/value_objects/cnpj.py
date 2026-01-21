"""CNPJ value object."""
import re

from ...core.exceptions import ValidationException
from ...core.value_object import ValueObject


class CNPJ(ValueObject):
    """CNPJ value object with validation."""

    def __init__(self, value: str) -> None:
        self._validate(value)
        self.value = re.sub(r"\D", "", value)

    def _validate(self, value: str) -> None:
        if not value:
            raise ValidationException("CNPJ cannot be empty")
        digits = re.sub(r"\D", "", value)
        if len(digits) != 14:
            raise ValidationException("CNPJ must have 14 digits")

    def __str__(self) -> str:
        v = self.value
        return f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:]}"
