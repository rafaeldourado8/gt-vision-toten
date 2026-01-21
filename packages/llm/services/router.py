"""Model router for intelligent LLM routing."""
import hashlib
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ModelRouter:
    """Routes requests to appropriate model based on complexity."""

    COMPLEXITY_LOW = 3
    COMPLEXITY_HIGH = 8

    def __init__(self):
        self.metrics = {
            "total": 0,
            "simple": 0,
            "complex": 0,
            "cache_hits": 0,
        }

    def route(self, question: str, force_complex: bool = False) -> Dict:
        """Route to appropriate model."""
        self.metrics["total"] += 1

        if force_complex:
            self.metrics["complex"] += 1
            return {"model": "complex", "reason": "forced"}

        complexity = self._calculate_complexity(question)

        if complexity >= self.COMPLEXITY_HIGH:
            self.metrics["complex"] += 1
            return {"model": "complex", "reason": f"complexity_{complexity}"}

        self.metrics["simple"] += 1
        return {"model": "simple", "reason": f"complexity_{complexity}"}

    def _calculate_complexity(self, question: str) -> int:
        """Calculate question complexity (0-10)."""
        score = 0
        lower = question.lower()

        if len(question) > 500:
            score += 2
        elif len(question) > 200:
            score += 1

        keywords = [
            "architecture",
            "scalability",
            "performance",
            "optimization",
            "design pattern",
            "refactor",
            "debug",
            "async",
            "concurrent",
        ]
        score += sum(1 for kw in keywords if kw in lower)

        if "```" in question:
            score += 2

        if question.count("?") > 1:
            score += 1

        return min(score, 10)

    def hash_question(self, question: str) -> str:
        """Generate hash for caching."""
        return hashlib.sha256(question.lower().strip().encode()).hexdigest()

    def get_metrics(self) -> Dict:
        """Get routing metrics."""
        total = self.metrics["total"]
        return {
            **self.metrics,
            "simple_pct": round((self.metrics["simple"] / total * 100) if total > 0 else 0, 2),
            "complex_pct": round((self.metrics["complex"] / total * 100) if total > 0 else 0, 2),
        }
