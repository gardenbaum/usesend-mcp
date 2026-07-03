---
status: "accepted"
date: "2026-06-03"
---

# FastMCP 3 Provider model with a composition root

## Context and Problem Statement

usesend-mcp exposes capabilities across several useSend domains (emails, contact
books, contacts, campaigns, domains, analytics) over MCP and is expected to grow
domain by domain. It is also served through three start methods (the `usesend-mcp`
console script, `python -m usesend_mcp`, and `fastmcp run fastmcp.json`), all over
stdio. We need
a wiring approach that keeps domains modular and independently testable, gives a
single obvious place to assemble the server, and behaves consistently across all
entrypoints.

## Considered Options

- **FastMCP 3 Provider model + composition root** — each domain is a standalone
  `LocalProvider`; a single no-arg `create_server()` factory assembles them via
  `FastMCP(providers=[...])`.
- **Monolithic server** — register every tool/resource inline on one `FastMCP`
  instance.
- **Sub-server composition** — build a `FastMCP` per domain and mount them.

## Decision Outcome

Chosen option: "Provider model + composition root", because it isolates each
domain behind a `LocalProvider` (under `src/usesend_mcp/components/`) while keeping
exactly one wiring location, `create_server()` in `src/usesend_mcp/server.py`. That
factory is also the `fastmcp.json` entrypoint, and `cli.py` (via `__main__.py` and
the console script) builds on it, so the three start methods stay consistent. import-linter contracts
enforce the layering: providers and server must not import the entrypoints, and
the server layer sits above components. Adding a domain means adding one provider
to the list.

### Consequences

- Good, because domains are decoupled and testable in isolation via the in-memory
  FastMCP client; the composition root is the single source of wiring truth.
- Good, because all entrypoints share one build path, so behavior does not drift
  between them.
- Bad, because the composition root is a shared touchpoint that every new domain
  must edit.
- Bad, because contributors must understand the distinction between ASGI/Starlette
  middleware and FastMCP's own MCP-middleware layer, and the known `fastmcp run`
  middleware limitation (documented in the README).

## More Information

Vendored docs: `docs/vendor/fastmcp/docs/servers/providers/overview.mdx`,
`servers/providers/local.mdx`, `servers/composition.mdx`. Layering is enforced by
the `[tool.importlinter]` contracts in `pyproject.toml`.
