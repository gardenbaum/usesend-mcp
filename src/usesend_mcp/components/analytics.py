"""useSend analytics tools."""

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
    """Build query params from kwargs, dropping ``None`` values and camelCasing keys."""
    return {_to_camel_case(key): value for key, value in kwargs.items() if value is not None}


@provider.tool(
    annotations=ToolAnnotations(
        title="Email time series", readOnlyHint=True, idempotentHint=True, openWorldHint=True
    )
)
@map_domain_errors
async def usesend_email_time_series(
    ctx: Context,
    days: str | None = None,
    domain_id: str | None = None,
    response_format: ResponseFormat = "markdown",
) -> str:
    """Get email volume time series analytics.

    days is "7" or "30" (default 30); domain_id optionally filters to one domain.
    """
    params = _compact(days=days, domain_id=domain_id)
    data = await _client(ctx).request("GET", "/v1/analytics/email-time-series", params=params)
    return format_response(data, response_format)


@provider.tool(
    annotations=ToolAnnotations(
        title="Reputation metrics", readOnlyHint=True, idempotentHint=True, openWorldHint=True
    )
)
@map_domain_errors
async def usesend_reputation_metrics(
    ctx: Context, domain_id: str | None = None, response_format: ResponseFormat = "markdown"
) -> str:
    """Get sending reputation metrics (bounce/complaint rates), optionally for one domain."""
    params = _compact(domain_id=domain_id)
    data = await _client(ctx).request("GET", "/v1/analytics/reputation-metrics", params=params)
    return format_response(data, response_format)
