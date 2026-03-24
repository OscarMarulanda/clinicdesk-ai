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

        self._current_session_id = session_id

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
        all_text_parts: list[str] = []

        response = await self._ai.process_message(
            message=message,
            conversation_history=conversation_history[:-1],  # exclude the just-added message
            tools=TOOL_DEFINITIONS,
            system_prompt=SYSTEM_PROMPT,
        )
        total_input_tokens += response["usage"]["input_tokens"]
        total_output_tokens += response["usage"]["output_tokens"]
        if response["content"]:
            all_text_parts.append(response["content"])

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
            if response["content"]:
                all_text_parts.append(response["content"])

        # Use the last text response — that's the one meant for the user
        agent_text = all_text_parts[-1] if all_text_parts else ""

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

        # Cost calculation (Sonnet 4.6 pricing: $3/M input, $15/M output)
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
            elif tool_name == "check_availability":
                return await self._tool_check_availability(tool_input)
            elif tool_name == "escalate_to_human":
                return await self._tool_escalate(tool_input, session_id)
            elif tool_name == "update_session_notes":
                return await self._tool_update_notes(tool_input, session_id)
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

    async def _tool_check_availability(self, input: dict[str, Any]) -> Any:
        """Pure read — checks calendar, returns options, creates nothing."""
        try:
            slots = await self._calendar.check_availability(
                preferred_time=input["preferred_time"],
            )
            if not slots:
                return {
                    "available_slots": [],
                    "message": "No available slots found near the requested time. Ask the user for a different time.",
                }
            # Store slots in session context for resolution later
            session = await self._session_repo.get_by_id(self._current_session_id)
            if session:
                ctx = session.context
                ctx["pending_slots"] = slots
                await self._session_repo.update_context(self._current_session_id, ctx)

            return {
                "available_slots": [
                    {"start": s["start"], "end": s["end"]}
                    for s in slots
                ],
                "next_step": (
                    "Show these available times to the user in a friendly, conversational way. "
                    "Let them respond naturally. When they choose, call escalate_to_human "
                    "and pass their choice as confirmed_time using the exact 'start' value "
                    "from the slot they picked. If the user replies with a time like '4' or "
                    "'4pm', match it to the closest slot by hour — do NOT interpret bare "
                    "numbers as option indices."
                ),
            }
        except Exception as e:
            logger.error(f"Availability check error: {e}")
            return {"error": str(e)}

    async def _tool_escalate(self, input: dict[str, Any], session_id: UUID) -> Any:
        """Creates everything in one shot: escalation record + calendar event + emails + notification."""
        reason_labels = {
            "knowledge_gap": "Knowledge Gap",
            "user_frustration": "User Frustration",
            "out_of_scope": "Out of Scope",
            "billing_dispute": "Billing Dispute",
            "account_change": "Account Change",
        }
        reason_label = reason_labels.get(input["reason"], input["reason"])
        preferred = input.get("preferred_action", "email")
        user_email = input.get("user_email")
        confirmed_time = input.get("confirmed_time")

        # Resolve confirmed_time from stored slots — require check_availability to have been called
        if confirmed_time and preferred in ("calendar", "both"):
            session = await self._session_repo.get_by_id(session_id)
            pending_slots = session.context.get("pending_slots", []) if session else []

            if not pending_slots:
                return {
                    "error": "You must call check_availability first before booking a callback. "
                    "No available slots have been checked yet.",
                }

            # If already ISO format, validate it matches a pending slot
            if "T" in confirmed_time:
                confirmed_start = confirmed_time.split("T")[1][:5]  # HH:MM
                slot_starts = [s["start"].split("T")[1][:5] for s in pending_slots]
                if confirmed_start not in slot_starts:
                    return {
                        "error": f"The time {confirmed_time} was not one of the available slots. "
                        f"Available slots: {[s['start'] for s in pending_slots]}. "
                        f"Please offer these to the user.",
                    }
            else:
                # Try to match by option number
                stripped = confirmed_time.strip()
                if stripped.isdigit():
                    idx = int(stripped) - 1
                    if 0 <= idx < len(pending_slots):
                        confirmed_time = pending_slots[idx]["start"]
                        logger.info(f"Resolved option {idx + 1} to {confirmed_time}")

                # If still not ISO, try to match by hour against available slots
                if "T" not in confirmed_time:
                    import re
                    hour_match = re.search(r'(\d{1,2})', confirmed_time)
                    if hour_match:
                        target_hour = int(hour_match.group(1))
                        if "pm" in confirmed_time.lower() and target_hour < 12:
                            target_hour += 12
                        elif target_hour < 7:
                            target_hour += 12  # assume PM for small numbers
                        for slot in pending_slots:
                            slot_hour = int(slot["start"].split("T")[1].split(":")[0])
                            if slot_hour == target_hour:
                                confirmed_time = slot["start"]
                                logger.info(f"Matched hour {target_hour} to slot {confirmed_time}")
                                break

                # If still unresolved, reject instead of blindly parsing
                if "T" not in confirmed_time:
                    return {
                        "error": f"Could not match '{confirmed_time}' to any available slot. "
                        f"Available slots: {[s['start'] for s in pending_slots]}. "
                        f"Please ask the user to pick one of these times.",
                    }

        # 1. Create escalation record
        escalation = await self._escalation_repo.create(
            session_id=session_id,
            reason=input["reason"],
            summary=input["summary"],
            assigned_to=settings.support_team_email,
            user_email=user_email,
        )

        result: dict[str, Any] = {
            "escalation_id": escalation.id,
        }

        # 2. Book calendar event if confirmed_time provided
        if preferred in ("calendar", "both") and confirmed_time:
            try:
                cal_result = await self._calendar.create_event(
                    summary="ClinicDesk Support Callback",
                    description=f"Support callback requested.\n\nIssue: {input['summary']}",
                    attendee_email=user_email or "",
                    start_time=confirmed_time,
                )
                await self._escalation_repo.set_calendar_event(
                    escalation.id, cal_result["event_id"]
                )
                result["callback"] = {
                    "status": "booked",
                    "scheduled_time": cal_result["scheduled_time"],
                    "event_id": cal_result["event_id"],
                    "meet_link": cal_result.get("meet_link", ""),
                }
            except Exception as e:
                logger.error(f"Calendar booking error: {e}")
                result["callback"] = {"status": "error", "message": str(e)}

        # 3. Send emails (always)
        callback_info = result.get("callback", {})
        try:
            # Notify all admin users
            from src.domain.entities.user import UserRole
            admin_users = await self._user_repo.list_by_role(UserRole.ADMIN)
            admin_emails = [u.email for u in admin_users] if admin_users else [settings.support_team_email]

            admin_body = (
                f"A new escalation has been created and requires attention.\n\n"
                f"Reason: {reason_label}\n"
                f"Escalation ID: {escalation.id}\n"
                f"User Email: {user_email or 'Not provided'}\n\n"
                f"--- Summary ---\n\n"
                f"{input['summary']}\n"
            )
            for admin_email in admin_emails:
                await self._email.send_email(
                    to_email=admin_email,
                    subject=f"[ClinicDesk] New Escalation — {reason_label}",
                    body=admin_body,
                )
            await self._escalation_repo.set_email_sent(escalation.id)

            if user_email:
                callback_section = ""
                if callback_info.get("status") == "booked":
                    meet_line = ""
                    if callback_info.get("meet_link"):
                        meet_line = f"Join the meeting: {callback_info['meet_link']}\n"
                    callback_section = (
                        f"\n--- Callback Details ---\n"
                        f"Scheduled: {callback_info['scheduled_time']}\n"
                        f"{meet_line}\n"
                    )

                await self._email.send_email(
                    to_email=user_email,
                    subject=f"[ClinicDesk] Your support request has been escalated (#{escalation.id})",
                    body=(
                        f"Hi,\n\n"
                        f"Your support request has been escalated to our team.\n\n"
                        f"Reason: {reason_label}\n"
                        f"Reference #: {escalation.id}\n\n"
                        f"Summary: {input['summary']}\n"
                        f"{callback_section}"
                        f"A member of our support team will be in touch shortly.\n\n"
                        f"— ClinicDesk Support"
                    ),
                )
            result["emails"] = "sent"
        except Exception as e:
            logger.error(f"Email sending error: {e}")
            result["emails"] = f"error: {e}"

        # 4. Admin notification + broadcast
        notif_title = f"New Escalation: {reason_label}"
        notif_message = input["summary"][:200]
        try:
            await self._escalation_repo._pool.execute(
                """INSERT INTO notifications (type, title, message, reference_id, reference_type)
                   VALUES ('escalation', $1, $2, $3, 'escalation')""",
                notif_title, notif_message, escalation.id,
            )
            from src.presentation.ws.admin import broadcast_to_admins
            await broadcast_to_admins({
                "type": "notification",
                "title": notif_title,
                "message": notif_message,
                "reference_id": escalation.id,
                "reference_type": "escalation",
            })
        except Exception as e:
            logger.error(f"Notification error: {e}")

        result["status"] = "complete"
        result["message"] = "Escalation created, emails sent, and callback booked (if requested). You can now confirm everything to the user."
        return result

    async def _tool_update_notes(
        self, input: dict[str, Any], session_id: UUID
    ) -> Any:
        session = await self._session_repo.get_by_id(session_id)
        if session:
            context = session.context
            context["notes"] = input["notes"]
            await self._session_repo.update_context(session_id, context)
        return {"status": "updated"}

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
