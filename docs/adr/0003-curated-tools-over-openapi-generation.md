---
status: "accepted"
date: "2026-07-02"
---

# Curated tools over OpenAPI generation

## Context and Problem Statement

useSend publishes an OpenAPI spec (now vendored at `docs/vendor/usesend/openapi.json`
via `just usesend-docs-sync`). The goal for this project is a curated MCP server with
clean `usesend_*` tool names, typed parameters, German client-safe error messages, and
stdio-first ergonomics. How should the 33 tools be produced: generated from the spec,
or hand-authored against it?

## Considered Options

- **Hand-authored tools over a typed client, verified against the OpenAPI spec** —
  each tool is a thin, explicitly-named function with typed parameters; the vendored
  `openapi.json` is used to check correctness, not to generate code.
- **OpenAPI code generation** (e.g. `datamodel-codegen` / spec-driven stub generation)
  — derive tool signatures and models mechanically from `openapi.json`.
- **FastMCP's `FastMCP.from_openapi` auto-proxy** — point FastMCP directly at the
  spec and let it synthesize tools at runtime.

## Decision Outcome

Chosen option: "Hand-authored tools, OpenAPI-verified", because it is the only
option that delivers the curated UX this project exists for. Generated or
auto-proxied tool names and parameter shapes follow the spec's raw operation IDs
and schemas — noisy, inconsistent with the `usesend_*` naming and `response_format`
convention, and without room for the German, client-safe error mapping in
`map_domain_errors` (ADR 0002's component layer). Instead, Task 12 used
`openapi.json` purely for verification: it aligned all 33 tools to the spec and
fixed real mismatches (e.g. campaign create's `from` field, upsert-contact's path
segment, analytics query param names).

### Consequences

- Good, because tool names, parameter types, and error messages are fully under our
  control and consistent with the rest of the codebase.
- Good, because the `response_format` (markdown/json) convention applies uniformly —
  something neither generation nor auto-proxying would produce on its own.
- Good, because the capability-surface snapshot (`tests/__snapshots__/test_contract.ambr`)
  guards the hand-authored surface from silent drift.
- Bad, because each new or changed useSend endpoint requires a hand-added tool
  instead of a re-run of a generator; keeping current is a manual process.
- Bad, because staying aligned with upstream requires discipline: run
  `just docs-sync-all` to refresh the vendored spec, re-verify tools against it, and
  regenerate the contract snapshot (`just snapshot-update`) when the surface changes.

## More Information

Verification work: commit `cde7596` ("docs: vendor useSend API docs + sync recipes;
align tools to OpenAPI"). Related: ADR 0002 (component/provider layering that hosts
the tools and error mapping). Vendored spec: `docs/vendor/usesend/openapi.json`.
