from __future__ import annotations

import socket

from aiogram.client.session.aiohttp import AiohttpSession


def build_telegram_session() -> AiohttpSession:
    session = AiohttpSession()
    # Some local Windows/DNS setups try IPv6 first for api.telegram.org and
    # then stall during SSL handshake. Force IPv4 for Telegram API requests.
    session._connector_init["family"] = socket.AF_INET
    return session
