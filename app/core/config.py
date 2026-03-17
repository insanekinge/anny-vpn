from __future__ import annotations

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: str = Field(default="production", alias="APP_ENV")
    bot_token: SecretStr | None = Field(default=None, alias="BOT_TOKEN")
    bot_username: str = Field(default="@AllyVPNsbot", alias="BOT_USERNAME")
    database_url: str = Field(default="sqlite+aiosqlite:///./allyvpn.db", alias="DATABASE_URL")
    marzban_base_url: str | None = Field(default=None, alias="MARZBAN_BASE_URL")
    marzban_username: SecretStr | None = Field(default=None, alias="MARZBAN_USERNAME")
    marzban_password: SecretStr | None = Field(default=None, alias="MARZBAN_PASSWORD")
    marzban_verify_ssl: bool = Field(default=False, alias="MARZBAN_VERIFY_SSL")
    marzban_timeout: int = Field(default=15, alias="MARZBAN_TIMEOUT")
    support_username: str | None = Field(default=None, alias="SUPPORT_USERNAME")
    admin_telegram_ids_raw: str = Field(default="", alias="ADMIN_TELEGRAM_IDS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @property
    def is_local(self) -> bool:
        return self.app_env.lower() == "local"

    @property
    def bot_token_value(self) -> str | None:
        return self.bot_token.get_secret_value() if self.bot_token else None

    @property
    def marzban_username_value(self) -> str | None:
        return self.marzban_username.get_secret_value() if self.marzban_username else None

    @property
    def marzban_password_value(self) -> str | None:
        return self.marzban_password.get_secret_value() if self.marzban_password else None

    @property
    def admin_telegram_ids(self) -> set[int]:
        values = set()
        for raw_item in self.admin_telegram_ids_raw.split(","):
            cleaned = raw_item.strip()
            if not cleaned:
                continue
            values.add(int(cleaned))
        return values

    def require_bot_token(self) -> str:
        token = self.bot_token_value
        if not token:
            raise RuntimeError("BOT_TOKEN is required to run the Telegram bot.")
        return token

    def validate_runtime(self) -> None:
        missing = []
        if not self.bot_token_value:
            missing.append("BOT_TOKEN")
        if not self.marzban_base_url:
            missing.append("MARZBAN_BASE_URL")
        if not self.marzban_username_value:
            missing.append("MARZBAN_USERNAME")
        if not self.marzban_password_value:
            missing.append("MARZBAN_PASSWORD")
        if missing:
            raise RuntimeError(f"Missing required runtime settings: {', '.join(missing)}")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
