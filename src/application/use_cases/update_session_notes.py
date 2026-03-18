from uuid import UUID

from src.domain.exceptions import EntityNotFoundError
from src.domain.repositories.session_repository import SessionRepositoryBase


class UpdateSessionNotesUseCase:
    def __init__(self, session_repo: SessionRepositoryBase) -> None:
        self._session_repo = session_repo

    async def execute(self, session_id: UUID, notes: str) -> None:
        session = await self._session_repo.get_by_id(session_id)
        if session is None:
            raise EntityNotFoundError("Session", session_id)
        context = session.context
        context["notes"] = notes
        await self._session_repo.update_context(session_id, context)
