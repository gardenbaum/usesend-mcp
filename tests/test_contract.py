"""Snapshot of the served capability surface — the reviewed MCP API contract.

The snapshot captures every tool, resource, resource template, and prompt with its
name, description, and input/output JSON schema. Changing the surface must be a
deliberate act: regenerate with ``just snapshot-update`` (or ``pytest
--snapshot-update``) and review the resulting diff. Lists are sorted by identity and
syrupy serializes mappings with sorted keys, so the snapshot is deterministic.
"""

from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport
from syrupy.assertion import SnapshotAssertion

DESTRUCTIVE_TOOLS = {
    "usesend_cancel_email",
    "usesend_delete_campaign",
    "usesend_pause_campaign",
    "usesend_delete_contact_book",
    "usesend_delete_contact",
    "usesend_bulk_delete_contacts",
    "usesend_delete_domain",
}


async def test_destructive_tools_carry_destructive_hint(
    client: Client[FastMCPTransport],
) -> None:
    """Delete/cancel/pause tools advertise destructiveHint so clients can warn first."""
    by_name = {tool.name: tool for tool in await client.list_tools()}
    for name in DESTRUCTIVE_TOOLS:
        annotations = by_name[name].annotations
        assert annotations is not None, name
        assert annotations.destructiveHint is True, name
    # Read-only and additive tools must not be flagged destructive.
    for name in ("usesend_list_emails", "usesend_resume_campaign", "usesend_send_email"):
        annotations = by_name[name].annotations
        assert annotations is None or annotations.destructiveHint is not True, name


async def test_capability_surface_contract(
    client: Client[FastMCPTransport], snapshot: SnapshotAssertion
) -> None:
    tools = sorted(await client.list_tools(), key=lambda item: item.name)
    resources = sorted(await client.list_resources(), key=lambda item: str(item.uri))
    templates = sorted(await client.list_resource_templates(), key=lambda item: item.uriTemplate)
    prompts = sorted(await client.list_prompts(), key=lambda item: item.name)

    surface: dict[str, object] = {
        "tools": [item.model_dump(mode="json", exclude_none=True) for item in tools],
        "resources": [item.model_dump(mode="json", exclude_none=True) for item in resources],
        "resource_templates": [
            item.model_dump(mode="json", exclude_none=True) for item in templates
        ],
        "prompts": [item.model_dump(mode="json", exclude_none=True) for item in prompts],
    }
    assert surface == snapshot
