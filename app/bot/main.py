from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, MenuButtonWebApp, WebAppInfo

from app.bot.handlers.about import router as about_router
from app.bot.handlers.access import router as access_router
from app.bot.handlers.admin import router as admin_router
from app.bot.handlers.configs import router as configs_router
from app.bot.handlers.help import router as help_router
from app.bot.handlers.menu import router as menu_router
from app.bot.handlers.start import router as start_router
from app.bot.handlers.subscription import router as subscription_router
from app.bot.handlers.support import router as support_router
from app.bot.telegram_session import build_telegram_session
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import init_database


LOGGER = logging.getLogger(__name__)


def build_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(admin_router)
    dispatcher.include_router(start_router)
    dispatcher.include_router(help_router)
    dispatcher.include_router(menu_router)
    dispatcher.include_router(subscription_router)
    dispatcher.include_router(access_router)
    dispatcher.include_router(configs_router)
    dispatcher.include_router(support_router)
    dispatcher.include_router(about_router)
    return dispatcher


async def set_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск AllyVPN"),
            BotCommand(command="menu", description="Открыть главное меню"),
            BotCommand(command="help", description="Помощь"),
        ]
    )


async def configure_miniapp_menu_button(bot: Bot) -> None:
    settings = get_settings()
    if not settings.miniapp_url:
        LOGGER.info("MINIAPP_URL is not configured; Telegram Mini App menu button was skipped.")
        return

    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="AllyVPN Mini",
            web_app=WebAppInfo(url=settings.miniapp_url),
        )
    )
    LOGGER.info("Telegram Mini App menu button configured for %s.", settings.miniapp_url)


async def run_bot() -> None:
    settings = get_settings()
    settings.validate_runtime()
    configure_logging(settings)
    await init_database(settings)

    bot = Bot(
        token=settings.require_bot_token(),
        default=DefaultBotProperties(parse_mode=None),
        session=build_telegram_session(),
    )
    dispatcher = build_dispatcher()

    await set_bot_commands(bot)
    await configure_miniapp_menu_button(bot)
    LOGGER.info("Starting AllyVPN bot in polling mode.")
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


def main() -> None:
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()
