"""Notification endpoints for admin dashboard."""

import json

from fastapi import APIRouter, Depends, Request

from src.presentation.middleware.auth import require_admin

router = APIRouter(prefix="/api/admin/notifications", tags=["notifications"])


@router.get("/count")
async def get_unread_count(
    request: Request,
    _admin: dict = Depends(require_admin),
):
    pool = request.app.state.db_pool
    row = await pool.fetchrow(
        "SELECT COUNT(*) as count FROM notifications WHERE is_read = false"
    )
    return {"unread": row["count"]}


@router.get("")
async def list_notifications(
    request: Request,
    _admin: dict = Depends(require_admin),
    limit: int = 20,
):
    pool = request.app.state.db_pool
    rows = await pool.fetch(
        """SELECT id, type, title, message, reference_id, reference_type,
                  is_read, created_at
           FROM notifications
           ORDER BY created_at DESC
           LIMIT $1""",
        limit,
    )
    return {
        "notifications": [
            {
                "id": r["id"],
                "type": r["type"],
                "title": r["title"],
                "message": r["message"],
                "reference_id": r["reference_id"],
                "reference_type": r["reference_type"],
                "is_read": r["is_read"],
                "created_at": r["created_at"].isoformat(),
            }
            for r in rows
        ]
    }


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    request: Request,
    _admin: dict = Depends(require_admin),
):
    pool = request.app.state.db_pool
    await pool.execute(
        "UPDATE notifications SET is_read = true WHERE id = $1", notification_id
    )
    return {"status": "ok"}


@router.post("/read-all")
async def mark_all_read(
    request: Request,
    _admin: dict = Depends(require_admin),
):
    pool = request.app.state.db_pool
    await pool.execute("UPDATE notifications SET is_read = true WHERE is_read = false")
    return {"status": "ok"}
