"""CLI entrypoint tests."""

import importlib
from unittest.mock import MagicMock, patch

from usesend_mcp import cli


def test_main_runs_stdio() -> None:
    fake = MagicMock()
    with patch.object(cli, "create_server", return_value=fake) as make:
        cli.main([])
    make.assert_called_once()
    fake.run.assert_called_once_with(transport="stdio")


def test_dunder_main_module_imports_cleanly() -> None:
    """``python -m usesend_mcp`` imports ``__main__``; the __name__ guard is not hit here."""
    module = importlib.import_module("usesend_mcp.__main__")
    assert module.main is cli.main
