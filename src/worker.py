"""Background worker for processing streams."""
import asyncio
import os
from src.core.infra.messaging.rabbitmq_event_bus import RabbitMQEventBus
from src.core.infra.cache.redis_cache import RedisCache

# Get environment variables
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


async def handle_face_detected(data: dict) -> None:
    """Handle face detected event."""
    print(f"Face detected: {data}")
    # TODO: Implement face matching and attendance registration


async def main():
    """Main worker loop."""
    print("Starting GT-Vision Worker...")
    
    # Initialize services
    event_bus = RabbitMQEventBus(RABBITMQ_URL)
    cache = RedisCache(REDIS_URL)
    
    await event_bus.connect()
    await cache.connect()
    
    print("Connected to RabbitMQ and Redis")
    
    # Subscribe to events
    await event_bus.subscribe("face.detected", handle_face_detected)
    
    print("Worker ready. Waiting for events...")
    
    # Keep running
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        print("Shutting down worker...")
        await event_bus.close()
        await cache.close()


if __name__ == "__main__":
    asyncio.run(main())
