from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.security import utc_now
from app.db.models import User, VpnAccess, VpnAccessStatus
from app.services.audit_service import record_audit_event
from app.services.marzban_service import MarzbanGateway, MarzbanService, VpnAccessResult
from app.services.subscription_service import SubscriptionService


class AccessProvisioningError(Exception):
    """Raised when VPN access cannot be provisioned."""


class AccessService:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        *,
        subscription_service: SubscriptionService | None = None,
        marzban_gateway: MarzbanGateway | None = None,
    ) -> None:
        self.session_factory = session_factory
        self.subscription_service = subscription_service or SubscriptionService(session_factory)
        self.marzban_gateway = marzban_gateway or MarzbanService(session_factory)

    async def ensure_user_access(self, user_id: int) -> VpnAccessResult:
        summary = await self.subscription_service.get_subscription_summary(user_id)
        if not summary.is_access_allowed:
            raise AccessProvisioningError("Active subscription is required before issuing VPN access.")

        result = await self.marzban_gateway.ensure_user_access(user_id)

        async with self.session_factory() as session:
            await self._ensure_user_exists(session, user_id)
            access = await session.scalar(select(VpnAccess).where(VpnAccess.user_id == user_id))
            if access is None:
                access = VpnAccess(
                    user_id=user_id,
                    marzban_username=result.marzban_username,
                    status=VpnAccessStatus.ACTIVE.value,
                )
                session.add(access)

            access.marzban_username = result.marzban_username
            access.external_ref = result.external_ref
            access.subscription_url = result.subscription_url
            access.raw_config_json = {
                "links": result.config_links,
                "payload": result.raw_payload,
            }
            access.status = result.status
            access.last_synced_at = utc_now()

            await record_audit_event(
                session,
                user_id=user_id,
                event_type="access.ensured",
                payload={"marzban_username": result.marzban_username, "status": result.status},
            )
            await session.commit()
        return result

    async def sync_user_access(self, user_id: int) -> VpnAccess | None:
        sync_result = await self.marzban_gateway.sync_user_access(user_id)
        if not sync_result.synced:
            return None

        async with self.session_factory() as session:
            access = await session.scalar(select(VpnAccess).where(VpnAccess.user_id == user_id))
            if access is None:
                return None
            access.status = sync_result.status
            access.last_synced_at = utc_now()
            current_payload = access.raw_config_json or {}
            current_payload["payload"] = sync_result.raw_payload
            access.raw_config_json = current_payload
            session.add(access)
            await record_audit_event(
                session,
                user_id=user_id,
                event_type="access.synced",
                payload={"marzban_username": sync_result.marzban_username},
            )
            await session.commit()
            await session.refresh(access)
            return access

    @staticmethod
    async def _ensure_user_exists(session: AsyncSession, user_id: int) -> None:
        user = await session.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise ValueError("User does not exist.")
