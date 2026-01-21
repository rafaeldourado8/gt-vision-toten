"""User aggregate root."""
from typing import List
from uuid import UUID

from ..core.aggregate_root import AggregateRoot
from ..core.exceptions import BusinessRuleViolationException, ValidationException
from .role import Role
from .value_objects import Email, Password


class User(AggregateRoot):
    """User aggregate root."""

    MAX_LOGIN_ATTEMPTS = 5

    def __init__(
        self,
        entity_id: UUID | None = None,
        email: Email | None = None,
        password: Password | None = None,
        name: str = "",
        is_active: bool = True,
        roles: List[Role] | None = None,
    ) -> None:
        super().__init__(entity_id)
        if email is None:
            raise ValidationException("Email is required")
        if password is None:
            raise ValidationException("Password is required")

        self.email = email
        self.password = password
        self.name = name
        self.is_active = is_active
        self.roles = roles or []
        self.login_attempts = 0

    @staticmethod
    def create(email: Email, password: Password, name: str) -> "User":
        return User(email=email, password=password, name=name)

    def authenticate(self, plain_password: str) -> None:
        if not self.is_active:
            raise BusinessRuleViolationException("User is inactive")

        if self.login_attempts >= self.MAX_LOGIN_ATTEMPTS:
            raise BusinessRuleViolationException("Too many login attempts")

        if not self.password.verify(plain_password):
            self.login_attempts += 1
            self._touch()
            raise BusinessRuleViolationException("Invalid credentials")

        self.login_attempts = 0
        self._touch()

    def add_role(self, role: Role) -> None:
        if role not in self.roles:
            self.roles.append(role)
            self._touch()

    def has_permission(self, permission_code: str) -> bool:
        return any(role.has_permission(permission_code) for role in self.roles)

    def deactivate(self) -> None:
        self.is_active = False
        self._touch()

    def activate(self) -> None:
        self.is_active = True
        self.login_attempts = 0
        self._touch()
