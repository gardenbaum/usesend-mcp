"""usesend MCP — a FastMCP server exposing usesend over MCP."""

from importlib.metadata import PackageNotFoundError as _PackageNotFoundError
from importlib.metadata import version as _version

try:
    __version__ = _version("usesend-mcp")
except _PackageNotFoundError:  # pragma: no cover - only during uninstalled use
    __version__ = "0.0.0"

__all__ = ["__version__"]
