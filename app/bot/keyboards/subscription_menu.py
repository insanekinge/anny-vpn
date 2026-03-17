from __future__ import annotations

from collections.abc import Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.common import build_navigation_keyboard
from app.db.models import Plan


def build_plan_selection_keyboard(plans: Sequence[Plan]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for plan in plans:
        builder.button(text=f"{plan.name} - {plan.price_rub} RUB", callback_data=f"buy:plan:{plan.code}")
    builder.adjust(1)
    builder.attach(InlineKeyboardBuilder.from_markup(build_navigation_keyboard()))
    return builder.as_markup()


def build_subscription_empty_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Buy Subscription", callback_data="menu:buy")
    builder.button(text="Main Menu", callback_data="nav:main")
    builder.adjust(1, 1)
    return builder.as_markup()
