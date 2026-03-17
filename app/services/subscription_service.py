from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from app.core.security import ensure_utc, utc_now
from app.db.models import Plan, Subscription, SubscriptionStatus
from app.services.audit_service import record_audit_event


@dataclass(slots=True)
class SubscriptionSummary:
    status: str
    plan_name: str | None = None
    plan_code: str | None = None
    ends_at: datetime | None = None
    starts_at: datetime | None = None
    price_rub: Decimal | None = None

    @property
    def is_access_allowed(self) -> bool:
        return self.status in {SubscriptionStatus.ACTIVE.value, SubscriptionStatus.TRIAL.value}


class SubscriptionService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def list_available_plans(self) -> list[Plan]:
        async with self.session_factory() as session:
            result = await session.scalars(
                select(Plan).where(Plan.is_active.is_(True)).order_by(Plan.duration_days.asc())
            )
            return list(result)

    async def get_plan_by_code(self, code: str) -> Plan | None:
        async with self.session_factory() as session:
            return await session.scalar(select(Plan).where(Plan.code == code, Plan.is_active.is_(True)))

    async def get_subscription_summary(self, user_id: int) -> SubscriptionSummary:
        async with self.session_factory() as session:
            subscription = await session.scalar(
                select(Subscription)
                .where(Subscription.user_id == user_id)
                .options(selectinload(Subscription.plan))
                .order_by(desc(Subscription.ends_at), desc(Subscription.id))
                .limit(1)
            )
            if subscription is None:
                return SubscriptionSummary(status=SubscriptionStatus.INACTIVE.value)

            current_time = utc_now()
            if subscription.status in {SubscriptionStatus.ACTIVE.value, SubscriptionStatus.TRIAL.value}:
                if ensure_utc(subscription.ends_at) <= current_time:
                    subscription.status = SubscriptionStatus.EXPIRED.value
                    session.add(subscription)
                    await session.commit()

            return SubscriptionSummary(
                status=subscription.status,
                plan_name=subscription.plan.name,
                plan_code=subscription.plan.code,
                starts_at=subscription.starts_at,
                ends_at=subscription.ends_at,
                price_rub=subscription.plan.price_rub,
            )

    async def record_plan_intent(self, user_id: int, plan_code: str) -> Plan:
        async with self.session_factory() as session:
            plan = await session.scalar(select(Plan).where(Plan.code == plan_code, Plan.is_active.is_(True)))
            if plan is None:
                raise ValueError("Selected plan does not exist.")
            await record_audit_event(
                session,
                user_id=user_id,
                event_type="subscription.plan_selected",
                payload={"plan_code": plan.code},
            )
            await session.commit()
            return plan

    async def create_subscription(
        self,
        *,
        user_id: int,
        plan_code: str,
        status: str = SubscriptionStatus.ACTIVE.value,
        starts_at: datetime | None = None,
        ends_at: datetime | None = None,
        source: str = "local_mvp",
        replace_existing: bool = True,
    ) -> Subscription:
        async with self.session_factory() as session:
            plan = await session.scalar(select(Plan).where(Plan.code == plan_code))
            if plan is None:
                raise ValueError("Plan does not exist.")

            current_time = starts_at or utc_now()
            computed_ends_at = ends_at or current_time + timedelta(days=plan.duration_days)
            if replace_existing:
                existing_subscriptions = await session.scalars(
                    select(Subscription).where(
                        Subscription.user_id == user_id,
                        Subscription.status.in_(
                            [
                                SubscriptionStatus.ACTIVE.value,
                                SubscriptionStatus.TRIAL.value,
                                SubscriptionStatus.INACTIVE.value,
                            ]
                        ),
                    )
                )
                for existing_subscription in existing_subscriptions:
                    existing_subscription.status = SubscriptionStatus.CANCELED.value
                    session.add(existing_subscription)
            subscription = Subscription(
                user_id=user_id,
                plan_id=plan.id,
                status=status,
                starts_at=current_time,
                ends_at=computed_ends_at,
                source=source,
            )
            session.add(subscription)
            await session.flush()
            await record_audit_event(
                session,
                user_id=user_id,
                event_type="subscription.created",
                payload={"subscription_id": subscription.id, "status": status},
            )
            await session.commit()
            await session.refresh(subscription)
            return subscription
