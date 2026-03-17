from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.handlers.start import bootstrap_user_from_telegram
from app.bot.handlers.utils import send_screen
from app.bot.keyboards.common import build_navigation_keyboard
from app.bot.keyboards.subscription_menu import (
    build_plan_selection_keyboard,
    build_subscription_empty_keyboard,
)
from app.bot.texts.messages import (
    format_plan_list_message,
    format_plan_selected_message,
    format_subscription_message,
    INVALID_PLAN_MESSAGE,
)
from app.db.session import get_session_factory
from app.services.subscription_service import SubscriptionService


router = Router(name="subscription")


@router.callback_query(F.data == "menu:buy")
async def handle_buy_subscription(callback: CallbackQuery) -> None:
    service = SubscriptionService(get_session_factory())
    plans = await service.list_available_plans()
    await send_screen(
        callback,
        text=format_plan_list_message(plans),
        reply_markup=build_plan_selection_keyboard(plans),
    )


@router.callback_query(F.data == "menu:subscription")
async def handle_my_subscription(callback: CallbackQuery) -> None:
    user = await bootstrap_user_from_telegram(callback.from_user)
    service = SubscriptionService(get_session_factory())
    summary = await service.get_subscription_summary(user.id)
    markup = build_navigation_keyboard()
    if summary.plan_name is None:
        markup = build_subscription_empty_keyboard()
    await send_screen(callback, text=format_subscription_message(summary), reply_markup=markup)


@router.callback_query(F.data.startswith("buy:plan:"))
async def handle_plan_selection(callback: CallbackQuery) -> None:
    user = await bootstrap_user_from_telegram(callback.from_user)
    plan_code = callback.data.split(":")[-1]
    service = SubscriptionService(get_session_factory())
    try:
        plan = await service.record_plan_intent(user.id, plan_code)
    except ValueError:
        await send_screen(
            callback,
            text=INVALID_PLAN_MESSAGE,
            reply_markup=build_navigation_keyboard(back_callback="menu:buy"),
        )
        return
    await send_screen(
        callback,
        text=format_plan_selected_message(plan.name),
        reply_markup=build_navigation_keyboard(),
    )
