"""Contact tools: routing + body-shape (_compact, bulk) behavior."""

import json
from typing import Any

import httpx
import pytest
from fastmcp import Client

from tests.conftest import Handler, make_test_lifespan
from usesend_mcp.server import create_server
from usesend_mcp.settings import Settings


async def _call(handler: Handler, tool: str, args: dict[str, Any]) -> str:
    server = create_server(Settings(api_key="us_test"), lifespan=make_test_lifespan(handler))
    async with Client(server) as c:
        result = await c.call_tool(tool, args)
    return result.data


def _record_handler(store: dict[str, Any]) -> Handler:
    def handler(req: httpx.Request) -> httpx.Response:
        store["method"] = req.method
        store["path"] = req.url.path
        return httpx.Response(200, json={"id": "c_1"})

    return handler


B = "/api/v1/contactBooks/cb_1/contacts"
CASES: list[tuple[str, dict[str, Any], str, str]] = [
    ("usesend_list_contacts", {"contact_book_id": "cb_1"}, "GET", B),
    ("usesend_get_contact", {"contact_book_id": "cb_1", "contact_id": "c_1"}, "GET", f"{B}/c_1"),
    ("usesend_create_contact", {"contact_book_id": "cb_1", "email": "a@x.io"}, "POST", B),
    (
        "usesend_update_contact",
        {"contact_book_id": "cb_1", "contact_id": "c_1", "subscribed": False},
        "PATCH",
        f"{B}/c_1",
    ),
    # useSend's PUT route is templated with a trailing {contactId} segment that the
    # handler never reads (upsert is keyed by email) — the segment must still be present
    # for routing to match, so the tool fills it with the (URL-encoded) email. httpx's
    # `url.path` reports the decoded form, hence the plain email below.
    (
        "usesend_upsert_contact",
        {"contact_book_id": "cb_1", "email": "a@x.io"},
        "PUT",
        f"{B}/a@x.io",
    ),
    (
        "usesend_delete_contact",
        {"contact_book_id": "cb_1", "contact_id": "c_1"},
        "DELETE",
        f"{B}/c_1",
    ),
    (
        "usesend_bulk_create_contacts",
        {"contact_book_id": "cb_1", "contacts": [{"email": "a@x.io"}]},
        "POST",
        f"{B}/bulk",
    ),
    (
        "usesend_bulk_delete_contacts",
        {"contact_book_id": "cb_1", "contact_ids": ["c_1"]},
        "DELETE",
        f"{B}/bulk",
    ),
]


@pytest.mark.parametrize(("tool", "args", "method", "path"), CASES)
async def test_contact_tool_routing(
    tool: str, args: dict[str, Any], method: str, path: str
) -> None:
    seen: dict[str, Any] = {}
    out = await _call(_record_handler(seen), tool, args)
    assert seen["method"] == method
    assert seen["path"] == path
    assert "c_1" in out


async def test_create_contact_body_uses_camel_case_and_omits_none() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "c_1"})

    await _call(
        handler,
        "usesend_create_contact",
        {
            "contact_book_id": "cb_1",
            "email": "a@x.io",
            "first_name": "Ada",
            "last_name": "Lovelace",
        },
    )
    assert seen["body"] == {
        "email": "a@x.io",
        "firstName": "Ada",
        "lastName": "Lovelace",
        "subscribed": True,
    }


async def test_upsert_contact_body_omits_none_fields() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "c_1"})

    await _call(handler, "usesend_upsert_contact", {"contact_book_id": "cb_1", "email": "a@x.io"})
    assert seen["body"] == {"email": "a@x.io"}


async def test_bulk_create_contacts_body_is_bare_array() -> None:
    """UseSend's openapi.json declares this requestBody as a bare array, not {"contacts": [...]}."""
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "c_1"})

    contacts = [{"email": "a@x.io"}, {"email": "b@x.io"}]
    await _call(
        handler,
        "usesend_bulk_create_contacts",
        {"contact_book_id": "cb_1", "contacts": contacts},
    )
    assert seen["body"] == contacts


async def test_bulk_create_contacts_serializes_typed_items() -> None:
    """Typed ContactInput items camelCase their keys and drop None (subscribed=False kept)."""
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "c_1"})

    await _call(
        handler,
        "usesend_bulk_create_contacts",
        {
            "contact_book_id": "cb_1",
            "contacts": [
                {"email": "a@x.io", "first_name": "Ada", "subscribed": False},
                {"email": "b@x.io"},
            ],
        },
    )
    assert seen["body"] == [
        {"email": "a@x.io", "firstName": "Ada", "subscribed": False},
        {"email": "b@x.io"},
    ]


async def test_bulk_delete_contacts_body_wraps_ids() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"id": "c_1"})

    await _call(
        handler,
        "usesend_bulk_delete_contacts",
        {"contact_book_id": "cb_1", "contact_ids": ["c_1", "c_2"]},
    )
    assert seen["body"] == {"contactIds": ["c_1", "c_2"]}
