"""Domain errors."""
from .exceptions import (
    DomainException,
    ValidationException,
    BusinessRuleViolationException,
    NotFoundException,
)

__all__ = [
    "DomainException",
    "ValidationException",
    "BusinessRuleViolationException",
    "NotFoundException",
]
