"""Structured JSON logging for the usesend MCP server.

``configure_logging`` installs :class:`JsonFormatter` on a stderr :class:`~logging.StreamHandler`
on the root logger (stdout is reserved for the stdio MCP transport), so every record is
emitted as a single-line JSON object. The formatter enriches each record with the
current request id read from :data:`request_id_var`, which callers may set to correlate
related log records.
"""

import json
import logging
import sys
from contextvars import ContextVar
from datetime import UTC, datetime

# May be set by callers to correlate related log records. Defaults to None for
# records emitted with no id bound (e.g. startup/shutdown).
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)

# Standard LogRecord attributes (plus the two added during formatting). Anything
# else found on a record is treated as a caller-supplied "extra" and serialized.
_RESERVED_ATTRS = frozenset(vars(logging.makeLogRecord({}))) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    """Serialize a :class:`logging.LogRecord` as a single-line JSON object."""

    def format(self, record: logging.LogRecord) -> str:
        """Render ``record`` as JSON with timestamp, level, logger, message, extras.

        The current request id (when set) and any caller-supplied ``extra`` fields
        are included; an exception, if attached, is rendered into ``exc_info``.

        Args:
            record: The log record to serialize.

        Returns:
            A JSON string (the handler appends the trailing newline).
        """
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        request_id = request_id_var.get()
        if request_id is not None:
            payload["request_id"] = request_id
        for key, value in record.__dict__.items():
            if key not in _RESERVED_ATTRS:
                payload[key] = value
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def configure_logging(level: str) -> None:
    """Configure root logging to emit JSON via :class:`JsonFormatter`.

    Args:
        level: A standard logging level name (e.g. ``"INFO"``).
    """
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=level, handlers=[handler], force=True)
