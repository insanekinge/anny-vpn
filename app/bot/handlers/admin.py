from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.keyboards.main_menu import build_main_menu_keyboard
from app.db.models import SubscriptionStatus
from app.db.session import get_session_factory
from app.services.admin_service import AdminAccessError, AdminService
from app.services.subscription_service import SubscriptionService
from app.services.user_service import UserService


router = Router(name="admin")


def _build_admin_service() -> AdminService:
    session_factory = get_session_factory()
    return AdminService(
        user_service=UserService(session_factory),
        subscription_service=SubscriptionService(session_factory),
    )


@router.message(Command("whoami"))
async def handle_whoami(message: Message) -> None:
    await message.answer(
        f"Your Telegram ID: {message.from_user.id}",
        reply_markup=build_main_menu_keyboard(),
    )


@router.message(Command("grant_subscription"))
async def handle_grant_subscription(message: Message) -> None:
    parts = (message.text or "").split()
    if len(parts) not in {3, 4}:
        await message.answer(
            "Usage: /grant_subscription <telegram_id> <plan_code> [active|trial]",
            reply_markup=build_main_menu_keyboard(),
        )
        return

    _, target_telegram_id_raw, plan_code, *status_parts = parts
    try:
        target_telegram_id = int(target_telegram_id_raw)
    except ValueError:
        await message.answer("telegram_id must be an integer.", reply_markup=build_main_menu_keyboard())
        return

    status = status_parts[0] if status_parts else SubscriptionStatus.ACTIVE.value
    if status not in {SubscriptionStatus.ACTIVE.value, SubscriptionStatus.TRIAL.value}:
        await message.answer("Allowed statuses: active, trial.", reply_markup=build_main_menu_keyboard())
        return

    service = _build_admin_service()
    try:
        subscription = await service.grant_subscription(
            admin_telegram_id=message.from_user.id,
            target_telegram_id=target_telegram_id,
            plan_code=plan_code,
            status=status,
        )
    except AdminAccessError:
        await message.answer("Admin access denied.", reply_markup=build_main_menu_keyboard())
        return
    except ValueError as exc:
        await message.answer(str(exc), reply_markup=build_main_menu_keyboard())
        return

    await message.answer(
        f"Subscription granted: user={target_telegram_id}, plan={plan_code}, status={subscription.status}",
        reply_markup=build_main_menu_keyboard(),
    )
