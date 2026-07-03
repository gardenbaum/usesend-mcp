"""useSend campaign tools."""

import re
from typing import Any, Literal

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


CampaignStatus = Literal["DRAFT", "SCHEDULED", "RUNNING", "PAUSED", "SENT"]


@provider.tool(annotations=ToolAnnotations(title="Create campaign"))
@map_domain_errors
async def usesend_create_campaign(
    ctx: Context,
    name: str,
    from_address: str,
    subject: str,
    contact_book_id: str,
    html: str | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Create a new email campaign."""
    body = _compact(
        name=name,
        subject=subject,
        contact_book_id=contact_book_id,
        html=html,
    )
    body["from"] = from_address  # useSend's field is "from", not the camelCase "fromAddress"
    data = await _client(ctx).request("POST", "/v1/campaigns", json=body)
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Get campaign", readOnlyHint=True))
@map_domain_errors
async def usesend_get_campaign(
    ctx: Context, campaign_id: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Get details for a specific campaign."""
    data = await _client(ctx).request("GET", f"/v1/campaigns/{campaign_id}")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="List campaigns", readOnlyHint=True))
@map_domain_errors
async def usesend_list_campaigns(
    ctx: Context,
    page: int = 1,
    status: CampaignStatus | None = None,
    search: str | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """List campaigns; optional status filter and name/subject search (no limit override)."""
    params = _compact(page=page, status=status, search=search)
    data = await _client(ctx).request("GET", "/v1/campaigns", params=params)
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Delete campaign", destructiveHint=True))
@map_domain_errors
async def usesend_delete_campaign(
    ctx: Context, campaign_id: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Delete a campaign."""
    data = await _client(ctx).request("DELETE", f"/v1/campaigns/{campaign_id}")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Pause campaign", destructiveHint=True))
@map_domain_errors
async def usesend_pause_campaign(
    ctx: Context, campaign_id: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Pause a running campaign."""
    data = await _client(ctx).request("POST", f"/v1/campaigns/{campaign_id}/pause")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Resume campaign"))
@map_domain_errors
async def usesend_resume_campaign(
    ctx: Context, campaign_id: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Resume a paused campaign."""
    data = await _client(ctx).request("POST", f"/v1/campaigns/{campaign_id}/resume")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Schedule campaign"))
@map_domain_errors
async def usesend_schedule_campaign(
    ctx: Context, campaign_id: str, scheduled_at: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Schedule a campaign to be sent at a future time."""
    data = await _client(ctx).request(
        "POST", f"/v1/campaigns/{campaign_id}/schedule", json={"scheduledAt": scheduled_at}
    )
    return format_response(data, response_format)
