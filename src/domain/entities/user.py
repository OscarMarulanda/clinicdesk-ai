from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    STAFF = "staff"
    ADMIN = "admin"


@dataclass
class User:
    id: int
    email: str
    name: str
    role: UserRole
    password_hash: str
    created_at: datetime

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
