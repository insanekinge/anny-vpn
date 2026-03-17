from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.security import utc_now
from app.db.models import User
from app.services.audit_service import record_audit_event


@dataclass(slots=True)
class TelegramUserDTO:
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None


class UserService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    @staticmethod
    def _coerce_telegram_user(telegram_user: Any) -> TelegramUserDTO:
        return TelegramUserDTO(
            id=int(getattr(telegram_user, "id")),
            username=getattr(telegram_user, "username", None),
            first_name=getattr(telegram_user, "first_name", None),
            last_name=getattr(telegram_user, "last_name", None),
            language_code=getattr(telegram_user, "language_code", None),
        )

    async def create_or_update_from_telegram(self, telegram_user: Any) -> User:
        payload = self._coerce_telegram_user(telegram_user)
        async with self.session_factory() as session:
            instance = await self._get_by_telegram_id(session, payload.id)
            if instance is None:
                instance = User(
                    telegram_id=payload.id,
                    username=payload.username,
                    first_name=payload.first_name,
                    last_name=payload.last_name,
                    language_code=payload.language_code,
                    is_active=True,
                    last_seen_at=utc_now(),
                )
                session.add(instance)
            else:
                instance.username = payload.username
                instance.first_name = payload.first_name
                instance.last_name = payload.last_name
                instance.language_code = payload.language_code
                instance.is_active = True
                instance.last_seen_at = utc_now()

            try:
                await session.flush()
            except IntegrityError:
                await session.rollback()
                instance = await self._get_by_telegram_id(session, payload.id)
                if instance is None:
                    raise
                instance.last_seen_at = utc_now()
                session.add(instance)
                await session.flush()

            await record_audit_event(
                session,
                user_id=instance.id,
                event_type="user.upserted",
                payload={"telegram_id": payload.id},
            )
            await session.commit()
            await session.refresh(instance)
            return instance

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        async with self.session_factory() as session:
            return await self._get_by_telegram_id(session, telegram_id)

    async def get_by_id(self, user_id: int) -> User | None:
        async with self.session_factory() as session:
            return await session.get(User, user_id)

    async def list_users(self, limit: int = 100) -> list[User]:
        async with self.session_factory() as session:
            result = await session.scalars(select(User).order_by(User.id.desc()).limit(limit))
            return list(result)

    @staticmethod
    async def _get_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
        return await session.scalar(select(User).where(User.telegram_id == telegram_id))
