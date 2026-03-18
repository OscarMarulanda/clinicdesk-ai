import asyncpg

from src.application.dto.analytics import AnalyticsResponse, CategoryCount, ReasonCount


class GetAnalyticsUseCase:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def execute(self, days: int = 30) -> AnalyticsResponse:
        async with self._pool.acquire() as conn:
            # Total and active sessions
            session_stats = await conn.fetchrow("""
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE status = 'active') AS active
                FROM sessions
                WHERE created_at >= NOW() - MAKE_INTERVAL(days => $1)
            """, days)

            total_sessions = session_stats["total"]
            active_sessions = session_stats["active"]

            # Escalation stats
            esc_stats = await conn.fetchrow("""
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE status = 'resolved') AS resolved
                FROM escalations
                WHERE created_at >= NOW() - MAKE_INTERVAL(days => $1)
            """, days)

            total_escalations = esc_stats["total"]
            resolved_escalations = esc_stats["resolved"]

            escalation_rate = (
                total_escalations / total_sessions if total_sessions > 0 else 0.0
            )
            resolution_rate = (
                resolved_escalations / total_escalations if total_escalations > 0 else 0.0
            )

            # Average messages per session
            avg_row = await conn.fetchrow("""
                SELECT AVG(jsonb_array_length(messages)) AS avg_msgs
                FROM sessions
                WHERE created_at >= NOW() - MAKE_INTERVAL(days => $1)
            """, days)
            avg_messages = float(avg_row["avg_msgs"]) if avg_row["avg_msgs"] else 0.0

            # Top categories (from knowledge base search patterns via session messages)
            # For now, use article categories as proxy
            top_cats = await conn.fetch("""
                SELECT category, COUNT(*) AS count
                FROM knowledge_articles
                GROUP BY category
                ORDER BY count DESC
                LIMIT 10
            """)

            # Escalation reasons
            esc_reasons = await conn.fetch("""
                SELECT reason, COUNT(*) AS count
                FROM escalations
                WHERE created_at >= NOW() - MAKE_INTERVAL(days => $1)
                GROUP BY reason
                ORDER BY count DESC
            """, days)

        return AnalyticsResponse(
            total_sessions=total_sessions,
            active_sessions=active_sessions,
            total_escalations=total_escalations,
            escalation_rate=round(escalation_rate, 3),
            resolved_escalations=resolved_escalations,
            resolution_rate=round(resolution_rate, 3),
            avg_messages_per_session=round(avg_messages, 1),
            top_categories=[
                CategoryCount(category=r["category"], count=r["count"])
                for r in top_cats
            ],
            escalation_reasons=[
                ReasonCount(reason=r["reason"], count=r["count"])
                for r in esc_reasons
            ],
            period_days=days,
        )
