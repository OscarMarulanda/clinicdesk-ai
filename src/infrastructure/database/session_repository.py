import json
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

import asyncpg

from src.domain.entities.session import Message, Session, SessionStatus
from src.domain.repositories.session_repository import SessionRepositoryBase


class PostgresSessionRepository(SessionRepositoryBase):
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create(
        self,
        user_id: int | None = None,
        channel: str = "chat",
    ) -> Session:
        row = await self._pool.fetchrow(
            """INSERT INTO sessions (user_id, channel)
               VALUES ($1, $2)
               RETURNING id, user_id, channel, status, context, messages,
                         created_at, updated_at, metadata""",
            user_id,
            channel,
        )
        return self._row_to_session(row)

    async def get_by_id(self, session_id: UUID) -> Session | None:
        row = await self._pool.fetchrow(
            """SELECT id, user_id, channel, status, context, messages,
                      created_at, updated_at, metadata
               FROM sessions WHERE id = $1""",
            session_id,
        )
        return self._row_to_session(row) if row else None

    async def update_messages(self, session_id: UUID, messages: list[dict[str, Any]]) -> None:
        await self._pool.execute(
            "UPDATE sessions SET messages = $1::jsonb, updated_at = NOW() WHERE id = $2",
            json.dumps(messages, default=str),
            session_id,
        )

    async def update_context(self, session_id: UUID, context: dict[str, Any]) -> None:
        await self._pool.execute(
            "UPDATE sessions SET context = $1::jsonb, updated_at = NOW() WHERE id = $2",
            json.dumps(context, default=str),
            session_id,
        )

    async def update_metadata(self, session_id: UUID, metadata: dict[str, Any]) -> None:
        await self._pool.execute(
            "UPDATE sessions SET metadata = $1::jsonb, updated_at = NOW() WHERE id = $2",
            json.dumps(metadata, default=str),
            session_id,
        )

    async def update_status(self, session_id: UUID, status: SessionStatus) -> None:
        await self._pool.execute(
            "UPDATE sessions SET status = $1, updated_at = NOW() WHERE id = $2",
            status.value,
            session_id,
        )

    async def list_all(
        self,
        status: SessionStatus | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Session], int]:
        where = ""
        params: list[object] = []

        if status is not None:
            where = "WHERE status = $1"
            params.append(status.value)

        count_row = await self._pool.fetchrow(
            f"SELECT COUNT(*) as total FROM sessions {where}", *params
        )
        total = count_row["total"] if count_row else 0

        offset = (page - 1) * per_page
        idx = len(params) + 1
        sql = f"""
            SELECT id, user_id, channel, status, context, messages,
                   created_at, updated_at, metadata
            FROM sessions {where}
            ORDER BY created_at DESC
            LIMIT ${idx} OFFSET ${idx + 1}
        """
        params.extend([per_page, offset])

        rows = await self._pool.fetch(sql, *params)
        sessions = [self._row_to_session(row) for row in rows]
        return sessions, total

    async def list_by_user(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Session], int]:
        count_row = await self._pool.fetchrow(
            "SELECT COUNT(*) as total FROM sessions WHERE user_id = $1", user_id
        )
        total = count_row["total"] if count_row else 0

        offset = (page - 1) * per_page
        rows = await self._pool.fetch(
            """SELECT id, user_id, channel, status, context, messages,
                      created_at, updated_at, metadata
               FROM sessions WHERE user_id = $1
               ORDER BY created_at DESC LIMIT $2 OFFSET $3""",
            user_id,
            per_page,
            offset,
        )
        sessions = [self._row_to_session(row) for row in rows]
        return sessions, total

    @staticmethod
    def _row_to_session(row: asyncpg.Record) -> Session:
        messages_data = json.loads(row["messages"]) if isinstance(row["messages"], str) else row["messages"]
        messages = [
            Message(
                role=m["role"],
                content=m["content"],
                timestamp=datetime.fromisoformat(m["timestamp"]) if isinstance(m["timestamp"], str) else m["timestamp"],
                tool_calls=m.get("tool_calls"),
                token_count=m.get("token_count"),
            )
            for m in (messages_data or [])
        ]
        context = json.loads(row["context"]) if isinstance(row["context"], str) else (row["context"] or {})
        metadata = json.loads(row["metadata"]) if isinstance(row["metadata"], str) else (row["metadata"] or {})

        return Session(
            id=row["id"],
            user_id=row["user_id"],
            channel=row["channel"],
            status=SessionStatus(row["status"]),
            context=context,
            messages=messages,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            metadata=metadata,
        )
