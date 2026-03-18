from datetime import datetime
from typing import Any

from pydantic import BaseModel


class MessageResponse(BaseModel):
    role: str
    content: str
    timestamp: datetime
    tool_calls: list[str] | None = None
    token_count: int | None = None


class SessionResponse(BaseModel):
    id: str
    user_id: int | None
    status: str
    message_count: int
    created_at: datetime
    updated_at: datetime


class SessionDetailResponse(BaseModel):
    id: str
    user_id: int | None
    status: str
    context: dict[str, Any]
    messages: list[MessageResponse]
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class SessionListResponse(BaseModel):
    sessions: list[SessionResponse]
    total: int
    page: int
    per_page: int
