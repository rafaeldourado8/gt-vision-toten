"""Role entity."""
from typing import List
from uuid import UUID

from ..core.entity import Entity
from .permission import Permission


class Role(Entity):
    """Role entity with permissions."""

    def __init__(
        self,
        entity_id: UUID | None = None,
        name: str = "",
        code: str = "",
        permissions: List[Permission] | None = None,
    ) -> None:
        super().__init__(entity_id)
        self.name = name
        self.code = code
        self.permissions = permissions or []

    def add_permission(self, permission: Permission) -> None:
        if permission not in self.permissions:
            self.permissions.append(permission)
            self._touch()

    def has_permission(self, permission_code: str) -> bool:
        return any(p.code == permission_code for p in self.permissions)
