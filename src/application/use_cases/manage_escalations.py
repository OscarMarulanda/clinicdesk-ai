from src.domain.entities.escalation import Escalation, EscalationStatus
from src.domain.exceptions import EntityNotFoundError
from src.domain.repositories.escalation_repository import EscalationRepositoryBase


class ManageEscalationsUseCase:
    def __init__(self, escalation_repo: EscalationRepositoryBase) -> None:
        self._escalation_repo = escalation_repo

    async def list_all(
        self,
        status: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Escalation], int]:
        st = EscalationStatus(status) if status else None
        return await self._escalation_repo.list_all(status=st, page=page, per_page=per_page)

    async def update_status(
        self,
        escalation_id: int,
        status: str,
        assigned_to: str | None = None,
    ) -> Escalation:
        escalation = await self._escalation_repo.update_status(
            escalation_id,
            EscalationStatus(status),
            assigned_to=assigned_to,
        )
        if escalation is None:
            raise EntityNotFoundError("Escalation", escalation_id)
        return escalation
