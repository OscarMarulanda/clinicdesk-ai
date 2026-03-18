import json
import logging
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from src.application.interfaces.ai_service import AIServiceInterface
from src.application.interfaces.calendar_service import CalendarServiceInterface
from src.application.interfaces.email_service import EmailServiceInterface
from src.domain.entities.article import ArticleCategory
from src.domain.repositories.escalation_repository import EscalationRepositoryBase
from src.domain.repositories.knowledge_repository import KnowledgeRepositoryBase
from src.domain.repositories.session_repository import SessionRepositoryBase
from src.domain.repositories.user_repository import UserRepositoryBase
from src.infrastructure.ai.system_prompt import SYSTEM_PROMPT
from src.infrastructure.ai.tools import TOOL_DEFINITIONS
from src.infrastructure.config import settings

logger = logging.getLogger(__name__)

MAX_TOOL_ROUNDS = 10


class ProcessChatMessageUseCase:
    def __init__(
        self,
        ai_service: AIServiceInterface,
        session_repo: SessionRepositoryBase,
        knowledge_repo: KnowledgeRepositoryBase,
        escalation_repo: EscalationRepositoryBase,
        user_repo: UserRepositoryBase,
        calendar_service: CalendarServiceInterface,
        email_service: EmailServiceInterface,
    ) -> None:
        self._ai = ai_service
        self._session_repo = session_repo
        self._knowledge_repo = knowledge_repo
        self._escalation_repo = escalation_repo
        self._user_repo = user_repo
        self._calendar = calendar_service
        self._email = email_service

    async def execute(
        self, message: str, session_id: UUID, user_id: int | None = None
    ) -> dict[str, Any]:
        # Load session
        session = await self._session_repo.get_by_id(session_id)
        if session is None:
            session = await self._session_repo.create(user_id=user_id)
            session_id = session.id

        # Build conversation history from stored messages
        conversation_history = self._build_history(session.messages)

        # Add user message
        now = datetime.now(timezone.utc)
        user_msg = {
            "role": "user",
            "content": message,
            "timestamp": now.isoformat(),
        }

        # Add to conversation for Claude
        conversation_history.append({"role": "user", "content": message})

        # Call Claude and handle tool loop
        total_input_tokens = 0
        total_output_tokens = 0
        tool_calls_made: list[str] = []

        response = await self._ai.process_message(
            message=message,
            conversation_history=conversation_history[:-1],  # exclude the just-added message
            tools=TOOL_DEFINITIONS,
            system_prompt=SYSTEM_PROMPT,
        )
        total_input_tokens += response["usage"]["input_tokens"]
        total_output_tokens += response["usage"]["output_tokens"]

        rounds = 0
        while response["stop_reason"] == "tool_use" and rounds < MAX_TOOL_ROUNDS:
            rounds += 1

            # Add assistant message with tool calls to conversation
            conversation_history.append({
                "role": "assistant",
                "content": response["raw_content"],
            })

            # Execute all tool calls and build tool results
            tool_results = []
            for tool_call in response["tool_calls"]:
                tool_name = tool_call["name"]
                tool_input = tool_call["input"]
                tool_calls_made.append(tool_name)

                logger.info(f"Executing tool: {tool_name} with input: {tool_input}")
                result = await self._execute_tool(tool_name, tool_input, session_id)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call["id"],
                    "content": json.dumps(result, default=str),
                })

            # Add tool results to conversation
            conversation_history.append({
                "role": "user",
                "content": tool_results,
            })

            # Continue conversation with tool results
            response = await self._ai.process_with_tool_results(
                conversation_history=conversation_history,
                tools=TOOL_DEFINITIONS,
                system_prompt=SYSTEM_PROMPT,
            )
            total_input_tokens += response["usage"]["input_tokens"]
            total_output_tokens += response["usage"]["output_tokens"]

        # Extract final text response
        agent_text = response["content"]

        # Save messages to session
        assistant_msg = {
            "role": "assistant",
            "content": agent_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool_calls": tool_calls_made if tool_calls_made else None,
            "token_count": total_input_tokens + total_output_tokens,
        }

        # Get current messages as dicts
        stored_messages = [
            {
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp.isoformat() if isinstance(m.timestamp, datetime) else m.timestamp,
                "tool_calls": m.tool_calls,
                "token_count": m.token_count,
            }
            for m in session.messages
        ]
        stored_messages.append(user_msg)
        stored_messages.append(assistant_msg)

        await self._session_repo.update_messages(session_id, stored_messages)

        # Update metadata with detailed per-turn and cumulative metrics
        metadata = session.metadata
        metadata["total_input_tokens"] = metadata.get("total_input_tokens", 0) + total_input_tokens
        metadata["total_output_tokens"] = metadata.get("total_output_tokens", 0) + total_output_tokens

        # Cost calculation (Sonnet 4 pricing: $3/M input, $15/M output)
        turn_input_cost = total_input_tokens * 3.0 / 1_000_000
        turn_output_cost = total_output_tokens * 15.0 / 1_000_000
        turn_cost = turn_input_cost + turn_output_cost
        metadata["total_cost_usd"] = round(
            metadata.get("total_cost_usd", 0.0) + turn_cost, 6
        )

        # Per-turn log
        turns = metadata.get("turns", [])
        turns.append({
            "turn": len(turns) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "cost_usd": round(turn_cost, 6),
            "tool_calls": tool_calls_made if tool_calls_made else [],
            "tool_rounds": rounds,
        })
        metadata["turns"] = turns

        # Aggregate tool call counts
        tool_counts: dict[str, int] = metadata.get("tool_call_counts", {})
        for tc in tool_calls_made:
            tool_counts[tc] = tool_counts.get(tc, 0) + 1
        metadata["tool_call_counts"] = tool_counts

        await self._session_repo.update_metadata(session_id, metadata)

        return {
            "message": agent_text,
            "session_id": str(session_id),
            "tool_calls_made": tool_calls_made if tool_calls_made else None,
        }

    async def _execute_tool(
        self, tool_name: str, tool_input: dict[str, Any], session_id: UUID
    ) -> Any:
        try:
            if tool_name == "search_knowledge_base":
                return await self._tool_search_kb(tool_input)
            elif tool_name == "get_article":
                return await self._tool_get_article(tool_input)
            elif tool_name == "escalate_to_human":
                return await self._tool_escalate(tool_input, session_id)
            elif tool_name == "schedule_callback":
                return await self._tool_schedule_callback(tool_input, session_id)
            elif tool_name == "send_escalation_email":
                return await self._tool_send_email(tool_input)
            elif tool_name == "update_session_notes":
                return await self._tool_update_notes(tool_input, session_id)
            elif tool_name == "get_user_info":
                return await self._tool_get_user_info(tool_input)
            elif tool_name == "list_categories":
                return await self._tool_list_categories()
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            logger.error(f"Tool execution error ({tool_name}): {e}")
            return {"error": str(e)}

    async def _tool_search_kb(self, input: dict[str, Any]) -> Any:
        query = input["query"]
        category = input.get("category")
        cat = ArticleCategory(category) if category else None
        results = await self._knowledge_repo.search(query, category=cat)
        if not results:
            return {"results": [], "message": "No articles found matching your query."}
        return {
            "results": [
                {
                    "id": r.id,
                    "title": r.title,
                    "category": r.category.value,
                    "content_preview": r.content[:500],
                    "rank": r.rank,
                }
                for r in results
            ]
        }

    async def _tool_get_article(self, input: dict[str, Any]) -> Any:
        article = await self._knowledge_repo.get_by_id(input["article_id"])
        if article is None:
            return {"error": "Article not found"}
        return {
            "id": article.id,
            "title": article.title,
            "category": article.category.value,
            "content": article.content,
        }

    async def _tool_escalate(self, input: dict[str, Any], session_id: UUID) -> Any:
        escalation = await self._escalation_repo.create(
            session_id=session_id,
            reason=input["reason"],
            summary=input["summary"],
            assigned_to=settings.support_team_email,
        )
        return {
            "escalation_id": escalation.id,
            "status": "created",
            "message": "Escalation has been created and the support team has been notified.",
        }

    async def _tool_schedule_callback(
        self, input: dict[str, Any], session_id: UUID
    ) -> Any:
        try:
            event_id = await self._calendar.create_event(
                summary="ClinicDesk Support Callback",
                description=f"Support callback requested.\n\nIssue: {input['issue_summary']}",
                attendee_email=input["user_email"],
                preferred_time=input["preferred_time"],
            )
            # Update escalation with calendar event if one exists for this session
            escalations, _ = await self._escalation_repo.list_all()
            for esc in escalations:
                if esc.session_id == session_id and esc.calendar_event_id is None:
                    await self._escalation_repo.set_calendar_event(esc.id, event_id)
                    break

            return {
                "event_id": event_id,
                "status": "scheduled",
                "message": f"Callback scheduled. Calendar invite sent to {input['user_email']}.",
            }
        except Exception as e:
            logger.error(f"Calendar scheduling error: {e}")
            return {
                "status": "error",
                "message": f"Could not schedule callback: {e}. The support team has been notified and will reach out directly.",
            }

    async def _tool_send_email(self, input: dict[str, Any]) -> Any:
        try:
            success = await self._email.send_email(
                to_email=input["to_email"],
                subject=input["subject"],
                body=input["conversation_summary"],
            )
            return {
                "status": "sent" if success else "failed",
                "message": "Email sent to the support team." if success else "Failed to send email.",
            }
        except Exception as e:
            logger.error(f"Email sending error: {e}")
            return {
                "status": "error",
                "message": f"Could not send email: {e}",
            }

    async def _tool_update_notes(
        self, input: dict[str, Any], session_id: UUID
    ) -> Any:
        session = await self._session_repo.get_by_id(session_id)
        if session:
            context = session.context
            context["notes"] = input["notes"]
            await self._session_repo.update_context(session_id, context)
        return {"status": "updated"}

    async def _tool_get_user_info(self, input: dict[str, Any]) -> Any:
        try:
            user_id = int(input["user_id"])
        except (ValueError, TypeError):
            return {"error": "Invalid user ID"}
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            return {"error": "User not found"}
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role.value,
        }

    async def _tool_list_categories(self) -> Any:
        categories = await self._knowledge_repo.list_categories()
        return {"categories": categories}

    @staticmethod
    def _build_history(messages: list) -> list[dict[str, Any]]:
        """Convert stored messages into Claude API format."""
        history: list[dict[str, Any]] = []
        for msg in messages:
            history.append({
                "role": msg.role,
                "content": msg.content,
            })
        return history
