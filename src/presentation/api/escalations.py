from fastapi import APIRouter, Depends, HTTPException, Query

from src.application.dto.escalation import (
    EscalationListResponse,
    EscalationResponse,
    EscalationUpdateStatus,
)
from src.application.use_cases.manage_escalations import ManageEscalationsUseCase
from src.domain.exceptions import EntityNotFoundError
from src.presentation.dependencies import get_manage_escalations_use_case
from src.presentation.middleware.auth import require_admin

router = APIRouter(prefix="/api/admin/escalations", tags=["escalations"])


@router.get("", response_model=EscalationListResponse)
async def list_escalations(
    status: str | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    use_case: ManageEscalationsUseCase = Depends(get_manage_escalations_use_case),
    _admin: dict = Depends(require_admin),
):
    escalations, total = await use_case.list_all(
        status=status, page=page, per_page=per_page
    )
    return EscalationListResponse(
        escalations=[
            EscalationResponse(
                id=e.id,
                session_id=str(e.session_id),
                reason=e.reason.value,
                summary=e.summary,
                status=e.status.value,
                assigned_to=e.assigned_to,
                calendar_event_id=e.calendar_event_id,
                email_sent_at=e.email_sent_at,
                created_at=e.created_at,
                resolved_at=e.resolved_at,
            )
            for e in escalations
        ],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.put("/{escalation_id}", response_model=EscalationResponse)
async def update_escalation(
    escalation_id: int,
    body: EscalationUpdateStatus,
    use_case: ManageEscalationsUseCase = Depends(get_manage_escalations_use_case),
    _admin: dict = Depends(require_admin),
):
    try:
        escalation = await use_case.update_status(
            escalation_id,
            status=body.status,
            assigned_to=body.assigned_to,
        )
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Escalation not found")
    return EscalationResponse(
        id=escalation.id,
        session_id=str(escalation.session_id),
        reason=escalation.reason.value,
        summary=escalation.summary,
        status=escalation.status.value,
        assigned_to=escalation.assigned_to,
        calendar_event_id=escalation.calendar_event_id,
        email_sent_at=escalation.email_sent_at,
        created_at=escalation.created_at,
        resolved_at=escalation.resolved_at,
    )
