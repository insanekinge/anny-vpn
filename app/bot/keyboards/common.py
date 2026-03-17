from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_navigation_keyboard(
    *,
    include_back: bool = True,
    include_main: bool = True,
    back_callback: str = "nav:back",
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if include_back:
        builder.button(text="Back", callback_data=back_callback)
    if include_main:
        builder.button(text="Main Menu", callback_data="nav:main")
    builder.adjust(2)
    return builder.as_markup()
