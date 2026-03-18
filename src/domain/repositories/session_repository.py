from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.domain.entities.session import Session, SessionStatus


class SessionRepositoryBase(ABC):
    @abstractmethod
    async def create(
        self,
        user_id: int | None = None,
        channel: str = "chat",
    ) -> Session:
        ...

    @abstractmethod
    async def get_by_id(self, session_id: UUID) -> Session | None:
        ...

    @abstractmethod
    async def update_messages(self, session_id: UUID, messages: list[dict[str, Any]]) -> None:
        ...

    @abstractmethod
    async def update_context(self, session_id: UUID, context: dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def update_metadata(self, session_id: UUID, metadata: dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def update_status(self, session_id: UUID, status: SessionStatus) -> None:
        ...

    @abstractmethod
    async def list_all(
        self,
        status: SessionStatus | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Session], int]:
        ...

    @abstractmethod
    async def list_by_user(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Session], int]:
        ...
