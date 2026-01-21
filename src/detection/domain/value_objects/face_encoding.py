"""Face encoding value object."""
from typing import List
from src.core.domain.base import ValueObject
from src.core.domain.errors import ValidationException


class FaceEncoding(ValueObject):
    """Face encoding (embedding vector)."""

    def __init__(self, embedding: List[float]) -> None:
        if not embedding:
            raise ValidationException("Face encoding cannot be empty")
        self._embedding = embedding

    @property
    def embedding(self) -> List[float]:
        return self._embedding

    @property
    def dimension(self) -> int:
        """Get embedding dimension."""
        return len(self._embedding)

    def to_list(self) -> List[float]:
        """Convert to list."""
        return self._embedding.copy()

    def __str__(self) -> str:
        return f"FaceEncoding(dim={self.dimension})"
