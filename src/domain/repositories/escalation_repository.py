from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.escalation import Escalation, EscalationStatus


class EscalationRepositoryBase(ABC):
    @abstractmethod
    async def create(
        self,
        session_id: UUID,
        reason: str,
        summary: str,
        assigned_to: str | None = None,
    ) -> Escalation:
        ...

    @abstractmethod
    async def get_by_id(self, escalation_id: int) -> Escalation | None:
        ...

    @abstractmethod
    async def update_status(
        self,
        escalation_id: int,
        status: EscalationStatus,
        assigned_to: str | None = None,
    ) -> Escalation | None:
        ...

    @abstractmethod
    async def set_calendar_event(self, escalation_id: int, event_id: str) -> None:
        ...

    @abstractmethod
    async def set_email_sent(self, escalation_id: int) -> None:
        ...

    @abstractmethod
    async def list_all(
        self,
        status: EscalationStatus | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Escalation], int]:
        ...
