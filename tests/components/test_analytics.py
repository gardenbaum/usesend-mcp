"""Analytics tools: routing + query-param shape (days/domainId compaction)."""

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
        store["params"] = req.url.params
        return httpx.Response(200, json={"id": "an_1"})

    return handler


CASES: list[tuple[str, dict[str, Any], str, str]] = [
    ("usesend_email_time_series", {}, "GET", "/api/v1/analytics/email-time-series"),
    ("usesend_reputation_metrics", {}, "GET", "/api/v1/analytics/reputation-metrics"),
]


@pytest.mark.parametrize(("tool", "args", "method", "path"), CASES)
async def test_analytics_tool_routing(
    tool: str, args: dict[str, Any], method: str, path: str
) -> None:
    seen: dict[str, Any] = {}
    out = await _call(_record_handler(seen), tool, args)
    assert seen["method"] == method
    assert seen["path"] == path
    assert "an_1" in out


async def test_email_time_series_params_present_when_given() -> None:
    seen: dict[str, Any] = {}
    await _call(
        _record_handler(seen),
        "usesend_email_time_series",
        {"days": "7", "domain_id": "dom_1"},
    )
    assert seen["params"]["days"] == "7"
    assert seen["params"]["domainId"] == "dom_1"


async def test_email_time_series_params_absent_when_omitted() -> None:
    seen: dict[str, Any] = {}
    await _call(_record_handler(seen), "usesend_email_time_series", {})
    assert "days" not in seen["params"]
    assert "domainId" not in seen["params"]


async def test_reputation_metrics_forwards_domain_id() -> None:
    seen: dict[str, Any] = {}
    await _call(_record_handler(seen), "usesend_reputation_metrics", {"domain_id": "dom_1"})
    assert seen["params"]["domainId"] == "dom_1"


async def test_reputation_metrics_omits_domain_id_when_absent() -> None:
    seen: dict[str, Any] = {}
    await _call(_record_handler(seen), "usesend_reputation_metrics", {})
    assert "domainId" not in seen["params"]
