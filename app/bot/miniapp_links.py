from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from app.core.config import get_settings


SECTION_TAB_MAP = {
    "subscription": "home",
    "support-section": "profile",
    "billing-section": "profile",
    "settings-section": "profile",
    "privacy-section": "profile",
}


def build_miniapp_url(
    *,
    tab: str | None = None,
    section: str | None = None,
    source: str | None = None,
) -> str | None:
    settings = get_settings()
    if not settings.miniapp_url:
        return None

    parts = urlsplit(settings.miniapp_url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))

    if tab:
        query["tab"] = tab
    if section:
        query["section"] = section
        query.setdefault("tab", SECTION_TAB_MAP.get(section, query.get("tab", "")))
    if source:
        query["source"] = source

    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
