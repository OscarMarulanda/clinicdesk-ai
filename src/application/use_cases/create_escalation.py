from uuid import UUID

from src.domain.entities.escalation import Escalation
from src.domain.repositories.escalation_repository import EscalationRepositoryBase
from src.infrastructure.config import settings


class CreateEscalationUseCase:
    def __init__(self, escalation_repo: EscalationRepositoryBase) -> None:
        self._escalation_repo = escalation_repo

    async def execute(
        self,
        session_id: UUID,
        reason: str,
        summary: str,
        assigned_to: str | None = None,
    ) -> Escalation:
        if assigned_to is None:
            assigned_to = settings.support_team_email
        return await self._escalation_repo.create(
            session_id=session_id,
            reason=reason,
            summary=summary,
            assigned_to=assigned_to,
        )
