"""Thin async httpx wrapper around the useSend v1 REST API."""

from __future__ import annotations

from typing import Any, cast

import httpx

from usesend_mcp.errors import AuthError, UpstreamError, error_for_status
from usesend_mcp.settings import Settings


class UsesendClient:
    """Authenticated async client that maps HTTP errors to domain errors."""

    def __init__(
        self, settings: Settings, *, transport: httpx.AsyncBaseTransport | None = None
    ) -> None:
        """Bind the client to the useSend base URL using the configured API key."""
        self._api_key = settings.api_key
        self._http = httpx.AsyncClient(
            base_url=settings.base_url.rstrip("/") + "/api",
            timeout=settings.timeout,
            transport=transport,
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Send a request; return parsed JSON (or None), raising a domain error on failure."""
        if not self._api_key:
            raise AuthError("Kein API-Key konfiguriert — USESEND_API_KEY setzen.")
        try:
            response = await self._http.request(
                method,
                path,
                json=json,
                params=params,
                headers={"Authorization": f"Bearer {self._api_key}"},
            )
        except httpx.RequestError as exc:
            raise UpstreamError("useSend-API vorübergehend nicht erreichbar.") from exc
        if response.is_success:
            return response.json() if response.content else None
        detail = _safe_detail(response)
        raise error_for_status(response.status_code, detail)

    async def aclose(self) -> None:
        """Close the underlying connection pool."""
        await self._http.aclose()


def _safe_detail(response: httpx.Response) -> str | None:
    """Extract a short, client-safe error hint from a failed response body."""
    try:
        body = response.json()
    except ValueError:  # pragma: no cover
        return None
    if isinstance(body, dict):
        typed_body = cast("dict[str, object]", body)
        for key in ("message", "error", "detail"):
            value = typed_body.get(key)
            if isinstance(value, str):
                return value[:200]
    return None
