"""useSend contact book tools."""

import re
from typing import Any

from fastmcp import Context
from fastmcp.server.providers import LocalProvider
from mcp.types import ToolAnnotations

from usesend_mcp.errors import map_domain_errors
from usesend_mcp.formatting import ResponseFormat, format_response

provider = LocalProvider()

_SNAKE_UNDERSCORE = re.compile(r"_([a-z0-9])")


def _client(ctx: Context) -> Any:
    return ctx.lifespan_context["usesend"]


def _to_camel_case(name: str) -> str:
    return _SNAKE_UNDERSCORE.sub(lambda m: m.group(1).upper(), name)


def _compact(**kwargs: Any) -> dict[str, Any]:
    """Build a JSON body from kwargs, dropping ``None`` values and camelCasing keys."""
    return {_to_camel_case(key): value for key, value in kwargs.items() if value is not None}


@provider.tool(annotations=ToolAnnotations(title="List contact books", readOnlyHint=True))
@map_domain_errors
async def usesend_list_contact_books(
    ctx: Context, response_format: ResponseFormat = "markdown"
) -> str:
    """List all contact books accessible by the API key (endpoint is unpaginated)."""
    data = await _client(ctx).request("GET", "/v1/contactBooks")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Get contact book", readOnlyHint=True))
@map_domain_errors
async def usesend_get_contact_book(
    ctx: Context, contact_book_id: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Get details for a specific contact book."""
    data = await _client(ctx).request("GET", f"/v1/contactBooks/{contact_book_id}")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Create contact book"))
@map_domain_errors
async def usesend_create_contact_book(
    ctx: Context,
    name: str,
    double_opt_in_enabled: bool = False,
    double_opt_in_from: str | None = None,
    double_opt_in_subject: str | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Create a new contact book."""
    body = _compact(
        name=name,
        double_opt_in_enabled=double_opt_in_enabled,
        double_opt_in_from=double_opt_in_from,
        double_opt_in_subject=double_opt_in_subject,
    )
    data = await _client(ctx).request("POST", "/v1/contactBooks", json=body)
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Update contact book"))
@map_domain_errors
async def usesend_update_contact_book(
    ctx: Context,
    contact_book_id: str,
    name: str | None = None,
    double_opt_in_enabled: bool | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Update a contact book's mutable fields."""
    body = _compact(name=name, double_opt_in_enabled=double_opt_in_enabled)
    data = await _client(ctx).request("PATCH", f"/v1/contactBooks/{contact_book_id}", json=body)
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Delete contact book", destructiveHint=True))
@map_domain_errors
async def usesend_delete_contact_book(
    ctx: Context, contact_book_id: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Delete a contact book."""
    data = await _client(ctx).request("DELETE", f"/v1/contactBooks/{contact_book_id}")
    return format_response(data, response_format)
