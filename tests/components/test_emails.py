"""Email tools: routing + default_from behavior."""

import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import httpx
import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError

from tests.conftest import Handler, make_test_lifespan
from usesend_mcp.client.usesend_client import UsesendClient
from usesend_mcp.server import create_server
from usesend_mcp.settings import Settings


async def _call(handler: Handler, tool: str, args: dict[str, Any]) -> str:
    server = create_server(
        Settings(api_key="us_test", default_from="def@x.io"), lifespan=make_test_lifespan(handler)
    )
    async with Client(server) as c:
        result = await c.call_tool(tool, args)
    return result.data


@pytest.mark.parametrize(
    ("tool", "args", "method", "path"),
    [
        (
            "usesend_send_email",
            {"to": "a@x.io", "from_address": "s@x.io", "subject": "Hi", "text": "yo"},
            "POST",
            "/api/v1/emails",
        ),
        (
            "usesend_batch_send_emails",
            {"emails": [{"to": "a@x.io", "from_address": "s@x.io", "subject": "A", "text": "a"}]},
            "POST",
            "/api/v1/emails/batch",
        ),
        ("usesend_list_emails", {}, "GET", "/api/v1/emails"),
        ("usesend_get_email", {"email_id": "e_1"}, "GET", "/api/v1/emails/e_1"),
        ("usesend_cancel_email", {"email_id": "e_1"}, "POST", "/api/v1/emails/e_1/cancel"),
        (
            "usesend_update_email_schedule",
            {"email_id": "e_1", "scheduled_at": "2026-01-01T00:00:00Z"},
            "PATCH",
            "/api/v1/emails/e_1",
        ),
    ],
)
async def test_email_tool_routing(tool: str, args: dict[str, Any], method: str, path: str) -> None:
    seen: dict[str, Any] = {}
    out = await _call(_record_handler(seen), tool, args)
    assert seen["method"] == method
    assert seen["path"] == path
    assert "e_1" in out


def _record_handler(store: dict[str, Any]) -> Handler:
    def handler(req: httpx.Request) -> httpx.Response:
        store["method"] = req.method
        store["path"] = req.url.path
        return httpx.Response(200, json={"id": "e_1", "status": "queued"})

    return handler


async def test_send_uses_default_from_when_omitted() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "e_1"})

    await _call(handler, "usesend_send_email", {"to": "a@x.io", "subject": "Hi", "text": "yo"})
    assert seen["body"]["from"] == "def@x.io"


async def test_send_omits_subject_when_none() -> None:
    """UseSend's openapi.json marks subject optional when template_id supplies it."""
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "e_1"})

    await _call(
        handler,
        "usesend_send_email",
        {"to": "a@x.io", "from_address": "s@x.io", "template_id": "tmpl_1"},
    )
    assert "subject" not in seen["body"]
    assert seen["body"]["templateId"] == "tmpl_1"


async def test_send_omits_from_when_no_default_configured() -> None:
    """With no from_address and no USESEND_DEFAULT_FROM, no 'from' key is sent at all."""
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "e_1"})

    @asynccontextmanager
    async def lifespan(_server: FastMCP) -> AsyncGenerator[dict[str, UsesendClient | str | None]]:
        client = UsesendClient(Settings(api_key="us_test"), transport=httpx.MockTransport(handler))
        try:
            yield {"usesend": client, "default_from": None}
        finally:
            await client.aclose()

    server = create_server(Settings(api_key="us_test"), lifespan=lifespan)
    async with Client(server) as c:
        await c.call_tool("usesend_send_email", {"to": "a@x.io", "subject": "Hi", "text": "yo"})
    assert "from" not in seen["body"]


async def test_list_emails_forwards_optional_filters() -> None:
    """UseSend's openapi.json documents startDate/endDate/domainId for GET /v1/emails."""
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["params"] = req.url.params
        return httpx.Response(200, json={"data": []})

    await _call(
        handler,
        "usesend_list_emails",
        {
            "page": 2,
            "limit": 10,
            "start_date": "2024-01-01T00:00:00Z",
            "end_date": "2024-01-31T23:59:59Z",
            "domain_id": "123",
        },
    )
    params = seen["params"]
    assert params["page"] == "2"
    assert params["limit"] == "10"
    assert params["startDate"] == "2024-01-01T00:00:00Z"
    assert params["endDate"] == "2024-01-31T23:59:59Z"
    assert params["domainId"] == "123"


async def test_list_emails_omits_optional_filters_when_absent() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["params"] = req.url.params
        return httpx.Response(200, json={"data": []})

    await _call(handler, "usesend_list_emails", {})
    params = seen["params"]
    assert params["page"] == "1"
    assert params["limit"] == "50"
    assert "startDate" not in params
    assert "endDate" not in params
    assert "domainId" not in params


async def test_send_forwards_extended_fields() -> None:
    """variables/headers/inReplyToId map to camelCase; attachments serialize to dicts."""
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "e_1"})

    await _call(
        handler,
        "usesend_send_email",
        {
            "to": "a@x.io",
            "from_address": "s@x.io",
            "template_id": "tmpl_1",
            "variables": {"name": "Ada"},
            "headers": {"X-Entity": "42"},
            "in_reply_to_id": "e_0",
            "attachments": [{"filename": "a.txt", "content": "aGk="}],
        },
    )
    body = seen["body"]
    assert body["variables"] == {"name": "Ada"}
    assert body["headers"] == {"X-Entity": "42"}
    assert body["inReplyToId"] == "e_0"
    assert body["attachments"] == [{"filename": "a.txt", "content": "aGk="}]


async def test_batch_rejects_empty_list() -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={})

    with pytest.raises(ToolError, match="Mindestens eine"):
        await _call(handler, "usesend_batch_send_emails", {"emails": []})


async def test_batch_rejects_more_than_100() -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={})

    emails = [{"to": "a@x.io", "subject": "s", "text": "t"}] * 101
    with pytest.raises(ToolError, match="Maximal 100"):
        await _call(handler, "usesend_batch_send_emails", {"emails": emails})
