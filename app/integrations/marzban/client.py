from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.config import Settings, get_settings
from app.integrations.marzban.exceptions import (
    MarzbanAuthenticationError,
    MarzbanUnavailableError,
)
from app.integrations.marzban.schemas import MarzbanTokenResponse, MarzbanUserPayload


LOGGER = logging.getLogger(__name__)


class MarzbanClient:
    def __init__(
        self,
        settings: Settings | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self._transport = transport
        self._token: str | None = None
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            base_url = self.settings.marzban_base_url
            if not base_url:
                raise MarzbanUnavailableError("MARZBAN_BASE_URL is not configured.")
            timeout = httpx.Timeout(self.settings.marzban_timeout)
            self._client = httpx.AsyncClient(
                base_url=base_url.rstrip("/"),
                verify=self.settings.marzban_verify_ssl,
                timeout=timeout,
                transport=self._transport,
            )
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()

    async def login(self) -> str:
        if self._token:
            return self._token

        client = await self._get_client()
        username = self.settings.marzban_username_value
        password = self.settings.marzban_password_value
        if not username or not password:
            raise MarzbanAuthenticationError("Marzban credentials are missing.")

        try:
            response = await client.post(
                "/api/admin/token",
                data={"username": username, "password": password},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise MarzbanAuthenticationError("Failed to authenticate with Marzban.") from exc
        except httpx.HTTPError as exc:
            raise MarzbanUnavailableError("Marzban is unavailable.") from exc

        payload = MarzbanTokenResponse.model_validate(response.json())
        token = payload.access_token or payload.token
        if not token:
            raise MarzbanAuthenticationError("Marzban authentication response did not include a token.")

        self._token = token
        return token

    async def _request(
        self,
        method: str,
        url: str,
        *,
        expected_statuses: tuple[int, ...] = (200,),
        **kwargs: Any,
    ) -> httpx.Response:
        client = await self._get_client()
        token = await self.login()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        try:
            response = await client.request(method, url, headers=headers, **kwargs)
        except httpx.HTTPError as exc:
            raise MarzbanUnavailableError("Marzban request failed.") from exc

        if response.status_code not in expected_statuses:
            response.raise_for_status()
        return response

    async def get_user(self, username: str) -> dict[str, Any] | None:
        response = await self._request("GET", f"/api/user/{username}", expected_statuses=(200, 404))
        if response.status_code == 404:
            return None
        return response.json()

    async def create_user(self, payload: MarzbanUserPayload) -> dict[str, Any]:
        response = await self._request(
            "POST",
            "/api/user",
            expected_statuses=(200, 201),
            json=payload.model_dump(exclude_none=True),
        )
        return response.json()

    async def modify_user(self, username: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = await self._request("PUT", f"/api/user/{username}", json=payload)
        return response.json()

    async def get_subscription_info(self, username: str) -> dict[str, Any] | None:
        try:
            response = await self._request("GET", f"/sub/{username}/info", expected_statuses=(200, 404))
        except httpx.HTTPStatusError:
            LOGGER.warning("Marzban subscription info endpoint returned an unexpected status for user %s.", username)
            return await self.get_user(username)
        if response.status_code == 404:
            return await self.get_user(username)
        return response.json()

    async def get_user_subscription_url(self, username: str) -> str | None:
        user_payload = await self.get_user(username)
        if not user_payload:
            return None
        return user_payload.get("subscription_url")
