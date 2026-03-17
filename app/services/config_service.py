from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import VpnAccess
from app.services.access_service import AccessService
from app.services.marzban_service import ConfigListResult, MarzbanGateway, MarzbanService


@dataclass(slots=True)
class LocalConfigItem:
    label: str
    value: str


class ConfigService:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        *,
        access_service: AccessService | None = None,
        marzban_gateway: MarzbanGateway | None = None,
    ) -> None:
        self.session_factory = session_factory
        self.marzban_gateway = marzban_gateway or MarzbanService(session_factory)
        self.access_service = access_service or AccessService(
            session_factory,
            marzban_gateway=self.marzban_gateway,
        )

    async def get_user_configs(self, user_id: int, *, refresh_remote: bool = False) -> ConfigListResult:
        if refresh_remote:
            await self.access_service.sync_user_access(user_id)
            remote_result = await self.marzban_gateway.get_user_configs(user_id)
            await self._persist_remote_configs(user_id, remote_result)

        async with self.session_factory() as session:
            access = await session.scalar(select(VpnAccess).where(VpnAccess.user_id == user_id))
            if access is None:
                return ConfigListResult(
                    marzban_username="",
                    subscription_url=None,
                    config_links=[],
                    source="empty",
                )

            raw_json = access.raw_config_json or {}
            links = raw_json.get("links") or []
            return ConfigListResult(
                marzban_username=access.marzban_username,
                subscription_url=access.subscription_url,
                config_links=[str(link) for link in links],
                source="local",
            )

    async def _persist_remote_configs(self, user_id: int, remote_result: ConfigListResult) -> None:
        async with self.session_factory() as session:
            access = await session.scalar(select(VpnAccess).where(VpnAccess.user_id == user_id))
            if access is None:
                return
            access.subscription_url = remote_result.subscription_url
            access.raw_config_json = {"links": remote_result.config_links}
            session.add(access)
            await session.commit()
