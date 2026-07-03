"""Server composition tests."""

from fastmcp import Client, FastMCP
from fastmcp.client.transports import FastMCPTransport


async def test_server_builds_and_lists_no_tools_yet(client: Client[FastMCPTransport]) -> None:
    tools = await client.list_tools()
    assert isinstance(tools, list)


def test_create_server_returns_fastmcp(server: FastMCP) -> None:
    assert isinstance(server, FastMCP)
