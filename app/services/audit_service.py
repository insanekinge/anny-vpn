from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AuditEvent


async def record_audit_event(
    session: AsyncSession,
    *,
    event_type: str,
    user_id: int | None = None,
    payload: dict[str, Any] | None = None,
) -> None:
    session.add(
        AuditEvent(
            user_id=user_id,
            event_type=event_type,
            payload_json=payload,
        )
    )
