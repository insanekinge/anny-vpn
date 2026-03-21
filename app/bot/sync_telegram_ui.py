from __future__ import annotations

import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from app.bot.main import configure_miniapp_menu_button, set_bot_commands
from app.bot.telegram_session import build_telegram_session
from app.core.config import get_settings


async def sync_telegram_ui() -> None:
    settings = get_settings()
    token = settings.require_bot_token()
    if not settings.miniapp_url:
        raise RuntimeError("MINIAPP_URL is required to link the Telegram Mini App.")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=None),
        session=build_telegram_session(),
    )
    try:
        await set_bot_commands(bot)
        await configure_miniapp_menu_button(bot)
    finally:
        await bot.session.close()


def main() -> None:
    asyncio.run(sync_telegram_ui())


if __name__ == "__main__":
    main()
