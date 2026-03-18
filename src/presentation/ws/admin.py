"""WebSocket hub for admin real-time notifications."""

import json
import logging
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

router = APIRouter()

# Connected admin WebSocket clients
_admin_connections: set[WebSocket] = set()


async def broadcast_to_admins(event: dict[str, Any]) -> None:
    """Send an event to all connected admin dashboards."""
    if not _admin_connections:
        return
    message = json.dumps(event, default=str)
    disconnected = set()
    for ws in _admin_connections:
        try:
            await ws.send_text(message)
        except Exception:
            disconnected.add(ws)
    _admin_connections.difference_update(disconnected)


@router.websocket("/ws/admin")
async def admin_websocket(websocket: WebSocket):
    await websocket.accept()
    _admin_connections.add(websocket)
    logger.info(f"Admin WebSocket connected. Total: {len(_admin_connections)}")

    try:
        while True:
            # Keep connection alive — client can send pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        _admin_connections.discard(websocket)
        logger.info(f"Admin WebSocket disconnected. Total: {len(_admin_connections)}")
