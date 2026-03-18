from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Provider:
    id: int
    name: str
    email: str
    calendar_id: str | None
    is_available: bool
    created_at: datetime
