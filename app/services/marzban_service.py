from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import Settings, get_settings
from app.core.security import build_marzban_username
from app.db.models import User
from app.integrations.marzban.client import MarzbanClient
from app.integrations.marzban.schemas import MarzbanUserPayload


@dataclass(slots=True)
class VpnAccessResult:
    marzban_username: str
    status: str
    subscription_url: str | None
    config_links: list[str]
    external_ref: str | None
    raw_payload: dict[str, Any]


@dataclass(slots=True)
class ConfigListResult:
    marzban_username: str
    subscription_url: str | None
    config_links: list[str]
    source: str


@dataclass(slots=True)
class SyncResult:
    marzban_username: str
    status: str
    synced: bool
    raw_payload: dict[str, Any]


class MarzbanGateway(Protocol):
    async def ensure_user_access(self, user_id: int) -> VpnAccessResult:
        ...

    async def get_user_configs(self, user_id: int) -> ConfigListResult:
        ...

    async def sync_user_access(self, user_id: int) -> SyncResult:
        ...


class MarzbanService(MarzbanGateway):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        *,
        settings: Settings | None = None,
        client: MarzbanClient | None = None,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings or get_settings()
        self.client = client or MarzbanClient(self.settings)

    async def ensure_user_access(self, user_id: int) -> VpnAccessResult:
        user = await self._get_user(user_id)
        marzban_username = build_marzban_username(user.telegram_id)
        remote_user = await self.client.get_user(marzban_username)

        if remote_user is None:
            remote_user = await self.client.create_user(
                MarzbanUserPayload(
                    username=marzban_username,
                    note=f"telegram_id={user.telegram_id}",
                    status="active",
                )
            )

        return self._normalize_access_result(marzban_username, remote_user)

    async def get_user_configs(self, user_id: int) -> ConfigListResult:
        user = await self._get_user(user_id)
        marzban_username = build_marzban_username(user.telegram_id)
        remote_user = await self.client.get_user(marzban_username)
        if remote_user is None:
            return ConfigListResult(
                marzban_username=marzban_username,
                subscription_url=None,
                config_links=[],
                source="empty",
            )

        result = self._normalize_access_result(marzban_username, remote_user)
        return ConfigListResult(
            marzban_username=result.marzban_username,
            subscription_url=result.subscription_url,
            config_links=result.config_links,
            source="marzban",
        )

    async def sync_user_access(self, user_id: int) -> SyncResult:
        user = await self._get_user(user_id)
        marzban_username = build_marzban_username(user.telegram_id)
        remote_user = await self.client.get_subscription_info(marzban_username)
        if remote_user is None:
            return SyncResult(
                marzban_username=marzban_username,
                status="missing",
                synced=False,
                raw_payload={},
            )
        result = self._normalize_access_result(marzban_username, remote_user)
        return SyncResult(
            marzban_username=result.marzban_username,
            status=result.status,
            synced=True,
            raw_payload=result.raw_payload,
        )

    async def _get_user(self, user_id: int) -> User:
        async with self.session_factory() as session:
            user = await session.scalar(select(User).where(User.id == user_id))
            if user is None:
                raise ValueError("User does not exist.")
            return user

    def _normalize_access_result(self, marzban_username: str, payload: dict[str, Any]) -> VpnAccessResult:
        links = payload.get("links") or []
        if isinstance(links, str):
            links = [links]
        subscription_url = payload.get("subscription_url")
        external_ref = str(payload.get("id")) if payload.get("id") is not None else None
        status = str(payload.get("status") or "active")
        return VpnAccessResult(
            marzban_username=marzban_username,
            status=status,
            subscription_url=subscription_url,
            config_links=[str(link) for link in links],
            external_ref=external_ref,
            raw_payload=payload,
        )
