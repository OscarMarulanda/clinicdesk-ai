from datetime import datetime

from pydantic import BaseModel


class EscalationCreate(BaseModel):
    session_id: str
    reason: str
    summary: str
    preferred_action: str = "email"


class EscalationUpdateStatus(BaseModel):
    status: str
    assigned_to: str | None = None


class EscalationResponse(BaseModel):
    id: int
    session_id: str
    reason: str
    summary: str
    status: str
    assigned_to: str | None
    calendar_event_id: str | None
    email_sent_at: datetime | None
    created_at: datetime
    resolved_at: datetime | None


class EscalationListResponse(BaseModel):
    escalations: list[EscalationResponse]
    total: int
    page: int
    per_page: int
