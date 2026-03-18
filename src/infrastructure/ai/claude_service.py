from typing import Any

import anthropic

from src.application.interfaces.ai_service import AIServiceInterface
from src.infrastructure.config import settings


class ClaudeAIService(AIServiceInterface):
    def __init__(self, model: str = "claude-sonnet-4-20250514") -> None:
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        self._model = model

    async def process_message(
        self,
        message: str,
        conversation_history: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        system_prompt: str,
    ) -> dict[str, Any]:
        messages = list(conversation_history)
        messages.append({"role": "user", "content": message})

        response = await self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=messages,
        )

        # Extract text content and tool calls
        text_content = ""
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                text_content += block.text
            elif block.type == "tool_use":
                tool_calls.append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })

        return {
            "content": text_content,
            "tool_calls": tool_calls if tool_calls else None,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
            "raw_content": response.content,
        }

    async def process_with_tool_results(
        self,
        conversation_history: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        system_prompt: str,
    ) -> dict[str, Any]:
        """Continue conversation after providing tool results."""
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=conversation_history,
        )

        text_content = ""
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                text_content += block.text
            elif block.type == "tool_use":
                tool_calls.append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })

        return {
            "content": text_content,
            "tool_calls": tool_calls if tool_calls else None,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
            "raw_content": response.content,
        }
