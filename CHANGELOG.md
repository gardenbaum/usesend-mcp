# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-07-03

### Added

- Initial public release of **usesend-mcp**, a FastMCP 3 stdio server exposing the
  [useSend](https://usesend.com) email platform over the Model Context Protocol.
- **33 curated MCP tools** across six domains: emails (6), contact books (5),
  contacts (8), campaigns (7), domains (5), and analytics (2).
- Optional `response_format` (`markdown` default, or `json`) on every tool.
- Full tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`,
  `openWorldHint`) for safe client-side handling.
- Configuration via `USESEND_*` environment variables (API key, base URL for
  self-hosted instances, default sender, log level, timeout).
- Distribution via PyPI (`uvx usesend-mcp`) and a container image.
- German, client-safe error messages mapped from useSend API failures.

[Unreleased]: https://github.com/gardenbaum/usesend-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/gardenbaum/usesend-mcp/releases/tag/v0.1.0
