"""useSend email tools."""

from typing import Any

from fastmcp import Context
from fastmcp.server.providers import LocalProvider
from mcp.types import ToolAnnotations

from usesend_mcp.errors import ValidationFailedError, map_domain_errors
from usesend_mcp.formatting import ResponseFormat, format_response
from usesend_mcp.models.emails import Attachment, BatchEmailItem

provider = LocalProvider()

_MAX_BATCH_EMAILS = 100  # useSend openapi.json: batch maxItems


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
        (item.variables, "variables"),
        (item.headers, "headers"),
        (item.scheduled_at, "scheduledAt"),
        (item.in_reply_to_id, "inReplyToId"),
    ):
        if src is not None:
            body[dst] = src
    if item.attachments is not None:
        body["attachments"] = [a.model_dump() for a in item.attachments]
    return body


@provider.tool(annotations=ToolAnnotations(title="Send email", openWorldHint=True))
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
    variables: dict[str, str] | None = None,
    attachments: list[Attachment] | None = None,
    headers: dict[str, str] | None = None,
    scheduled_at: str | None = None,
    in_reply_to_id: str | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Send a single transactional email.

    Uses USESEND_DEFAULT_FROM if from_address is omitted; subject may be omitted only
    if template_id supplies one. variables fill template placeholders; attachments carry
    base64 content; in_reply_to_id threads a reply.
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
        variables=variables,
        attachments=attachments,
        headers=headers,
        scheduled_at=scheduled_at,
        in_reply_to_id=in_reply_to_id,
    )
    data = await _client(ctx).request("POST", "/v1/emails", json=_email_body(item, default_from))
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Batch send emails", openWorldHint=True))
@map_domain_errors
async def usesend_batch_send_emails(
    ctx: Context, emails: list[BatchEmailItem], response_format: ResponseFormat = "markdown"
) -> str:
    """Send up to 100 emails in a single request."""
    if not emails:
        raise ValidationFailedError("Mindestens eine E-Mail erforderlich.")
    if len(emails) > _MAX_BATCH_EMAILS:
        raise ValidationFailedError(f"Maximal {_MAX_BATCH_EMAILS} E-Mails pro Batch.")
    default_from = ctx.lifespan_context.get("default_from")
    payload = [_email_body(item, default_from) for item in emails]
    data = await _client(ctx).request("POST", "/v1/emails/batch", json=payload)
    return format_response(data, response_format)


@provider.tool(
    annotations=ToolAnnotations(
        title="List emails", readOnlyHint=True, idempotentHint=True, openWorldHint=True
    )
)
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


@provider.tool(
    annotations=ToolAnnotations(
        title="Get email", readOnlyHint=True, idempotentHint=True, openWorldHint=True
    )
)
@map_domain_errors
async def usesend_get_email(
    ctx: Context, email_id: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Get details for a specific email."""
    data = await _client(ctx).request("GET", f"/v1/emails/{email_id}")
    return format_response(data, response_format)


@provider.tool(
    annotations=ToolAnnotations(
        title="Cancel scheduled email", destructiveHint=True, openWorldHint=True
    )
)
@map_domain_errors
async def usesend_cancel_email(
    ctx: Context, email_id: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Cancel a scheduled email."""
    data = await _client(ctx).request("POST", f"/v1/emails/{email_id}/cancel")
    return format_response(data, response_format)


@provider.tool(annotations=ToolAnnotations(title="Update email schedule", openWorldHint=True))
@map_domain_errors
async def usesend_update_email_schedule(
    ctx: Context, email_id: str, scheduled_at: str, response_format: ResponseFormat = "markdown"
) -> str:
    """Reschedule a scheduled email."""
    data = await _client(ctx).request(
        "PATCH", f"/v1/emails/{email_id}", json={"scheduledAt": scheduled_at}
    )
    return format_response(data, response_format)
