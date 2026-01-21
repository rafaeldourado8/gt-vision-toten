"""Permission entity."""
from uuid import UUID

from ..core.entity import Entity


class Permission(Entity):
    """Permission entity."""

    def __init__(
        self,
        entity_id: UUID | None = None,
        name: str = "",
        code: str = "",
        description: str = "",
    ) -> None:
        super().__init__(entity_id)
        self.name = name
        self.code = code
        self.description = description
