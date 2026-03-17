from __future__ import annotations

from fastapi import APIRouter

from app.db.session import get_session_factory
from app.services.user_service import UserService


router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/users")
async def debug_users() -> list[dict[str, object]]:
    users = await UserService(get_session_factory()).list_users(limit=100)
    return [
        {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
            "first_name": user.first_name,
            "is_active": user.is_active,
        }
        for user in users
    ]
