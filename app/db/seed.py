from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import Plan


DEFAULT_PLANS = (
    {"code": "m1", "name": "1 month", "duration_days": 30, "price_rub": Decimal("299.00")},
    {"code": "m3", "name": "3 months", "duration_days": 90, "price_rub": Decimal("799.00")},
    {"code": "m12", "name": "12 months", "duration_days": 365, "price_rub": Decimal("2490.00")},
)


async def seed_plans(session: AsyncSession) -> None:
    existing_codes = set(await session.scalars(select(Plan.code)))
    for plan_data in DEFAULT_PLANS:
        if plan_data["code"] in existing_codes:
            continue
        session.add(Plan(**plan_data))


async def ensure_seed_data(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async with session_factory() as session:
        await seed_plans(session)
        await session.commit()
