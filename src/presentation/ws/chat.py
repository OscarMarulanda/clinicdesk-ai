import json
import logging
from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.application.use_cases.process_chat_message import ProcessChatMessageUseCase
from src.infrastructure.ai.claude_service import ClaudeAIService
from src.infrastructure.database.connection import get_pool
from src.infrastructure.database.escalation_repository import PostgresEscalationRepository
from src.infrastructure.database.knowledge_repository import PostgresKnowledgeRepository
from src.infrastructure.database.session_repository import PostgresSessionRepository
from src.infrastructure.database.user_repository import PostgresUserRepository

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()

    pool = await get_pool()
    session_repo = PostgresSessionRepository(pool)

    # Get query params
    session_id_str = websocket.query_params.get("session_id")
    user_id_str = websocket.query_params.get("user_id")

    user_id = int(user_id_str) if user_id_str else None

    # Create or resume session
    if session_id_str:
        try:
            session_id = UUID(session_id_str)
            session = await session_repo.get_by_id(session_id)
            if session is None:
                session = await session_repo.create(user_id=user_id)
                session_id = session.id
        except ValueError:
            session = await session_repo.create(user_id=user_id)
            session_id = session.id
    else:
        session = await session_repo.create(user_id=user_id)
        session_id = session.id

    # Build use case — pull services from app state
    ai_service = websocket.app.state.ai_service
    calendar_service = websocket.app.state.calendar_service
    email_service = websocket.app.state.email_service

    use_case = ProcessChatMessageUseCase(
        ai_service=ai_service,
        session_repo=session_repo,
        knowledge_repo=PostgresKnowledgeRepository(pool),
        escalation_repo=PostgresEscalationRepository(pool),
        user_repo=PostgresUserRepository(pool),
        calendar_service=calendar_service,
        email_service=email_service,
    )

    # Send session ID to client
    await websocket.send_json({
        "type": "session",
        "session_id": str(session_id),
    })

    try:
        while True:
            data = await websocket.receive_text()

            try:
                msg = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid message format",
                })
                continue

            if msg.get("type") != "message" or not msg.get("content"):
                await websocket.send_json({
                    "type": "error",
                    "message": "Message must have type 'message' and non-empty 'content'",
                })
                continue

            # Send typing indicator
            await websocket.send_json({"type": "typing", "status": True})

            try:
                result = await use_case.execute(
                    message=msg["content"],
                    session_id=session_id,
                    user_id=user_id,
                )

                await websocket.send_json({"type": "typing", "status": False})
                await websocket.send_json({
                    "type": "message",
                    "content": result["message"],
                    "session_id": result["session_id"],
                })
            except Exception as e:
                logger.error(f"Chat processing error: {e}", exc_info=True)
                await websocket.send_json({"type": "typing", "status": False})
                await websocket.send_json({
                    "type": "error",
                    "message": "Something went wrong. Please try again.",
                })

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: session={session_id}")
