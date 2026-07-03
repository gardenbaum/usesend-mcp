# Architecture Decision Records

Architecturally significant decisions for **usesend-mcp** are recorded here as
lightweight [MADR](https://adr.github.io/madr/) files, committed alongside the
code that realizes them. ADRs are informational — they are **not** wired into
any CI gate.

## Conventions

- One decision per file, named `NNNN-kebab-case-title.md` with a zero-padded,
  monotonically increasing number.
- Copy [`0000-template.md`](0000-template.md) to start a new record.
- A decision is rarely deleted. When it is reversed, add a new ADR and set the
  superseded one's `status` to `superseded by ADR-NNNN`.

## Records

- [0001 — Record architecture decisions as ADRs](0001-record-architecture-decisions-as-adrs.md)
- [0002 — FastMCP 3 Provider model with a composition root](0002-fastmcp-3-provider-model-with-composition-root.md)
- [0003 — Curated tools over OpenAPI generation](0003-curated-tools-over-openapi-generation.md)
