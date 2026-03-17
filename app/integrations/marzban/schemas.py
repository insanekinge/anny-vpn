from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MarzbanTokenResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    access_token: str | None = None
    token: str | None = None


class MarzbanUserPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    username: str
    note: str | None = None
    status: str = "active"
    data_limit: int = 0
    expire: int = 0
    proxies: dict[str, Any] = Field(default_factory=dict)
    inbounds: dict[str, Any] = Field(default_factory=dict)


class MarzbanUserResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    username: str
    status: str | None = None
    subscription_url: str | None = None
    links: list[str] = Field(default_factory=list)
    note: str | None = None
    expire: int | None = None
    data_limit: int | None = None
    used_traffic: int | None = None
    admin: dict[str, Any] | None = None
