from abc import ABC, abstractmethod
from typing import Any


class AIServiceInterface(ABC):
    @abstractmethod
    async def process_message(
        self,
        message: str,
        conversation_history: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        system_prompt: str,
    ) -> dict[str, Any]:
        """Send a message to the AI model and return the response.

        Returns a dict with:
            - content: str (the text response)
            - tool_calls: list[dict] | None (any tool calls the model wants to make)
            - stop_reason: str
            - usage: dict (token counts)
        """
        ...
