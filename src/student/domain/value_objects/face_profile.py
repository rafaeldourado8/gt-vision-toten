"""Face profile value object."""
from typing import List
from src.core.domain.base import ValueObject


class FaceProfile(ValueObject):
    """Face profile containing photo path and encoding."""

    def __init__(self, photo_path: str, encoding: List[float] | None = None) -> None:
        self._photo_path = photo_path
        self._encoding = encoding or []

    @property
    def photo_path(self) -> str:
        return self._photo_path

    @property
    def encoding(self) -> List[float]:
        return self._encoding

    @property
    def has_encoding(self) -> bool:
        """Check if profile has face encoding."""
        return len(self._encoding) > 0

    def update_encoding(self, encoding: List[float]) -> "FaceProfile":
        """Create new profile with updated encoding."""
        return FaceProfile(self._photo_path, encoding)
