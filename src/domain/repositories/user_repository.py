from abc import ABC, abstractmethod

from src.domain.entities.user import User, UserRole


class UserRepositoryBase(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        ...

    @abstractmethod
    async def create(
        self,
        email: str,
        name: str,
        password_hash: str,
        role: UserRole = UserRole.STAFF,
    ) -> User:
        ...

    @abstractmethod
    async def list_all(self) -> list[User]:
        ...
