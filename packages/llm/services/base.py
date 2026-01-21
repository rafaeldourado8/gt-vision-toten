"""Base LLM service."""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class BaseLLMService(ABC):
    """Base class for LLM services."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Dict:
        """Generate response from LLM."""
        pass

    @abstractmethod
    def generate_with_history(
        self,
        prompt: str,
        history: List[Dict],
        system_instruction: Optional[str] = None,
    ) -> Dict:
        """Generate with conversation history."""
        pass
