"""Contact book tools: routing + body-shape (_compact) behavior."""

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
        return httpx.Response(200, json={"id": "cb_1"})

    return handler


CASES: list[tuple[str, dict[str, Any], str, str]] = [
    # list is unpaginated per useSend's openapi.json — no page/limit query params.
    ("usesend_list_contact_books", {}, "GET", "/api/v1/contactBooks"),
    ("usesend_get_contact_book", {"contact_book_id": "cb_1"}, "GET", "/api/v1/contactBooks/cb_1"),
    ("usesend_create_contact_book", {"name": "VIP"}, "POST", "/api/v1/contactBooks"),
    (
        "usesend_update_contact_book",
        {"contact_book_id": "cb_1", "name": "X"},
        "PATCH",
        "/api/v1/contactBooks/cb_1",
    ),
    (
        "usesend_delete_contact_book",
        {"contact_book_id": "cb_1"},
        "DELETE",
        "/api/v1/contactBooks/cb_1",
    ),
]


@pytest.mark.parametrize(("tool", "args", "method", "path"), CASES)
async def test_contact_book_tool_routing(
    tool: str, args: dict[str, Any], method: str, path: str
) -> None:
    seen: dict[str, Any] = {}
    out = await _call(_record_handler(seen), tool, args)
    assert seen["method"] == method
    assert seen["path"] == path
    assert "cb_1" in out


async def test_create_contact_book_body_uses_camel_case_and_omits_none() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "cb_1"})

    await _call(
        handler,
        "usesend_create_contact_book",
        {"name": "VIP", "double_opt_in_enabled": True, "double_opt_in_from": "hi@x.io"},
    )
    assert seen["body"] == {
        "name": "VIP",
        "doubleOptInEnabled": True,
        "doubleOptInFrom": "hi@x.io",
    }
    assert "doubleOptInSubject" not in seen["body"]
