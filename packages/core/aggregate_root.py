"""Aggregate Root base class for DDD."""
from typing import List
from uuid import UUID

from .domain_event import DomainEvent
from .entity import Entity


class AggregateRoot(Entity):
    """Base class for aggregate roots."""

    def __init__(self, entity_id: UUID | None = None) -> None:
        super().__init__(entity_id)
        self._domain_events: List[DomainEvent] = []

    @property
    def domain_events(self) -> List[DomainEvent]:
        return self._domain_events.copy()

    def add_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        self._domain_events.clear()
