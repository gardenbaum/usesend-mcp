"""Campaign tools: routing + body-shape (_compact) behavior."""

import json
from typing import Any

import httpx
import pytest
from fastmcp import Client

from tests.conftest import Handler, make_test_lifespan
from usesend_mcp.server import create_server
from usesend_mcp.settings import Settings


async def _call(handler: Handler, tool: str, args: dict[str, Any]) -> str:
    server = create_server(Settings(api_key="us_test"), lifespan=make_test_lifespan(handler))
    async with Client(server) as c:
        result = await c.call_tool(tool, args)
    return result.data


def _record_handler(store: dict[str, Any]) -> Handler:
    def handler(req: httpx.Request) -> httpx.Response:
        store["method"] = req.method
        store["path"] = req.url.path
        return httpx.Response(200, json={"id": "cmp_1"})

    return handler


CASES: list[tuple[str, dict[str, Any], str, str]] = [
    (
        "usesend_create_campaign",
        {"name": "S", "from_address": "s@x.io", "subject": "Hi", "contact_book_id": "cb_1"},
        "POST",
        "/api/v1/campaigns",
    ),
    ("usesend_get_campaign", {"campaign_id": "cmp_1"}, "GET", "/api/v1/campaigns/cmp_1"),
    ("usesend_list_campaigns", {}, "GET", "/api/v1/campaigns"),
    ("usesend_delete_campaign", {"campaign_id": "cmp_1"}, "DELETE", "/api/v1/campaigns/cmp_1"),
    ("usesend_pause_campaign", {"campaign_id": "cmp_1"}, "POST", "/api/v1/campaigns/cmp_1/pause"),
    (
        "usesend_resume_campaign",
        {"campaign_id": "cmp_1"},
        "POST",
        "/api/v1/campaigns/cmp_1/resume",
    ),
    (
        "usesend_schedule_campaign",
        {"campaign_id": "cmp_1", "scheduled_at": "2026-01-01T09:00:00Z"},
        "POST",
        "/api/v1/campaigns/cmp_1/schedule",
    ),
]


@pytest.mark.parametrize(("tool", "args", "method", "path"), CASES)
async def test_campaign_tool_routing(
    tool: str, args: dict[str, Any], method: str, path: str
) -> None:
    seen: dict[str, Any] = {}
    out = await _call(_record_handler(seen), tool, args)
    assert seen["method"] == method
    assert seen["path"] == path
    assert "cmp_1" in out


async def test_create_campaign_body_uses_camel_case_and_omits_none() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "cmp_1"})

    await _call(
        handler,
        "usesend_create_campaign",
        {
            "name": "S",
            "from_address": "s@x.io",
            "subject": "Hi",
            "contact_book_id": "cb_1",
        },
    )
    assert seen["body"] == {
        "name": "S",
        "from": "s@x.io",
        "subject": "Hi",
        "contactBookId": "cb_1",
    }
    assert "html" not in seen["body"]


async def test_create_campaign_forwards_extended_fields() -> None:
    """previewText/content/replyTo/cc/bcc/sendNow/scheduledAt/batchSize per openapi.json."""
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "cmp_1"})

    await _call(
        handler,
        "usesend_create_campaign",
        {
            "name": "S",
            "from_address": "s@x.io",
            "subject": "Hi",
            "contact_book_id": "cb_1",
            "preview_text": "peek",
            "content": "{}",
            "reply_to": ["r@x.io"],
            "cc": ["c@x.io"],
            "bcc": ["b@x.io"],
            "send_now": True,
            "scheduled_at": "2026-01-01T09:00:00Z",
            "batch_size": 50,
        },
    )
    assert seen["body"] == {
        "name": "S",
        "subject": "Hi",
        "contactBookId": "cb_1",
        "previewText": "peek",
        "content": "{}",
        "replyTo": ["r@x.io"],
        "cc": ["c@x.io"],
        "bcc": ["b@x.io"],
        "sendNow": True,
        "scheduledAt": "2026-01-01T09:00:00Z",
        "batchSize": 50,
        "from": "s@x.io",
    }


async def test_list_campaigns_sends_page_but_not_limit() -> None:
    """UseSend's openapi.json documents page/status/search for this endpoint — no limit."""
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["params"] = req.url.params
        return httpx.Response(200, json={"id": "cmp_1"})

    await _call(handler, "usesend_list_campaigns", {"page": 2})
    assert seen["params"]["page"] == "2"
    assert "limit" not in seen["params"]


async def test_list_campaigns_forwards_status_and_search() -> None:
    """openapi.json documents optional status (enum) + name/subject search filters."""
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["params"] = req.url.params
        return httpx.Response(200, json={"id": "cmp_1"})

    await _call(
        handler,
        "usesend_list_campaigns",
        {"page": 1, "status": "RUNNING", "search": "newsletter"},
    )
    assert seen["params"]["status"] == "RUNNING"
    assert seen["params"]["search"] == "newsletter"


async def test_schedule_campaign_body_shape() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "cmp_1"})

    await _call(
        handler,
        "usesend_schedule_campaign",
        {"campaign_id": "cmp_1", "scheduled_at": "2026-01-01T09:00:00Z"},
    )
    assert seen["body"] == {"scheduledAt": "2026-01-01T09:00:00Z"}
