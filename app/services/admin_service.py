from __future__ import annotations

from app.core.config import Settings, get_settings
from app.db.models import Subscription, SubscriptionStatus
from app.services.subscription_service import SubscriptionService
from app.services.user_service import UserService


class AdminAccessError(Exception):
    """Raised when a non-admin tries to use admin features."""


class AdminService:
    def __init__(
        self,
        user_service: UserService,
        subscription_service: SubscriptionService,
        *,
        settings: Settings | None = None,
    ) -> None:
        self.user_service = user_service
        self.subscription_service = subscription_service
        self.settings = settings or get_settings()

    def ensure_admin(self, telegram_id: int) -> None:
        if telegram_id not in self.settings.admin_telegram_ids:
            raise AdminAccessError("Telegram user is not allowed to perform admin actions.")

    async def grant_subscription(
        self,
        *,
        admin_telegram_id: int,
        target_telegram_id: int,
        plan_code: str,
        status: str = SubscriptionStatus.ACTIVE.value,
    ) -> Subscription:
        self.ensure_admin(admin_telegram_id)
        target_user = await self.user_service.get_by_telegram_id(target_telegram_id)
        if target_user is None:
            raise ValueError("Target user does not exist in local database. Ask them to send /start first.")
        return await self.subscription_service.create_subscription(
            user_id=target_user.id,
            plan_code=plan_code,
            status=status,
            source="admin_command",
            replace_existing=True,
        )
