"""Status enum base."""
from enum import Enum


class Status(Enum):
    """Generic status enum."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ERROR = "ERROR"
