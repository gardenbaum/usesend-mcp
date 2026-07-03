"""Render API payloads as markdown (human-readable) or JSON (machine-readable)."""

from __future__ import annotations

import json
from typing import Any, Literal, cast

ResponseFormat = Literal["markdown", "json"]


def format_response(data: Any, response_format: ResponseFormat = "markdown") -> str:
    """Format an API payload for return to the MCP client."""
    if response_format == "json":
        return json.dumps(data, indent=2, sort_keys=True, default=str, ensure_ascii=False)
    return _to_markdown(data)


def _to_markdown(data: Any) -> str:
    """Convert data to markdown representation."""
    if data is None:
        return "OK"
    if isinstance(data, list):
        return _list_to_table(cast(list[Any], data))
    if isinstance(data, dict):
        return _dict_to_kv(cast(dict[str, Any], data))
    return str(data)


def _dict_to_kv(data: dict[str, Any]) -> str:
    """Convert dictionary to key-value markdown list."""
    return "\n".join(f"- **{key}**: {_scalar(value)}" for key, value in data.items())


def _list_to_table(rows: list[Any]) -> str:
    """Convert list to markdown table or bullet list."""
    if not rows:
        return "_Keine Einträge._"
    if not all(isinstance(row, dict) for row in rows):
        return "\n".join(f"- {_scalar(row)}" for row in rows)
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(_scalar(row.get(col, "")) for col in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def _scalar(value: Any) -> str:
    """Convert a value to a scalar string representation."""
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, default=str)
    else:
        text = str(value)
    text = text.replace("\n", " ").replace("\r", " ")
    return text.replace("|", "\\|")
