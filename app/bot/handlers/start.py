from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from app.bot.handlers.utils import send_screen
from app.bot.keyboards.main_menu import build_main_menu_keyboard
from app.bot.texts.messages import MAIN_MENU_MESSAGE, WELCOME_MESSAGE
from app.db.session import get_session_factory
from app.services.user_service import UserService


router = Router(name="start")


async def bootstrap_user_from_telegram(telegram_user: object, session_factory=None):
    factory = session_factory or get_session_factory()
    service = UserService(factory)
    return await service.create_or_update_from_telegram(telegram_user)


async def render_main_menu(event: Message | CallbackQuery, *, welcome: bool = False) -> None:
    if hasattr(event, "from_user") and getattr(event, "from_user") is not None:
        await bootstrap_user_from_telegram(getattr(event, "from_user"))
    text = WELCOME_MESSAGE if welcome else MAIN_MENU_MESSAGE
    await send_screen(event, text=text, reply_markup=build_main_menu_keyboard())


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await render_main_menu(message, welcome=True)


@router.callback_query(F.data.in_({"nav:main", "nav:back"}))
async def handle_main_navigation(callback: CallbackQuery) -> None:
    await render_main_menu(callback)
