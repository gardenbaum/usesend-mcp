"""Application configuration for the usesend MCP server (env prefix ``USESEND_``)."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Runtime configuration, overridable via ``USESEND_*`` environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="USESEND_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_key: str | None = None
    base_url: str = "https://app.usesend.com"
    default_from: str | None = None
    log_level: LogLevel = "INFO"
    timeout: float = 30.0
    server_name: str = "usesend MCP"
