from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Buy Subscription", callback_data="menu:buy")
    builder.button(text="My Subscription", callback_data="menu:subscription")
    builder.button(text="Get Access", callback_data="menu:access")
    builder.button(text="My Configs", callback_data="menu:configs")
    builder.button(text="Instructions", callback_data="menu:instructions")
    builder.button(text="Support", callback_data="menu:support")
    builder.button(text="About", callback_data="menu:about")
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()
