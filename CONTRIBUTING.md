# Contributing to usesend-mcp

Thanks for your interest in improving **usesend-mcp**! This document explains how to
set up a development environment, the quality bar every change must clear, and how to
propose changes.

By participating you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

- **Report a bug** — open a [bug report](https://github.com/gardenbaum/usesend-mcp/issues/new?template=bug_report.yml).
- **Request a feature** — open a [feature request](https://github.com/gardenbaum/usesend-mcp/issues/new?template=feature_request.yml).
- **Report a security issue** — please do **not** open a public issue; see [SECURITY.md](SECURITY.md).
- **Improve docs or code** — open a pull request (see below).

For anything larger than a small fix, please open an issue first so we can agree on the
approach before you invest time.

## Development setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and
[just](https://github.com/casey/just) as a task runner. Python **3.13+** is required.

```bash
git clone https://github.com/gardenbaum/usesend-mcp.git
cd usesend-mcp
uv sync --dev          # install runtime + dev dependencies into .venv
just check             # run the full quality gate (see below)
```

You can run the server locally against a real useSend instance with:

```bash
USESEND_API_KEY=us_your_api_key_here just run
```

## Quality gate

Every change must pass `just check` before it can be merged — CI runs the same steps.
It bundles:

| Step | Command | What it enforces |
|---|---|---|
| Lint | `just lint` | `ruff check` (pycodestyle, pyflakes, bugbear, security `S`, pydocstyle `D`, …) |
| Format | `just format-check` | `ruff format` |
| Types | `just typecheck` | `basedpyright` in **strict** mode |
| Architecture | `just imports` | import-linter layering contracts |
| Dependencies | `just deps` | `deptry` (no unused / missing / misplaced deps) |
| Tests + coverage | `just cov-diff` | `pytest` with **100% diff coverage** on changed lines |

Additional useful recipes:

- `just test` — run the test suite only.
- `just cov` — full coverage report.
- `just audit` — `pip-audit` supply-chain scan of the locked dependencies.
- `just snapshot-update` — regenerate the tool-surface contract snapshot after an
  intentional change to the exposed tools (`tests/__snapshots__/test_contract.ambr`).
- `just docs-sync-all` — refresh the vendored FastMCP docs and useSend OpenAPI spec.

## Coding conventions

- **Curated tools.** Tools are hand-authored and verified against the vendored useSend
  OpenAPI spec (`docs/vendor/usesend/openapi.json`) — see
  [ADR 0003](docs/adr/0003-curated-tools-over-openapi-generation.md). When you add or
  change a tool, verify its shape against the spec and update the contract snapshot.
- **Layering.** Respect the `cli → server → components → client → models` layering
  enforced by import-linter — see [ADR 0002](docs/adr/0002-fastmcp-3-provider-model-with-composition-root.md).
- **stdio discipline.** `stdout` is reserved for the MCP protocol; all logging goes to
  `stderr`. Never `print()` to stdout from server code.
- **Type everything.** The codebase is fully typed and `basedpyright` runs in strict
  mode. New code must not introduce `Any` leaks or `# type: ignore` without a reason.

## Architecture Decision Records

Architecturally significant decisions are recorded as lightweight
[MADR](https://adr.github.io/madr/) ADRs in [`docs/adr/`](docs/adr/). If your change
makes such a decision, add an ADR using [`0000-template.md`](docs/adr/0000-template.md).

## Pull requests

1. Fork the repo and create a topic branch off `main`.
2. Make your change, keeping commits focused.
3. Ensure `just check` is green.
4. Write commit messages in the [Conventional Commits](https://www.conventionalcommits.org)
   style (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`, `build:`, `chore:`).
5. Open the PR against `main` and fill in the template. Link any related issue.
6. CI must pass and the branch must be up to date with `main` before merge.

Maintainers merge via squash to keep a linear, readable history.

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE) that covers this project.
