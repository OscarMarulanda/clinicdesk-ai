from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from src.application.dto.session import (
    MessageResponse,
    SessionDetailResponse,
    SessionListResponse,
    SessionResponse,
)
from src.application.use_cases.get_sessions import GetSessionsUseCase
from src.domain.exceptions import EntityNotFoundError
from src.presentation.dependencies import get_sessions_use_case
from src.presentation.middleware.auth import get_current_user, require_admin

router = APIRouter(tags=["sessions"])


@router.get("/api/admin/sessions", response_model=SessionListResponse)
async def list_sessions(
    status: str | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    use_case: GetSessionsUseCase = Depends(get_sessions_use_case),
    _admin: dict = Depends(require_admin),
):
    sessions, total = await use_case.list_all(
        status=status, page=page, per_page=per_page
    )
    return SessionListResponse(
        sessions=[
            SessionResponse(
                id=str(s.id),
                user_id=s.user_id,
                status=s.status.value,
                message_count=len(s.messages),
                created_at=s.created_at,
                updated_at=s.updated_at,
            )
            for s in sessions
        ],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/api/admin/sessions/{session_id}", response_model=SessionDetailResponse)
async def get_session(
    session_id: UUID,
    use_case: GetSessionsUseCase = Depends(get_sessions_use_case),
    _admin: dict = Depends(require_admin),
):
    try:
        session = await use_case.get_detail(session_id)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionDetailResponse(
        id=str(session.id),
        user_id=session.user_id,
        status=session.status.value,
        context=session.context,
        messages=[
            MessageResponse(
                role=m.role,
                content=m.content,
                timestamp=m.timestamp,
                tool_calls=m.tool_calls,
                token_count=m.token_count,
            )
            for m in session.messages
        ],
        metadata=session.metadata,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )


# Staff-accessible endpoints
@router.get("/api/sessions/me", response_model=SessionListResponse)
async def list_my_sessions(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    use_case: GetSessionsUseCase = Depends(get_sessions_use_case),
    current_user: dict = Depends(get_current_user),
):
    sessions, total = await use_case.list_by_user(
        user_id=current_user["user_id"], page=page, per_page=per_page
    )
    return SessionListResponse(
        sessions=[
            SessionResponse(
                id=str(s.id),
                user_id=s.user_id,
                status=s.status.value,
                message_count=len(s.messages),
                created_at=s.created_at,
                updated_at=s.updated_at,
            )
            for s in sessions
        ],
        total=total,
        page=page,
        per_page=per_page,
    )
