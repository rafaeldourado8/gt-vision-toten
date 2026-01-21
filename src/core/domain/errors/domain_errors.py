"""Domain errors."""


class DomainError(Exception):
    """Base domain error."""

    pass


class ValidationError(DomainError):
    """Validation error."""

    pass


class BusinessRuleViolationError(DomainError):
    """Business rule violation error."""

    pass


class NotFoundError(DomainError):
    """Not found error."""

    pass
