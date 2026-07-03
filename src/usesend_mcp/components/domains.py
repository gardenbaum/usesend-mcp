"""useSend domain tools."""

from typing import Any

from fastmcp import Context
from fastmcp.server.providers import LocalProvider
from mcp.types import ToolAnnotations

from usesend_mcp.errors import map_domain_errors
from usesend_mcp.formatting import ResponseFormat, format_response

provider = LocalProvider()


def _client(ctx: Context) -> Any:
    return ctx.lifespan_context["usesend"]


@provider.tool(
    annotations=ToolAnnotations(
        title="List domains", readOnlyHint=True, idempotentHint=True, openWorldHint=True
    )
)
@map_domain_errors
async def usesend_list_domains(ctx: Context, response_format: ResponseFormat = "markdown") -> str:
    """List all domains."""
    data = await _client(ctx).request("GET", "/v1/domains")
    return format_response(data, response_format)


@provider.tool(
    annotations=ToolAnnotations(
        title="Get domain", readOnlyHint=True, idempotentHint=True, openWorldHint=True
    )
)
@map_domain_errors
async def usesend_get_domain(
    ctx: Context, domain_id: int, response_format: ResponseFormat = "markdown"
) -> str:
    """Get details for a specific domain."""
    data = await _client(ctx).request("GET", f"/v1/domains/{domain_id}")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Create domain", openWorldHint=True))
@map_domain_errors
async def usesend_create_domain(
    ctx: Context,
    name: str,
    region: str,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Create a new domain. useSend requires both name and region."""
    data = await _client(ctx).request("POST", "/v1/domains", json={"name": name, "region": region})
    return format_response(data, response_format)


@provider.tool(
    annotations=ToolAnnotations(title="Verify domain", idempotentHint=True, openWorldHint=True)
)
@map_domain_errors
async def usesend_verify_domain(
    ctx: Context, domain_id: int, response_format: ResponseFormat = "markdown"
) -> str:
    """Trigger verification for a domain."""
    data = await _client(ctx).request("PUT", f"/v1/domains/{domain_id}/verify")
    return format_response(data, response_format)


@provider.tool(
    annotations=ToolAnnotations(
        title="Delete domain", destructiveHint=True, idempotentHint=True, openWorldHint=True
    )
)
@map_domain_errors
async def usesend_delete_domain(
    ctx: Context, domain_id: int, response_format: ResponseFormat = "markdown"
) -> str:
    """Delete a domain."""
    data = await _client(ctx).request("DELETE", f"/v1/domains/{domain_id}")
    return format_response(data, response_format)
