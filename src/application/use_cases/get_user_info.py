from src.domain.entities.user import User
from src.domain.exceptions import EntityNotFoundError
from src.domain.repositories.user_repository import UserRepositoryBase


class GetUserInfoUseCase:
    def __init__(self, user_repo: UserRepositoryBase) -> None:
        self._user_repo = user_repo

    async def execute(self, user_id: int) -> dict:
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise EntityNotFoundError("User", user_id)
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role.value,
        }
