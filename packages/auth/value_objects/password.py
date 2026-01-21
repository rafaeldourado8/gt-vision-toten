"""Password value object with hashing."""
import hashlib
import secrets

from ...core.exceptions import ValidationException
from ...core.value_object import ValueObject


class Password(ValueObject):
    """Password value object with secure hashing."""

    MIN_LENGTH = 8

    def __init__(self, value: str, hashed: bool = False) -> None:
        if not hashed:
            self._validate(value)
            self.value = self._hash(value)
        else:
            self.value = value

    def _validate(self, value: str) -> None:
        if not value:
            raise ValidationException("Password cannot be empty")
        if len(value) < self.MIN_LENGTH:
            raise ValidationException(f"Password must be at least {self.MIN_LENGTH} characters")

    def _hash(self, value: str) -> str:
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((value + salt).encode()).hexdigest()
        return f"{salt}${hashed}"

    def verify(self, plain_password: str) -> bool:
        try:
            salt, hashed = self.value.split("$")
            test_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
            return test_hash == hashed
        except Exception:
            return False

    def __str__(self) -> str:
        return "********"
