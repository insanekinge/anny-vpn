from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.keyboards.main_menu import build_main_menu_keyboard
from app.bot.texts.messages import HELP_MESSAGE


router = Router(name="help")


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    await message.answer(HELP_MESSAGE, reply_markup=build_main_menu_keyboard())
