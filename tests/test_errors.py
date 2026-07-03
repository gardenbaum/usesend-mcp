"""Tests for the domain error hierarchy and the MCP error-mapping boundary.

The failing tools live here in ``tests/`` (never in ``src/usesend_mcp/components/``)
so they exercise the mapping without expanding the shipped capability surface. They
are defined at module level and registered per test onto a fresh ``create_server()``.
"""

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from usesend_mcp.errors import (
    AuthError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UpstreamError,
    ValidationFailedError,
    error_for_status,
    map_domain_errors,
)
from usesend_mcp.server import create_server


@map_domain_errors
async def _ok(value: str) -> str:
    return value.upper()


@map_domain_errors
async def _explode(entity_id: str) -> str:
    try:
        raise RuntimeError("dsn=postgres://user:SECRET@db/internal")
    except RuntimeError as cause:
        raise NotFoundError(f"entity {entity_id} not found") from cause


@map_domain_errors
async def _down() -> str:
    raise UpstreamError("usesend backend unavailable")


async def _bug() -> str:
    raise ValueError("RAW-INTERNAL-BUG-LEAK")


async def test_decorated_tool_returns_normally() -> None:
    mcp = create_server()
    mcp.tool(_ok)
    async with Client(mcp) as client:
        result = await client.call_tool("_ok", {"value": "hi"})
    assert result.data == "HI"


async def test_domain_error_returns_sanitized_message_without_internals() -> None:
    mcp = create_server()
    mcp.tool(_explode)
    async with Client(mcp) as client:
        with pytest.raises(ToolError) as exc_info:
            await client.call_tool("_explode", {"entity_id": "x1"})

    message = str(exc_info.value)
    assert "entity x1 not found" in message  # sanitized domain message reaches client
    assert "SECRET" not in message  # wrapped-cause detail does not
    assert "RuntimeError" not in message  # internal exception type does not
    assert "Traceback" not in message  # no stack trace


async def test_upstream_error_is_also_mapped() -> None:
    mcp = create_server()
    mcp.tool(_down)
    async with Client(mcp) as client:
        with pytest.raises(ToolError) as exc_info:
            await client.call_tool("_down", {})
    assert "usesend backend unavailable" in str(exc_info.value)


async def test_map_domain_errors_suppresses_cause_chain() -> None:
    @map_domain_errors
    async def _raises() -> str:
        try:
            raise RuntimeError("internal SECRET detail")
        except RuntimeError as cause:
            raise NotFoundError("not found") from cause

    with pytest.raises(ToolError) as exc_info:
        await _raises()
    assert exc_info.value.__cause__ is None  # internal cause chain dropped at the boundary


async def test_unmapped_exception_is_masked() -> None:
    mcp = create_server()
    mcp.tool(_bug)
    async with Client(mcp) as client:
        with pytest.raises(ToolError) as exc_info:
            await client.call_tool("_bug", {})

    message = str(exc_info.value)
    assert "RAW-INTERNAL-BUG-LEAK" not in message  # masked by mask_error_details=True
    assert "Traceback" not in message


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (401, AuthError),
        (403, PermissionDeniedError),
        (404, NotFoundError),
        (409, ConflictError),
        (422, ValidationFailedError),
        (429, RateLimitError),
        (500, UpstreamError),
        (503, UpstreamError),
    ],
)
def test_error_for_status(status: int, expected: type) -> None:
    err = error_for_status(status, detail="x")
    assert isinstance(err, expected)


def test_auth_message_is_actionable() -> None:
    assert "USESEND_API_KEY" in str(error_for_status(401, None))
