from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID


class SessionStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"


@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    tool_calls: list[dict[str, Any]] | None = None
    token_count: int | None = None


@dataclass
class Session:
    id: UUID
    user_id: int | None
    channel: str
    status: SessionStatus
    context: dict[str, Any]
    messages: list[Message]
    created_at: datetime
    updated_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def update_context(self, key: str, value: Any) -> None:
        self.context[key] = value

    def close(self) -> None:
        self.status = SessionStatus.CLOSED
