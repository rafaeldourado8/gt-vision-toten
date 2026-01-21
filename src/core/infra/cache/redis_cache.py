"""Redis cache service."""
import json
import redis.asyncio as redis
from typing import Any


class RedisCache:
    """Redis cache service."""

    def __init__(self, redis_url: str) -> None:
        self._url = redis_url
        self._client = None

    async def connect(self) -> None:
        """Connect to Redis."""
        self._client = await redis.from_url(self._url, decode_responses=True)

    async def get(self, key: str) -> Any | None:
        """Get value from cache."""
        if not self._client:
            await self.connect()

        value = await self._client.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache."""
        if not self._client:
            await self.connect()

        await self._client.setex(
            key,
            ttl,
            json.dumps(value),
        )

    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        if not self._client:
            await self.connect()

        await self._client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        if not self._client:
            await self.connect()

        return await self._client.exists(key) > 0

    async def close(self) -> None:
        """Close connection."""
        if self._client:
            await self._client.close()
