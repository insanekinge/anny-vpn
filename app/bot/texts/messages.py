from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal

from app.core.config import Settings
from app.core.security import ensure_utc
from app.services.marzban_service import ConfigListResult
from app.services.subscription_service import SubscriptionSummary


WELCOME_MESSAGE = (
    "Добро пожаловать в AllyVPN.\n"
    "Управляйте подпиской, доступом и конфигами прямо в Telegram."
)

HELP_MESSAGE = (
    "Команды AllyVPN:\n"
    "/start - запуск и регистрация\n"
    "/menu - главное меню\n"
    "/help - краткая справка\n"
    "/whoami - показать ваш Telegram ID\n\n"
    "Бот: @AllyVPNsbot"
)

MAIN_MENU_MESSAGE = "Главное меню AllyVPN."

NO_SUBSCRIPTION_MESSAGE = "У вас пока нет активной подписки."
PAYMENT_PLACEHOLDER_MESSAGE = "Интеграция оплаты будет подключена на следующем этапе."
ACCESS_SUCCESS_MESSAGE = "Доступ создан. Конфиги готовы к просмотру."
ACCESS_REQUIRES_SUBSCRIPTION_MESSAGE = "Для выдачи доступа нужна активная подписка."
CONFIGS_EMPTY_MESSAGE = "Конфиги пока не готовы. Сначала создайте доступ."
SUPPORT_CREATED_MESSAGE = "Запрос в поддержку сохранён. Мы свяжемся с вами позже."
SUPPORT_PROMPT_MESSAGE = "Отправьте следующим сообщением описание проблемы. Сообщение будет сохранено локально."
INSTRUCTIONS_MESSAGE = (
    "Как это работает:\n"
    "1. Выберите план подписки.\n"
    "2. После активации нажмите Get Access.\n"
    "3. Конфиги появятся в разделе My Configs.\n\n"
    "Mini App и Android-клиент будут добавлены позже."
)
ABOUT_MESSAGE = (
    "AllyVPN\n"
    "Текущий этап: Telegram bot MVP.\n\n"
    "Следующие шаги:\n"
    "- платежи\n"
    "- Telegram Mini App\n"
    "- Android app"
)

GENERIC_ERROR_MESSAGE = "Операция временно недоступна. Попробуйте позже."
MARZBAN_UNAVAILABLE_MESSAGE = "Сервис доступа временно недоступен. Попробуйте позже."
INVALID_PLAN_MESSAGE = "Выбранный план недоступен. Попробуйте снова."
SUPPORT_VALIDATION_MESSAGE = "Сообщение пустое или слишком короткое. Опишите проблему одним следующим сообщением."


def format_plan_list_message(plans: Sequence[object]) -> str:
    lines = ["Доступные планы:"]
    for plan in plans:
        lines.append(f"- {plan.name}: {plan.duration_days} дней / {plan.price_rub} RUB")
    return "\n".join(lines)


def format_subscription_message(summary: SubscriptionSummary) -> str:
    if summary.plan_name is None:
        return NO_SUBSCRIPTION_MESSAGE

    date_text = format_datetime(summary.ends_at)
    price_text = format_price(summary.price_rub)
    return (
        f"Статус: {summary.status}\n"
        f"План: {summary.plan_name}\n"
        f"Стоимость: {price_text}\n"
        f"Активна до: {date_text}"
    )


def format_configs_message(result: ConfigListResult) -> str:
    if not result.config_links and not result.subscription_url:
        return CONFIGS_EMPTY_MESSAGE

    lines = [f"Пользователь: {result.marzban_username or 'not-ready'}"]
    if result.subscription_url:
        lines.append(f"Subscription URL: {result.subscription_url}")
    if result.config_links:
        lines.append("Конфиги:")
        for link in result.config_links:
            lines.append(link)
    return "\n".join(lines)


def format_support_contact_message(settings: Settings) -> str:
    if settings.support_username:
        return f"Связаться с поддержкой: {settings.support_username}"
    return "Контакт поддержки пока не настроен. Создайте локальный запрос через Create request."


def format_plan_selected_message(plan_name: str) -> str:
    return f"Выбран план: {plan_name}\n{PAYMENT_PLACEHOLDER_MESSAGE}"


def format_datetime(value: datetime | None) -> str:
    if value is None:
        return "not-set"
    return ensure_utc(value).strftime("%Y-%m-%d %H:%M UTC")


def format_price(value: Decimal | None) -> str:
    if value is None:
        return "not-set"
    return f"{value:.2f} RUB"
