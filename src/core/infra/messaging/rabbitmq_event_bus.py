"""RabbitMQ event bus."""
import json
import aio_pika
from typing import Callable, Dict
from aio_pika import Message, ExchangeType


class RabbitMQEventBus:
    """RabbitMQ event bus."""

    def __init__(self, rabbitmq_url: str) -> None:
        self._url = rabbitmq_url
        self._connection = None
        self._channel = None
        self._exchange = None
        self._handlers: Dict[str, list[Callable]] = {}

    async def connect(self) -> None:
        """Connect to RabbitMQ."""
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            "gtvision_events",
            ExchangeType.TOPIC,
            durable=True,
        )

    async def publish(self, event_type: str, data: dict) -> None:
        """Publish event."""
        if not self._exchange:
            await self.connect()

        message = Message(
            body=json.dumps(data).encode(),
            content_type="application/json",
        )

        await self._exchange.publish(
            message,
            routing_key=event_type,
        )

    async def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to event."""
        if not self._channel:
            await self.connect()

        queue = await self._channel.declare_queue(
            f"queue_{event_type}",
            durable=True,
        )

        await queue.bind(self._exchange, routing_key=event_type)

        async def on_message(message: aio_pika.IncomingMessage):
            async with message.process():
                data = json.loads(message.body.decode())
                await handler(data)

        await queue.consume(on_message)

    async def close(self) -> None:
        """Close connection."""
        if self._connection:
            await self._connection.close()
