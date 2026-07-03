"""Contact request models."""

from __future__ import annotations

from pydantic import BaseModel


class ContactInput(BaseModel):
    """One contact for bulk creation (useSend openapi.json: only email required)."""

    email: str
    first_name: str | None = None
    last_name: str | None = None
    subscribed: bool | None = None
    properties: dict[str, object] | None = None
