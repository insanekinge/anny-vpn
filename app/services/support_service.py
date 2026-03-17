from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.security import sanitize_support_message
from app.db.models import SupportRequest, SupportRequestStatus
from app.services.audit_service import record_audit_event


class SupportService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def create_request(self, user_id: int, message_text: str) -> SupportRequest:
        sanitized_text = sanitize_support_message(message_text)
        async with self.session_factory() as session:
            request = SupportRequest(
                user_id=user_id,
                message_text=sanitized_text,
                status=SupportRequestStatus.OPEN.value,
            )
            session.add(request)
            await session.flush()
            await record_audit_event(
                session,
                user_id=user_id,
                event_type="support.request_created",
                payload={"support_request_id": request.id},
            )
            await session.commit()
            await session.refresh(request)
            return request
