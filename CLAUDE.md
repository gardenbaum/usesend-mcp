# usesend-mcp

## FastMCP 3 — start here

**Before any FastMCP work (questions, design, or code), read
`docs/fastmcp-reading-guide.md` first.** It is a curated relevance triage of the vendored
docs for this project: it tells you which of the 286 `.mdx` files matter for usesend-mcp and
which to ignore. Use it as the entry point, then open the specific vendored docs it points
to rather than recalling API shapes from memory — the v3 API is new and training data may
be stale.

## FastMCP 3 documentation (vendored)

This project targets **FastMCP 3** (Provider model). The upstream docs are vendored
**into the repo** so every dev (and Claude) has them by default on clone — no setup step:

- Location: `docs/vendor/fastmcp/docs/` (286 `.mdx` files, committed)
- Source commit: `docs/vendor/fastmcp/UPSTREAM_COMMIT.txt`
- Refresh to latest upstream: `just docs-sync`
- Which files matter: see `docs/fastmcp-reading-guide.md` (the triage above)
