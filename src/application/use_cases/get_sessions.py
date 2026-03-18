from uuid import UUID

from src.domain.entities.session import Session, SessionStatus
from src.domain.exceptions import EntityNotFoundError
from src.domain.repositories.session_repository import SessionRepositoryBase


class GetSessionsUseCase:
    def __init__(self, session_repo: SessionRepositoryBase) -> None:
        self._session_repo = session_repo

    async def list_all(
        self,
        status: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Session], int]:
        st = SessionStatus(status) if status else None
        return await self._session_repo.list_all(status=st, page=page, per_page=per_page)

    async def list_by_user(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Session], int]:
        return await self._session_repo.list_by_user(user_id, page=page, per_page=per_page)

    async def get_detail(self, session_id: UUID) -> Session:
        session = await self._session_repo.get_by_id(session_id)
        if session is None:
            raise EntityNotFoundError("Session", session_id)
        return session
