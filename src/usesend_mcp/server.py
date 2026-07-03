"""The composition root: build and wire the stdio FastMCP server."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from fastmcp.server.lifespan import Lifespan
from fastmcp.server.server import LifespanCallable

from usesend_mcp.client.usesend_client import UsesendClient
from usesend_mcp.components import (
    analytics,
    campaigns,
    contact_books,
    contacts,
    domains,
    emails,
)
from usesend_mcp.logging import configure_logging
from usesend_mcp.settings import Settings

LifespanArg = LifespanCallable | Lifespan | None

INSTRUCTIONS = (
    "useSend MCP server. Use the tools to send emails and manage contacts, "
    "contact books, campaigns, domains and analytics on the useSend platform."
)


def _default_lifespan(settings: Settings) -> LifespanCallable:
    @asynccontextmanager
    async def lifespan(_server: FastMCP) -> AsyncGenerator[dict[str, UsesendClient | str | None]]:
        client = UsesendClient(settings)
        try:
            yield {"usesend": client, "default_from": settings.default_from}
        finally:
            await client.aclose()

    return lifespan


def create_server(settings: Settings | None = None, lifespan: LifespanArg = None) -> FastMCP:
    """Build a fully wired stdio useSend MCP server."""
    settings = settings or Settings()
    configure_logging(settings.log_level)
    return FastMCP(
        name=settings.server_name,
        instructions=INSTRUCTIONS,
        providers=[
            emails.provider,
            contact_books.provider,
            contacts.provider,
            campaigns.provider,
            domains.provider,
            analytics.provider,
        ],
        mask_error_details=True,
        lifespan=lifespan or _default_lifespan(settings),
    )
