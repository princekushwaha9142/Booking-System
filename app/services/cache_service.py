import json
import logging
from typing import Optional, Any
import redis.asyncio as aioredis
from app.core.config import settings

logger = logging.getLogger(__name__)


class CacheService:

    def __init__(self):
        self._client: Optional[aioredis.Redis] = None

    async def connect(self):
        self._client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
        await self._client.ping()
        logger.info("Redis connected.")

    async def disconnect(self):
        if self._client:
            await self._client.aclose()

    async def get(self, key: str) -> Optional[Any]:
        try:
            data = await self._client.get(key)
            return json.loads(data) if data else None
        except Exception as exc:
            logger.warning("Cache GET failed: %s", exc)
            return None

    async def set(self, key: str, value: Any, ttl: int = settings.CACHE_TTL_SECONDS):
        try:
            await self._client.set(key, json.dumps(value, default=str), ex=ttl)
        except Exception as exc:
            logger.warning("Cache SET failed: %s", exc)

    async def delete(self, key: str):
        try:
            await self._client.delete(key)
        except Exception as exc:
            logger.warning("Cache DELETE failed: %s", exc)

    async def delete_pattern(self, pattern: str):
        try:
            keys = await self._client.keys(pattern)
            if keys:
                await self._client.delete(*keys)
        except Exception as exc:
            logger.warning("Cache PATTERN DELETE failed: %s", exc)

    # Key builders
    def user_bookings_key(self, user_id: int, suffix: str = "all") -> str:
        return f"user:{user_id}:bookings:{suffix}"

    def booking_key(self, booking_id: int) -> str:
        return f"booking:{booking_id}"

    def user_tasks_key(self, user_id: int, suffix: str = "all") -> str:
        return f"user:{user_id}:tasks:{suffix}"

    def task_key(self, task_id: int) -> str:
        return f"task:{task_id}"

    def search_key(self, search_type: str, params_hash: str) -> str:
        return f"search:{search_type}:{params_hash}"


cache_service = CacheService()