"""Domain error hierarchy and the single MCP error-mapping boundary.

Domain code raises subclasses of :class:`UsesendMcpError`, which carry a client-safe
message and stay decoupled from the MCP layer. :func:`map_domain_errors` is the one
place that translates them into a FastMCP :class:`~fastmcp.exceptions.ToolError` at
the tool boundary; a ``ToolError`` message is delivered to the client verbatim. Every
other (unexpected) exception is masked by the server's ``mask_error_details=True``
setting, so no stack trace or internal detail ever reaches the client.

The mapping lives at the tool boundary, not in MCP middleware: FastMCP's tool runner
catches and masks a tool's exception *below* the middleware chain, so an
``on_call_tool`` hook cannot deliver a sanitized domain message — only raising
``ToolError`` from within the tool can.
"""

from collections.abc import Awaitable, Callable
from functools import wraps

from fastmcp.exceptions import ToolError


class UsesendMcpError(Exception):
    """Base class for domain errors raised by usesend-mcp.

    The string message is considered client-safe and is surfaced verbatim by
    :func:`map_domain_errors`; never put secrets or internal detail in it.
    """


class NotFoundError(UsesendMcpError):
    """A requested entity or resource does not exist."""


class UpstreamError(UsesendMcpError):
    """An upstream dependency (e.g. the usesend API) failed."""


class AuthError(UsesendMcpError):
    """Authentication failed (missing/invalid API key)."""


class PermissionDeniedError(UsesendMcpError):
    """The API key lacks permission for this operation."""


class ConflictError(UsesendMcpError):
    """The request conflicts with current state (e.g. idempotency)."""


class ValidationFailedError(UsesendMcpError):
    """The request payload was rejected as invalid."""


class RateLimitError(UsesendMcpError):
    """The API rate limit was exceeded."""


def error_for_status(status_code: int, detail: str | None) -> UsesendMcpError:
    """Map an HTTP status code to a client-safe domain error (German messages)."""
    suffix = f" ({detail})" if detail else ""
    error: UsesendMcpError
    match status_code:
        case 401:
            error = AuthError("Ungültiger oder fehlender API-Key — USESEND_API_KEY prüfen.")
        case 403:
            error = PermissionDeniedError("Zugriff verweigert — API-Key-Berechtigungen prüfen.")
        case 404:
            error = NotFoundError(f"Ressource nicht gefunden — ID prüfen.{suffix}")
        case 409:
            error = ConflictError(f"Konflikt mit aktuellem Zustand.{suffix}")
        case 422:
            error = ValidationFailedError(f"Ungültige Anfrage.{suffix}")
        case 429:
            error = RateLimitError("Rate-Limit erreicht — kurz warten und erneut versuchen.")
        case _:
            error = UpstreamError("useSend-API vorübergehend nicht verfügbar.")
    return error


def map_domain_errors[**P, R](func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    """Translate a :class:`UsesendMcpError` raised by an async tool into ``ToolError``.

    Wrap a tool coroutine so domain errors cross the MCP boundary as a
    :class:`~fastmcp.exceptions.ToolError` carrying only the domain message — never a
    stack trace or wrapped-cause details. Non-domain exceptions are left untouched for
    the server's error masking to handle.

    Args:
        func: The tool coroutine function to wrap.

    Returns:
        The wrapped coroutine function, with the original signature preserved.
    """

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await func(*args, **kwargs)
        except UsesendMcpError as exc:
            # `from None`: keep the internal cause chain (and any wrapped secrets) off
            # the boundary exception entirely, matching this module's no-leak contract.
            raise ToolError(str(exc)) from None

    return wrapper
