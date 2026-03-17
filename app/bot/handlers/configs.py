from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.handlers.start import bootstrap_user_from_telegram
from app.bot.handlers.utils import send_screen
from app.bot.texts.messages import format_configs_message
from app.db.session import get_session_factory
from app.services.config_service import ConfigService


router = Router(name="configs")


def build_configs_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Refresh", callback_data="configs:refresh")
    builder.button(text="Back", callback_data="nav:back")
    builder.button(text="Main Menu", callback_data="nav:main")
    builder.adjust(2, 1)
    return builder.as_markup()


@router.callback_query(F.data == "menu:configs")
async def handle_configs(callback: CallbackQuery) -> None:
    user = await bootstrap_user_from_telegram(callback.from_user)
    service = ConfigService(get_session_factory())
    result = await service.get_user_configs(user.id)
    await send_screen(callback, text=format_configs_message(result), reply_markup=build_configs_keyboard())


@router.callback_query(F.data == "configs:refresh")
async def handle_configs_refresh(callback: CallbackQuery) -> None:
    user = await bootstrap_user_from_telegram(callback.from_user)
    service = ConfigService(get_session_factory())
    result = await service.get_user_configs(user.id, refresh_remote=True)
    await send_screen(callback, text=format_configs_message(result), reply_markup=build_configs_keyboard())
