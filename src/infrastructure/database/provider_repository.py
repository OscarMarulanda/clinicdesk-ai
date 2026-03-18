import asyncpg

from src.domain.entities.provider import Provider
from src.domain.repositories.provider_repository import ProviderRepositoryBase


class PostgresProviderRepository(ProviderRepositoryBase):
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def get_by_id(self, provider_id: int) -> Provider | None:
        row = await self._pool.fetchrow(
            "SELECT id, name, email, calendar_id, is_available, created_at FROM providers WHERE id = $1",
            provider_id,
        )
        return self._row_to_provider(row) if row else None

    async def get_available(self) -> list[Provider]:
        rows = await self._pool.fetch(
            """SELECT id, name, email, calendar_id, is_available, created_at
               FROM providers WHERE is_available = true ORDER BY id"""
        )
        return [self._row_to_provider(row) for row in rows]

    async def list_all(self) -> list[Provider]:
        rows = await self._pool.fetch(
            "SELECT id, name, email, calendar_id, is_available, created_at FROM providers ORDER BY id"
        )
        return [self._row_to_provider(row) for row in rows]

    @staticmethod
    def _row_to_provider(row: asyncpg.Record) -> Provider:
        return Provider(
            id=row["id"],
            email=row["email"],
            name=row["name"],
            calendar_id=row["calendar_id"],
            is_available=row["is_available"],
            created_at=row["created_at"],
        )
