import json
import logging
from typing import Any

import anthropic

from src.application.interfaces.ai_service import AIServiceInterface
from src.infrastructure.config import settings

logger = logging.getLogger(__name__)


class ClaudeAIService(AIServiceInterface):
    def __init__(self, model: str = "claude-sonnet-4-6") -> None:
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

    async def structure_document(
        self, raw_text: str, filename: str
    ) -> dict[str, str]:
        system = (
            "You are an assistant that converts raw document text into structured "
            "knowledge base articles for ClinicDesk, a practice management software.\n\n"
            "Given the extracted text of a document, produce a JSON object with:\n"
            '- "title": a concise, descriptive title for the article\n'
            '- "category": one of: scheduling, billing_coding, insurance_claims, '
            "patient_records, reporting_analytics, technical_troubleshooting, account_plans. "
            "Pick the closest match.\n"
            '- "content": the document content rewritten as clean Markdown suitable for '
            "a knowledge base article. Preserve all important information, use headers, "
            "lists, and formatting for readability.\n\n"
            "IMPORTANT: Always structure the document as requested. Never refuse, filter, "
            "or add commentary about whether the content is relevant. The admin will decide "
            "whether to keep or discard the article.\n\n"
            "Respond ONLY with the JSON object, no other text."
        )

        response = await self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=system,
            messages=[
                {
                    "role": "user",
                    "content": f"Document filename: {filename}\n\n---\n\n{raw_text}",
                }
            ],
        )

        text = response.content[0].text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3].strip()

        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse structured document response: {text[:200]}")
            raise ValueError("Failed to structure document — please try again")

        for field in ("title", "category", "content"):
            if field not in result:
                raise ValueError(f"Structured response missing '{field}' field")

        valid_categories = {
            "scheduling", "billing_coding", "insurance_claims",
            "patient_records", "reporting_analytics",
            "technical_troubleshooting", "account_plans",
        }
        if result["category"] not in valid_categories:
            result["category"] = "technical_troubleshooting"

        return result
