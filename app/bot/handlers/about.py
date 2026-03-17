from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.handlers.utils import send_screen
from app.bot.keyboards.common import build_navigation_keyboard
from app.bot.texts.messages import ABOUT_MESSAGE


router = Router(name="about")


@router.callback_query(F.data == "menu:about")
async def handle_about(callback: CallbackQuery) -> None:
    await send_screen(callback, text=ABOUT_MESSAGE, reply_markup=build_navigation_keyboard())
