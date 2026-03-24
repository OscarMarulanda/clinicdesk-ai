from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class EscalationReason(str, Enum):
    KNOWLEDGE_GAP = "knowledge_gap"
    USER_FRUSTRATION = "user_frustration"
    OUT_OF_SCOPE = "out_of_scope"
    BILLING_DISPUTE = "billing_dispute"
    ACCOUNT_CHANGE = "account_change"


class EscalationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


@dataclass
class Escalation:
    id: int
    session_id: UUID
    reason: EscalationReason
    summary: str
    status: EscalationStatus
    user_email: str | None
    assigned_to: str | None
    calendar_event_id: str | None
    email_sent_at: datetime | None
    created_at: datetime
    resolved_at: datetime | None
