"""useSend email tools."""

from typing import Any

from fastmcp import Context
from fastmcp.server.providers import LocalProvider
from mcp.types import ToolAnnotations

from usesend_mcp.errors import map_domain_errors
from usesend_mcp.formatting import ResponseFormat, format_response
from usesend_mcp.models.emails import BatchEmailItem

provider = LocalProvider()


def _client(ctx: Context) -> Any:
    return ctx.lifespan_context["usesend"]


def _email_body(item: BatchEmailItem, default_from: str | None) -> dict[str, Any]:
    body: dict[str, Any] = {"to": item.to}
    sender = item.from_address or default_from
    if sender is not None:
        body["from"] = sender
    for src, dst in (
        (item.subject, "subject"),
        (item.html, "html"),
        (item.text, "text"),
        (item.cc, "cc"),
        (item.bcc, "bcc"),
        (item.reply_to, "replyTo"),
        (item.template_id, "templateId"),
        (item.scheduled_at, "scheduledAt"),
    ):
        if src is not None:
            body[dst] = src
    return body


@provider.tool(annotations=ToolAnnotations(title="Send email"))
@map_domain_errors
async def usesend_send_email(
    ctx: Context,
    to: str | list[str],
    subject: str | None = None,
    from_address: str | None = None,
    html: str | None = None,
    text: str | None = None,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    reply_to: list[str] | None = None,
    template_id: str | None = None,
    scheduled_at: str | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Send a single transactional email.

    Uses USESEND_DEFAULT_FROM if from_address is omitted; subject may be omitted only
    if template_id supplies one.
    """
    default_from = ctx.lifespan_context.get("default_from")
    item = BatchEmailItem(
        to=to,
        subject=subject,
        from_address=from_address,
        html=html,
        text=text,
        cc=cc,
        bcc=bcc,
        reply_to=reply_to,
        template_id=template_id,
        scheduled_at=scheduled_at,
    )
    data = await _client(ctx).request("POST", "/v1/emails", json=_email_body(item, default_from))
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Batch send emails"))
@map_domain_errors
async def usesend_batch_send_emails(
    ctx: Context, emails: list[BatchEmailItem], response_format: ResponseFormat = "markdown"
) -> str:
    """Send up to 100 emails in a single request."""
    default_from = ctx.lifespan_context.get("default_from")
    payload = [_email_body(item, default_from) for item in emails]
    data = await _client(ctx).request("POST", "/v1/emails/batch", json=payload)
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="List emails", readOnlyHint=True))
@map_domain_errors
async def usesend_list_emails(
    ctx: Context,
    page: int = 1,
    limit: int = 50,
    start_date: str | None = None,
    end_date: str | None = None,
    domain_id: str | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """List emails with pagination; optional ISO-8601 date range and domain filter."""
    params: dict[str, Any] = {"page": page, "limit": limit}
    if start_date is not None:
        params["startDate"] = start_date
    if end_date is not None:
        params["endDate"] = end_date
    if domain_id is not None:
        params["domainId"] = domain_id
    data = await _client(ctx).request("GET", "/v1/emails", params=params)
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Get email", readOnlyHint=True))
@map_domain_errors
async def usesend_get_email(
    ctx: Context, email_id: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Get details for a specific email."""
    data = await _client(ctx).request("GET", f"/v1/emails/{email_id}")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Cancel scheduled email", destructiveHint=True))
@map_domain_errors
async def usesend_cancel_email(
    ctx: Context, email_id: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Cancel a scheduled email."""
    data = await _client(ctx).request("POST", f"/v1/emails/{email_id}/cancel")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Update email schedule"))
@map_domain_errors
async def usesend_update_email_schedule(
    ctx: Context, email_id: str, scheduled_at: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Reschedule a scheduled email."""
    data = await _client(ctx).request(
        "PATCH", f"/v1/emails/{email_id}", json={"scheduledAt": scheduled_at}
    )
    return format_response(data, response_format)
