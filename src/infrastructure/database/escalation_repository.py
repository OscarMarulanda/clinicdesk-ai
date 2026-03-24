from uuid import UUID

import asyncpg

from src.domain.entities.escalation import Escalation, EscalationReason, EscalationStatus
from src.domain.repositories.escalation_repository import EscalationRepositoryBase


class PostgresEscalationRepository(EscalationRepositoryBase):
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def create(
        self,
        session_id: UUID,
        reason: str,
        summary: str,
        assigned_to: str | None = None,
        user_email: str | None = None,
    ) -> Escalation:
        row = await self._pool.fetchrow(
            """INSERT INTO escalations (session_id, reason, summary, assigned_to, user_email)
               VALUES ($1, $2, $3, $4, $5)
               RETURNING id, session_id, reason, summary, status, user_email, assigned_to,
                         calendar_event_id, email_sent_at, created_at, resolved_at""",
            session_id,
            reason,
            summary,
            assigned_to,
            user_email,
        )
        return self._row_to_escalation(row)

    async def get_by_id(self, escalation_id: int) -> Escalation | None:
        row = await self._pool.fetchrow(
            """SELECT id, session_id, reason, summary, status, user_email, assigned_to,
                      calendar_event_id, email_sent_at, created_at, resolved_at
               FROM escalations WHERE id = $1""",
            escalation_id,
        )
        return self._row_to_escalation(row) if row else None

    async def update_status(
        self,
        escalation_id: int,
        status: EscalationStatus,
        assigned_to: str | None = None,
    ) -> Escalation | None:
        resolved_clause = ", resolved_at = NOW()" if status == EscalationStatus.RESOLVED else ""

        if assigned_to is not None:
            row = await self._pool.fetchrow(
                f"""UPDATE escalations
                    SET status = $1, assigned_to = $2{resolved_clause}
                    WHERE id = $3
                    RETURNING id, session_id, reason, summary, status, user_email, assigned_to,
                              calendar_event_id, email_sent_at, created_at, resolved_at""",
                status.value,
                assigned_to,
                escalation_id,
            )
        else:
            row = await self._pool.fetchrow(
                f"""UPDATE escalations
                    SET status = $1{resolved_clause}
                    WHERE id = $2
                    RETURNING id, session_id, reason, summary, status, user_email, assigned_to,
                              calendar_event_id, email_sent_at, created_at, resolved_at""",
                status.value,
                escalation_id,
            )
        return self._row_to_escalation(row) if row else None

    async def set_calendar_event(self, escalation_id: int, event_id: str) -> None:
        await self._pool.execute(
            "UPDATE escalations SET calendar_event_id = $1 WHERE id = $2",
            event_id,
            escalation_id,
        )

    async def set_email_sent(self, escalation_id: int) -> None:
        await self._pool.execute(
            "UPDATE escalations SET email_sent_at = NOW() WHERE id = $1",
            escalation_id,
        )

    async def list_all(
        self,
        status: EscalationStatus | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Escalation], int]:
        where = ""
        params: list[object] = []

        if status is not None:
            where = "WHERE status = $1"
            params.append(status.value)

        count_row = await self._pool.fetchrow(
            f"SELECT COUNT(*) as total FROM escalations {where}", *params
        )
        total = count_row["total"] if count_row else 0

        offset = (page - 1) * per_page
        idx = len(params) + 1
        sql = f"""
            SELECT id, session_id, reason, summary, status, user_email, assigned_to,
                   calendar_event_id, email_sent_at, created_at, resolved_at
            FROM escalations {where}
            ORDER BY created_at DESC
            LIMIT ${idx} OFFSET ${idx + 1}
        """
        params.extend([per_page, offset])

        rows = await self._pool.fetch(sql, *params)
        escalations = [self._row_to_escalation(row) for row in rows]
        return escalations, total

    @staticmethod
    def _row_to_escalation(row: asyncpg.Record) -> Escalation:
        return Escalation(
            id=row["id"],
            session_id=row["session_id"],
            reason=EscalationReason(row["reason"]),
            summary=row["summary"],
            status=EscalationStatus(row["status"]),
            user_email=row.get("user_email"),
            assigned_to=row["assigned_to"],
            calendar_event_id=row["calendar_event_id"],
            email_sent_at=row["email_sent_at"],
            created_at=row["created_at"],
            resolved_at=row["resolved_at"],
        )
