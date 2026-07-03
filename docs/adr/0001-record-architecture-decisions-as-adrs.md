---
status: "accepted"
date: "2026-06-03"
---

# Record architecture decisions as ADRs

## Context and Problem Statement

usesend-mcp is a FastMCP 3 server that wraps the useSend email platform's REST
API. The rationale behind architecturally significant choices currently lives
implicitly in code and commit messages, where it is hard to find and easy to
lose. How do we capture *why* decisions were made so the reasoning survives
turnover and can be reviewed alongside the code?

## Considered Options

- Lightweight ADRs (MADR) committed in the repo under `docs/adr/`.
- An external wiki / Confluence space.
- No formal record — rely on commit history and tribal knowledge.

## Decision Outcome

Chosen option: "Lightweight ADRs in the repo", because the rationale then lives
next to the code, is versioned and reviewed through the same pull-request flow,
and needs no extra tooling or access. We use the [MADR](https://adr.github.io/madr/)
format in `docs/adr/`, numbered sequentially. ADRs are informational and are
**not** wired into any CI gate.

### Consequences

- Good, because decisions are discoverable, versioned, and reviewable with the
  change that introduces them.
- Good, because the format is lightweight enough to actually be used.
- Bad, because it takes discipline to write an ADR when a decision is made and to
  mark records superseded when they are reversed.

## More Information

Template: [`0000-template.md`](0000-template.md). Index: [`README.md`](README.md).
