from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from app.bot.handlers.start import bootstrap_user_from_telegram
from app.bot.handlers.utils import send_screen
from app.bot.states.support import SupportRequestState
from app.bot.texts.messages import (
    SUPPORT_CREATED_MESSAGE,
    SUPPORT_PROMPT_MESSAGE,
    SUPPORT_VALIDATION_MESSAGE,
    format_support_contact_message,
)
from app.core.config import get_settings
from app.db.session import get_session_factory
from app.services.support_service import SupportService


router = Router(name="support")


def build_support_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Contact support", callback_data="support:contact")
    builder.button(text="Create request", callback_data="support:create")
    builder.button(text="Back", callback_data="nav:back")
    builder.button(text="Main Menu", callback_data="nav:main")
    builder.adjust(1, 1, 2)
    return builder.as_markup()


@router.callback_query(F.data == "menu:support")
async def handle_support(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await send_screen(callback, text="Поддержка AllyVPN.", reply_markup=build_support_keyboard())


@router.callback_query(F.data == "support:contact")
async def handle_support_contact(callback: CallbackQuery) -> None:
    settings = get_settings()
    await send_screen(callback, text=format_support_contact_message(settings), reply_markup=build_support_keyboard())


@router.callback_query(F.data == "support:create")
async def handle_support_create(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SupportRequestState.awaiting_message)
    await send_screen(callback, text=SUPPORT_PROMPT_MESSAGE, reply_markup=build_support_keyboard())


@router.message(SupportRequestState.awaiting_message)
async def handle_support_message(message: Message, state: FSMContext) -> None:
    user = await bootstrap_user_from_telegram(message.from_user)
    service = SupportService(get_session_factory())
    try:
        await service.create_request(user.id, message.text or "")
    except ValueError:
        await message.answer(SUPPORT_VALIDATION_MESSAGE, reply_markup=build_support_keyboard())
        return
    await state.clear()
    await message.answer(SUPPORT_CREATED_MESSAGE, reply_markup=build_support_keyboard())
