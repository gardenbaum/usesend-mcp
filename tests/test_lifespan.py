"""The default lifespan provides a UsesendClient under 'usesend'."""

from collections.abc import Callable

import httpx
from fastmcp import Client, Context, FastMCP

from usesend_mcp.client.usesend_client import UsesendClient

MakeServer = Callable[[Callable[[httpx.Request], httpx.Response]], FastMCP]


async def test_lifespan_exposes_client(make_server: MakeServer) -> None:
    captured: dict[str, object] = {}

    server = make_server(lambda req: httpx.Response(200, json={}))

    @server.tool
    async def _probe(ctx: Context) -> str:  # pyright: ignore[reportUnusedFunction]
        captured["client"] = ctx.lifespan_context["usesend"]
        return "ok"

    async with Client(server) as c:
        await c.call_tool("_probe", {})
    assert isinstance(captured["client"], UsesendClient)
