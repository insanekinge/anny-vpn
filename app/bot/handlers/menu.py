from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.handlers.start import render_main_menu
from app.bot.handlers.utils import send_screen
from app.bot.keyboards.common import build_navigation_keyboard
from app.bot.texts.messages import INSTRUCTIONS_MESSAGE


router = Router(name="menu")


@router.message(Command("menu"))
async def handle_menu(message: Message) -> None:
    await render_main_menu(message)


@router.callback_query(F.data == "menu:instructions")
async def handle_instructions(callback: CallbackQuery) -> None:
    await send_screen(callback, text=INSTRUCTIONS_MESSAGE, reply_markup=build_navigation_keyboard())
