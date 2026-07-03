"""Command-line entrypoint: run the useSend MCP server over stdio."""

from __future__ import annotations

from usesend_mcp.server import create_server
from usesend_mcp.settings import Settings


def main(argv: list[str] | None = None) -> None:
    """Build settings from the environment and run the server over stdio."""
    create_server(Settings()).run(transport="stdio")
