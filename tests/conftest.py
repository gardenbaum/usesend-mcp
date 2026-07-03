"""Shared pytest fixtures."""

from collections.abc import AsyncGenerator, AsyncIterator, Callable
from contextlib import asynccontextmanager

import httpx
import pytest
from fastmcp import Client, FastMCP
from fastmcp.client.transports import FastMCPTransport

from usesend_mcp.client.usesend_client import UsesendClient
from usesend_mcp.server import create_server
from usesend_mcp.settings import Settings

Handler = Callable[[httpx.Request], httpx.Response]


def make_test_lifespan(handler: Handler):
    """Build a FastMCP lifespan yielding a MockTransport-backed UsesendClient."""

    @asynccontextmanager
    async def lifespan(_server: FastMCP) -> AsyncGenerator[dict[str, UsesendClient | str | None]]:
        client = UsesendClient(Settings(api_key="us_test"), transport=httpx.MockTransport(handler))
        try:
            yield {"usesend": client, "default_from": "def@x.io"}
        finally:
            await client.aclose()

    return lifespan


@pytest.fixture
def server() -> FastMCP:
    """A server with no network (empty-200 handler)."""
    return create_server(
        Settings(api_key="us_test"),
        lifespan=make_test_lifespan(lambda req: httpx.Response(200, json={})),
    )


@pytest.fixture
async def client(server: FastMCP) -> AsyncIterator[Client[FastMCPTransport]]:
    async with Client(server) as connected:
        yield connected


@pytest.fixture
def make_server() -> Callable[[Handler], FastMCP]:
    """Factory: build a server whose client uses the given MockTransport handler."""

    def _make(handler: Handler) -> FastMCP:
        return create_server(Settings(api_key="us_test"), lifespan=make_test_lifespan(handler))

    return _make
