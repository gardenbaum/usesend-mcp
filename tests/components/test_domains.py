"""Domain tools: routing + body-shape (_compact) behavior."""

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
        return httpx.Response(200, json={"id": 123})

    return handler


CASES: list[tuple[str, dict[str, Any], str, str]] = [
    ("usesend_list_domains", {}, "GET", "/api/v1/domains"),
    ("usesend_get_domain", {"domain_id": 123}, "GET", "/api/v1/domains/123"),
    (
        "usesend_create_domain",
        {"name": "mail.x.io", "region": "us-east-1"},
        "POST",
        "/api/v1/domains",
    ),
    ("usesend_verify_domain", {"domain_id": 123}, "PUT", "/api/v1/domains/123/verify"),
    ("usesend_delete_domain", {"domain_id": 123}, "DELETE", "/api/v1/domains/123"),
]


@pytest.mark.parametrize(("tool", "args", "method", "path"), CASES)
async def test_domain_tool_routing(tool: str, args: dict[str, Any], method: str, path: str) -> None:
    seen: dict[str, Any] = {}
    out = await _call(_record_handler(seen), tool, args)
    assert seen["method"] == method
    assert seen["path"] == path
    assert "123" in out


async def test_create_domain_body_includes_name_and_region() -> None:
    """UseSend's openapi.json requires both name and region."""
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": 123})

    await _call(handler, "usesend_create_domain", {"name": "mail.x.io", "region": "eu-west-1"})
    assert seen["body"] == {"name": "mail.x.io", "region": "eu-west-1"}
