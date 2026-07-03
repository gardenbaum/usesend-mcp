"""useSend contact tools (nested under a contact book)."""

import re
from typing import Any
from urllib.parse import quote

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


def _base(contact_book_id: str) -> str:
    return f"/v1/contactBooks/{contact_book_id}/contacts"


@provider.tool(annotations=ToolAnnotations(title="List contacts", readOnlyHint=True))
@map_domain_errors
async def usesend_list_contacts(
    ctx: Context,
    contact_book_id: str,
    page: int = 1,
    limit: int = 50,
    response_format: ResponseFormat = "markdown",
) -> str:
    """List contacts in a contact book with pagination."""
    data = await _client(ctx).request(
        "GET", _base(contact_book_id), params={"page": page, "limit": limit}
    )
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Get contact", readOnlyHint=True))
@map_domain_errors
async def usesend_get_contact(
    ctx: Context,
    contact_book_id: str,
    contact_id: str,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Get details for a specific contact."""
    data = await _client(ctx).request("GET", f"{_base(contact_book_id)}/{contact_id}")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Create contact"))
@map_domain_errors
async def usesend_create_contact(
    ctx: Context,
    contact_book_id: str,
    email: str,
    first_name: str | None = None,
    last_name: str | None = None,
    subscribed: bool = True,
    properties: dict[str, object] | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Create a new contact in a contact book."""
    body = _compact(
        email=email,
        first_name=first_name,
        last_name=last_name,
        subscribed=subscribed,
        properties=properties,
    )
    data = await _client(ctx).request("POST", _base(contact_book_id), json=body)
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Update contact"))
@map_domain_errors
async def usesend_update_contact(
    ctx: Context,
    contact_book_id: str,
    contact_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
    subscribed: bool | None = None,
    properties: dict[str, object] | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Update a contact's mutable fields."""
    body = _compact(
        first_name=first_name,
        last_name=last_name,
        subscribed=subscribed,
        properties=properties,
    )
    data = await _client(ctx).request("PATCH", f"{_base(contact_book_id)}/{contact_id}", json=body)
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Upsert contact"))
@map_domain_errors
async def usesend_upsert_contact(
    ctx: Context,
    contact_book_id: str,
    email: str,
    first_name: str | None = None,
    last_name: str | None = None,
    subscribed: bool | None = None,
    properties: dict[str, object] | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Create or update a contact by email (upsert)."""
    body = _compact(
        email=email,
        first_name=first_name,
        last_name=last_name,
        subscribed=subscribed,
        properties=properties,
    )
    # useSend's PUT route is templated as .../contacts/{contactId}, but the handler
    # keys the upsert purely on the email in the body and never reads the path segment —
    # it must still be present for routing to match, so we fill it with the email.
    path = f"{_base(contact_book_id)}/{quote(email, safe='')}"
    data = await _client(ctx).request("PUT", path, json=body)
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Delete contact", destructiveHint=True))
@map_domain_errors
async def usesend_delete_contact(
    ctx: Context,
    contact_book_id: str,
    contact_id: str,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Delete a contact from a contact book."""
    data = await _client(ctx).request("DELETE", f"{_base(contact_book_id)}/{contact_id}")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Bulk create contacts"))
@map_domain_errors
async def usesend_bulk_create_contacts(
    ctx: Context,
    contact_book_id: str,
    contacts: list[dict[str, object]],
    response_format: ResponseFormat = "markdown",
) -> str:
    """Create multiple contacts in a single request."""
    data = await _client(ctx).request("POST", f"{_base(contact_book_id)}/bulk", json=contacts)
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Bulk delete contacts", destructiveHint=True))
@map_domain_errors
async def usesend_bulk_delete_contacts(
    ctx: Context,
    contact_book_id: str,
    contact_ids: list[str],
    response_format: ResponseFormat = "markdown",
) -> str:
    """Delete multiple contacts in a single request."""
    data = await _client(ctx).request(
        "DELETE", f"{_base(contact_book_id)}/bulk", json={"contactIds": contact_ids}
    )
    return format_response(data, response_format)
