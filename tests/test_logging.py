"""Tests for structured JSON logging configuration."""

import json
import logging
import sys

from usesend_mcp.logging import JsonFormatter, configure_logging, request_id_var


def _record(
    level: int = logging.INFO, msg: str = "hi %s", args: tuple[object, ...] = ("there",)
) -> logging.LogRecord:
    return logging.LogRecord("svc", level, "path.py", 10, msg, args, None)


def test_json_formatter_emits_expected_keys() -> None:
    payload = json.loads(JsonFormatter().format(_record()))
    assert payload["level"] == "INFO"
    assert payload["logger"] == "svc"
    assert payload["message"] == "hi there"
    assert "timestamp" in payload
    assert "request_id" not in payload  # nothing bound outside a request


def test_json_formatter_includes_request_id_when_bound() -> None:
    token = request_id_var.set("req-1")
    try:
        payload = json.loads(JsonFormatter().format(_record()))
    finally:
        request_id_var.reset(token)
    assert payload["request_id"] == "req-1"


def test_json_formatter_includes_extra_fields() -> None:
    record = logging.getLogger("svc").makeRecord(
        "svc", logging.INFO, "p", 1, "m", (), None, extra={"tenant": "acme"}
    )
    payload = json.loads(JsonFormatter().format(record))
    assert payload["tenant"] == "acme"


def test_json_formatter_renders_exception() -> None:
    try:
        raise ValueError("boom")
    except ValueError:
        record = logging.LogRecord("svc", logging.ERROR, "p", 1, "m", (), sys.exc_info())
    payload = json.loads(JsonFormatter().format(record))
    assert "ValueError" in payload["exc_info"]
    assert "boom" in payload["exc_info"]


def test_configure_logging_sets_level() -> None:
    configure_logging("WARNING")
    assert logging.getLogger().level == logging.WARNING


def test_configure_logging_installs_json_formatter() -> None:
    configure_logging("INFO")
    root = logging.getLogger()
    assert root.level == logging.INFO
    assert any(isinstance(handler.formatter, JsonFormatter) for handler in root.handlers)
