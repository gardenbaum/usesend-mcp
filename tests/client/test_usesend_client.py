"""UsesendClient tests (no real network — httpx.MockTransport)."""

from collections.abc import Callable

import httpx
import pytest

from usesend_mcp.client.usesend_client import UsesendClient
from usesend_mcp.errors import AuthError, NotFoundError, RateLimitError, UpstreamError
from usesend_mcp.settings import Settings


def _client(
    handler: Callable[[httpx.Request], httpx.Response], api_key: str | None = "us_test"
) -> UsesendClient:
    return UsesendClient(Settings(api_key=api_key), transport=httpx.MockTransport(handler))


async def test_sets_auth_and_base_path() -> None:
    seen: dict[str, str] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["url"] = str(req.url)
        seen["auth"] = req.headers.get("authorization", "")
        return httpx.Response(200, json={"ok": True})

    client = _client(handler)
    data = await client.request("GET", "/v1/emails")
    await client.aclose()
    assert data == {"ok": True}
    assert seen["url"] == "https://app.usesend.com/api/v1/emails"
    assert seen["auth"] == "Bearer us_test"


async def test_missing_api_key_raises_before_request() -> None:
    def handler(req: httpx.Request) -> httpx.Response:  # pragma: no cover - must not run
        raise AssertionError("request must not be sent without api key")

    client = _client(handler, api_key=None)
    with pytest.raises(AuthError):
        await client.request("GET", "/v1/emails")
    await client.aclose()


@pytest.mark.parametrize(("status", "exc"), [(404, NotFoundError), (429, RateLimitError)])
async def test_status_maps_to_domain_error(status: int, exc: type) -> None:
    client = _client(lambda req: httpx.Response(status, json={"error": "boom"}))
    with pytest.raises(exc):
        await client.request("GET", "/v1/emails/x")
    await client.aclose()


async def test_empty_body_returns_none() -> None:
    client = _client(lambda req: httpx.Response(204))
    assert await client.request("DELETE", "/v1/emails/x") is None
    await client.aclose()


@pytest.mark.parametrize("body", [{"unrelated": "field"}, ["not", "a", "dict"]])
async def test_error_without_recognized_detail_key_has_no_suffix(body: object) -> None:
    """A failure body with no message/error/detail string yields a bare domain message."""
    client = _client(lambda req: httpx.Response(404, json=body))
    with pytest.raises(NotFoundError) as excinfo:
        await client.request("GET", "/v1/emails/x")
    await client.aclose()
    assert "(" not in str(excinfo.value)


async def test_transport_error_maps_to_upstream_error() -> None:
    """A transport-level failure (no response received) still raises a domain error."""

    def handler(req: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom")

    client = _client(handler)
    with pytest.raises(UpstreamError):
        await client.request("GET", "/v1/emails")
    await client.aclose()
