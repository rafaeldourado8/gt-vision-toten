"""Bounding box value object."""
from dataclasses import dataclass
from src.core.domain.base import ValueObject
from src.core.domain.errors import ValidationException


@dataclass(frozen=True)
class BoundingBox(ValueObject):
    """Bounding box for face detection."""

    x: int
    y: int
    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValidationException("Width and height must be positive")
        if self.x < 0 or self.y < 0:
            raise ValidationException("X and Y must be non-negative")

    @property
    def area(self) -> int:
        """Calculate bounding box area."""
        return self.width * self.height

    @property
    def center(self) -> tuple[int, int]:
        """Get center point of bounding box."""
        return (self.x + self.width // 2, self.y + self.height // 2)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }
