from __future__ import annotations

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message


async def send_screen(
    event: Message | CallbackQuery,
    *,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    if isinstance(event, CallbackQuery):
        try:
            if event.message is not None:
                await event.message.edit_text(text=text, reply_markup=reply_markup)
            await event.answer()
        except TelegramBadRequest:
            if event.message is not None:
                await event.message.answer(text=text, reply_markup=reply_markup)
            await event.answer()
        return

    await event.answer(text=text, reply_markup=reply_markup)
