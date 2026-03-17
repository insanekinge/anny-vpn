from __future__ import annotations

import re
from datetime import UTC, datetime


SUPPORT_MESSAGE_MAX_LENGTH = 2_000
CONTROL_CHARS_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
USERNAME_PATTERN = re.compile(r"[^a-zA-Z0-9_]")


def utc_now() -> datetime:
    return datetime.now(UTC)


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def build_marzban_username(telegram_id: int) -> str:
    base_value = f"ally_{telegram_id}"
    sanitized = USERNAME_PATTERN.sub("_", base_value)
    return sanitized[:64]


def sanitize_support_message(message_text: str) -> str:
    normalized = message_text.replace("\r\n", "\n").strip()
    normalized = CONTROL_CHARS_PATTERN.sub("", normalized)
    if not normalized:
        raise ValueError("Support request message cannot be empty.")
    if len(normalized) > SUPPORT_MESSAGE_MAX_LENGTH:
        normalized = normalized[:SUPPORT_MESSAGE_MAX_LENGTH].rstrip()
    return normalized
