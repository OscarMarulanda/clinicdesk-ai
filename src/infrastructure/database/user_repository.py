import asyncpg

from src.domain.entities.user import User, UserRole
from src.domain.repositories.user_repository import UserRepositoryBase


class PostgresUserRepository(UserRepositoryBase):
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def get_by_id(self, user_id: int) -> User | None:
        row = await self._pool.fetchrow(
            "SELECT id, email, name, role, password_hash, created_at FROM users WHERE id = $1",
            user_id,
        )
        return self._row_to_user(row) if row else None

    async def get_by_email(self, email: str) -> User | None:
        row = await self._pool.fetchrow(
            "SELECT id, email, name, role, password_hash, created_at FROM users WHERE email = $1",
            email,
        )
        return self._row_to_user(row) if row else None

    async def create(
        self,
        email: str,
        name: str,
        password_hash: str,
        role: UserRole = UserRole.STAFF,
    ) -> User:
        row = await self._pool.fetchrow(
            """INSERT INTO users (email, name, password_hash, role)
               VALUES ($1, $2, $3, $4)
               RETURNING id, email, name, role, password_hash, created_at""",
            email,
            name,
            password_hash,
            role.value,
        )
        return self._row_to_user(row)

    async def list_all(self) -> list[User]:
        rows = await self._pool.fetch(
            "SELECT id, email, name, role, password_hash, created_at FROM users ORDER BY id"
        )
        return [self._row_to_user(row) for row in rows]

    async def list_by_role(self, role: UserRole) -> list[User]:
        rows = await self._pool.fetch(
            "SELECT id, email, name, role, password_hash, created_at FROM users WHERE role = $1 ORDER BY id",
            role.value,
        )
        return [self._row_to_user(row) for row in rows]

    @staticmethod
    def _row_to_user(row: asyncpg.Record) -> User:
        return User(
            id=row["id"],
            email=row["email"],
            name=row["name"],
            role=UserRole(row["role"]),
            password_hash=row["password_hash"],
            created_at=row["created_at"],
        )
