"""Settings tests."""

import pytest
from pydantic import ValidationError

from usesend_mcp.settings import Settings


def test_defaults_without_api_key() -> None:
    s = Settings(_env_file=None)  # type: ignore[call-arg]  # hermetic: ignore stray .env
    assert s.api_key is None
    assert s.base_url == "https://app.usesend.com"
    assert s.default_from is None
    assert s.log_level == "INFO"
    assert s.timeout == 30.0
    assert s.server_name == "usesend MCP"


def test_env_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("USESEND_API_KEY", "us_abc")
    monkeypatch.setenv("USESEND_BASE_URL", "https://self.hosted")
    monkeypatch.setenv("USESEND_DEFAULT_FROM", "no-reply@x.io")
    s = Settings()
    assert s.api_key == "us_abc"
    assert s.base_url == "https://self.hosted"
    assert s.default_from == "no-reply@x.io"


def test_invalid_log_level() -> None:
    with pytest.raises(ValidationError):
        Settings(log_level="TRACE")  # type: ignore[arg-type]
