"""Formatter tests."""

import json

from usesend_mcp.formatting import format_response


def test_json_is_sorted_and_indented() -> None:
    out = format_response({"b": 1, "a": 2}, "json")
    assert json.loads(out) == {"a": 2, "b": 1}
    assert out.index('"a"') < out.index('"b"')


def test_markdown_dict_is_key_value() -> None:
    out = format_response({"id": "e_1", "status": "sent"}, "markdown")
    assert "**id**" in out and "e_1" in out
    assert "**status**" in out and "sent" in out


def test_markdown_list_is_table() -> None:
    out = format_response([{"id": "a"}, {"id": "b"}], "markdown")
    assert "| id |" in out
    assert "| a |" in out and "| b |" in out


def test_markdown_empty_list() -> None:
    assert "keine" in format_response([], "markdown").lower()


def test_markdown_scalar_falls_back_to_str() -> None:
    assert format_response("just text", "markdown") == "just text"
    assert format_response(42, "markdown") == "42"


def test_markdown_list_of_non_dicts_is_bullet_list() -> None:
    out = format_response(["a", "b"], "markdown")
    assert out == "- a\n- b"


def test_markdown_nested_value_is_json_dumped() -> None:
    out = format_response({"meta": {"x": 1}}, "markdown")
    assert '**meta**: {"x": 1}' in out


def test_markdown_none_renders_ok() -> None:
    assert format_response(None, "markdown") == "OK"


def test_json_none_renders_null() -> None:
    assert format_response(None, "json") == "null"


def test_markdown_table_cell_escapes_pipe_and_newline() -> None:
    out = format_response([{"note": "a|b\nc"}], "markdown")
    lines = out.splitlines()
    assert lines[0] == "| note |"
    assert lines[1] == "| --- |"
    assert lines[2] == "| a\\|b c |"
