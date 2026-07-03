"""Email request models."""

from __future__ import annotations

from pydantic import BaseModel


class BatchEmailItem(BaseModel):
    """One item of a batch-send request."""

    to: str | list[str]
    from_address: str | None = None
    subject: str | None = None  # optional when template_id supplies it (useSend openapi.json)
    html: str | None = None
    text: str | None = None
    cc: list[str] | None = None
    bcc: list[str] | None = None
    reply_to: list[str] | None = None
    template_id: str | None = None
    scheduled_at: str | None = None
