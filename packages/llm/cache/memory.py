"""Cache service for LLM responses."""
import hashlib
import json
from typing import Dict, Optional


class CacheService:
    """In-memory cache for LLM responses."""

    TTL_ANSWER = 604800  # 7 days
    TTL_CONTEXT = 3600  # 1 hour

    def __init__(self):
        self._cache: Dict[str, Dict] = {}
        self.stats = {"hits": 0, "misses": 0}

    def cache_answer(self, question: str, answer: Dict, ttl: int = None):
        """Cache LLM answer."""
        key = self._hash(question)
        self._cache[key] = {"data": answer, "ttl": ttl or self.TTL_ANSWER}

    def get_cached_answer(self, question: str) -> Optional[Dict]:
        """Get cached answer."""
        key = self._hash(question)
        if key in self._cache:
            self.stats["hits"] += 1
            return self._cache[key]["data"]
        self.stats["misses"] += 1
        return None

    def invalidate(self, question: str) -> bool:
        """Invalidate cached answer."""
        key = self._hash(question)
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self):
        """Clear all cache."""
        self._cache.clear()

    def _hash(self, text: str) -> str:
        """Generate cache key."""
        return hashlib.sha256(text.lower().strip().encode()).hexdigest()

    def get_stats(self) -> Dict:
        """Get cache statistics."""
        total = self.stats["hits"] + self.stats["misses"]
        return {
            **self.stats,
            "hit_rate": round((self.stats["hits"] / total * 100) if total > 0 else 0, 2),
            "size": len(self._cache),
        }
