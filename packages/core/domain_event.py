"""Domain Event base class."""
from abc import ABC
from datetime import datetime
from uuid import UUID, uuid4


class DomainEvent(ABC):
    """Base class for domain events."""

    def __init__(self) -> None:
        self.event_id: UUID = uuid4()
        self.occurred_at: datetime = datetime.utcnow()
