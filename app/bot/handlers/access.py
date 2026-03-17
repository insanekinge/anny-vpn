from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.handlers.start import bootstrap_user_from_telegram
from app.bot.handlers.utils import send_screen
from app.bot.keyboards.common import build_navigation_keyboard
from app.bot.keyboards.subscription_menu import build_subscription_empty_keyboard
from app.bot.texts.messages import (
    ACCESS_REQUIRES_SUBSCRIPTION_MESSAGE,
    ACCESS_SUCCESS_MESSAGE,
    GENERIC_ERROR_MESSAGE,
    MARZBAN_UNAVAILABLE_MESSAGE,
)
from app.db.session import get_session_factory
from app.integrations.marzban.exceptions import MarzbanError
from app.services.access_service import AccessProvisioningError, AccessService


LOGGER = logging.getLogger(__name__)
router = Router(name="access")


@router.callback_query(F.data == "menu:access")
async def handle_get_access(callback: CallbackQuery) -> None:
    user = await bootstrap_user_from_telegram(callback.from_user)
    service = AccessService(get_session_factory())
    try:
        await service.ensure_user_access(user.id)
    except AccessProvisioningError:
        await send_screen(
            callback,
            text=ACCESS_REQUIRES_SUBSCRIPTION_MESSAGE,
            reply_markup=build_subscription_empty_keyboard(),
        )
        return
    except MarzbanError:
        await send_screen(callback, text=MARZBAN_UNAVAILABLE_MESSAGE, reply_markup=build_navigation_keyboard())
        return
    except Exception:
        LOGGER.exception("Unexpected access provisioning error.")
        await send_screen(callback, text=GENERIC_ERROR_MESSAGE, reply_markup=build_navigation_keyboard())
        return

    await send_screen(
        callback,
        text=ACCESS_SUCCESS_MESSAGE,
        reply_markup=build_navigation_keyboard(back_callback="menu:configs"),
    )
