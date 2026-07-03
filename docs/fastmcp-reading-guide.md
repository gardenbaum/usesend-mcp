# FastMCP 3 — Reading Guide (Relevance Triage for usesend-mcp)

Curated map of the vendored FastMCP docs (`docs/vendor/fastmcp/docs/`) for building
**usesend-mcp**: a Python / FastMCP 3 MCP server, likely wrapping the usesend REST API.

**Deployment:** internal HTTP service **+** public remote server → auth & HTTP are core.
**Planned features:** interactive UIs (usesend test reports as dashboards/charts) and an
own MCP client component.

Paths below are relative to `docs/vendor/fastmcp/docs/`.

> **What is vendored:** only the `docs/` subtree. A conservative
> prune (`just docs-sync`) drops what we never need: `v2/` (legacy FastMCP 2),
> `development/{contributing,releases,tests}.mdx` (contributing to FastMCP itself), and
> FastMCP's own repo-root files (incl. its `CLAUDE.md`/`AGENTS.md`). Images and
> Mintlify site assets (`assets/`, `css/`, `public/`, `*.js`) are *kept* but irrelevant —
> ignore them.

---

## 🟢 Core — read first (the foundation)

- `getting-started/welcome.mdx · installation.mdx · quickstart.mdx`
- `servers/server.mdx` — the `FastMCP` instance, central API
- `servers/tools.mdx` — **most important**; tools are the product
- `servers/resources.mdx` · `servers/prompts.mdx` — the other two component types
- `servers/context.mdx` — `Context`: logging, progress, sampling, state — used everywhere
- `servers/testing.mdx` + `patterns/testing.mdx` — in-memory client, no network needed
- `development/v3-notes/v3-features.mdx` — what's new in v3 (training data may be stale)
- `integrations/fastapi.mdx · integrations/openapi.mdx` — **wrap the existing usesend REST API as an MCP server** (likely the backbone of usesend-mcp)

### Auth & HTTP — core for this project (both deployment modes)

- `servers/auth/authentication.mdx` — overview / decision spectrum
- `servers/auth/token-verification.mdx` — **internal HTTP**: server as pure resource server validating JWTs from existing SSO/gateway
- public IdP, pick ONE matching the provider:
  - DCR providers (WorkOS AuthKit, Descope, modern OIDC) → `servers/auth/remote-oauth.mdx` (`RemoteAuthProvider`)
  - traditional providers (Azure AD, Google, GitHub, AWS Cognito) → `servers/auth/oauth-proxy.mdx` + `servers/auth/oidc-proxy.mdx`
- `servers/auth/multi-auth.mdx` — ⭐ combine multiple auth schemes (one server serving both internal + public)
- `clients/auth/bearer.mdx · oauth.mdx` — auth from the client side (testing + own client)
- `deployment/http.mdx · server-configuration.mdx · running-server.mdx`
- `integrations/<your-idp>.mdx` — the one file matching your public IdP (azure / workos / aws-cognito / auth0 / …), once decided

> ⚠️ Docs warn: MCP auth is rapidly evolving. Always check the local docs first.

---

## 🟡 Important — read soon

**Server quality & architecture**
- `servers/middleware.mdx` — cross-cutting: logging, error handling, timing
- `servers/dependency-injection.mdx` · `servers/lifespan.mdx` — usesend connection/session at startup
- `servers/logging.mdx` · `servers/progress.mdx` — long-running usesend runs → progress + structured logs
- `servers/tasks.mdx` — **v3, NEW**: long-running async operations — relevant for test runs
- `servers/providers/overview.mdx · local.mdx · custom.mdx` — the "Provider model"; modularize the server
- `servers/composition.mdx` — mount sub-servers (modularity)
- `cli/overview.mdx · running.mdx · inspecting.mdx` — dev workflow, inspect/debug
- `more/faq.mdx · settings.mdx` — reference

**Apps — interactive UIs (planned: usesend test-report dashboards)**
- `apps/overview.mdx · quickstart.mdx` — start here
- `apps/prefab.mdx` — interactive tools (`@mcp.tool(app=True)` → charts/tables/dashboards)
- `apps/fastmcp-app.mdx` — when the UI calls back to the server (forms, buttons)
- `apps/architecture.mdx · development.mdx · examples.mdx` — building & patterns
- `apps/generative.mdx · low-level.mdx` — LLM-written UI / custom HTML (advanced)

**Clients — building an own MCP client component**
- `clients/client.mdx · transports.mdx` — core client + transports
- `clients/tools.mdx · resources.mdx · prompts.mdx` — calling components
- `clients/sampling.mdx · elicitation.mdx · roots.mdx` — client-side capabilities the server may use
- `clients/progress.mdx · logging.mdx · notifications.mdx · tasks.mdx` — handling server events
- `clients/auth/*` (see Auth above)

---

## 🟠 Situational — read when the case arises

- `servers/sampling.mdx` · `servers/elicitation.mdx` — only if the server calls back to the LLM / asks the user
- `servers/transforms/tool-search.mdx · code-mode.mdx` — only with a LARGE tool catalog (on-demand search); ignore with few tools
- `servers/transforms/tool-transformation.mdx · namespace.mdx` — rename/reshape tools, esp. when composing
- `servers/providers/proxy.mdx · filesystem.mdx · skills.mdx` — proxying / dynamic sources
- `servers/storage-backends.mdx · pagination.mdx · versioning.mdx · telemetry.mdx · visibility.mdx · icons.mdx · tool-fingerprinting.mdx` — specialist topics
- `servers/authorization.mdx` — fine-grained authz beyond authn
- `tutorials/create-mcp-server.mdx · mcp.mdx · rest-api.mdx` — guided walkthroughs (rest-api ≈ the usesend-wrapping case)
- `python-sdk/` (61 files) — **API reference, do not read through** — look up as needed
- `integrations/pydantic-ai.mdx` — if consuming the server from an agent framework
- `integrations/{claude-code,claude-desktop,cursor,gemini-cli}.mdx` — the ones matching your actual test clients
- `cli/{auth,client,generate-cli,install-mcp}.mdx` · `clients/{cli,fastmcp-remote,client-only-package,generate-cli}.mdx`

---

## 🔴 Skip — not relevant (and mostly not even vendored)

- **`v2/`** — REMOVED by prune. Legacy FastMCP 2; this project is v3
- **`development/{contributing,releases,tests}.mdx`** — REMOVED by prune; for contributing to FastMCP itself (kept: `development/v3-notes/`)
- **FastMCP repo-root files** (its own `CLAUDE.md`, `pyproject.toml`, etc.) — not vendored
- `servers/auth/full-oauth-server.mdx` — only if usesend-mcp itself becomes the identity provider
- most other `integrations/` (Supabase, Discord, OCI, Descope, Keycloak, Permit, Eunomia, Scalekit, PropelAuth, Anthropic/OpenAI/Gemini/Google client integrations, …) — only read the one matching a service you actually use
- `deployment/{prefect-horizon,sandboxed-agents}.mdx` — Prefect's hosted platform
- `community/` · `patterns/contrib.mdx`
- **Retained in repo but ignore:** `assets/`, `css/`, `public/`, `snippets/`, `*.js`, all images — Mintlify site assets, no value for code/reference
