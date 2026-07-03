_default:
    @just --list

# Refresh the vendored FastMCP docs (sparse: only the /docs tree) to the latest upstream.
# The result is committed to the repo so every dev gets it on clone — this recipe is only
# for updating. Only the docs/ subtree is copied (FastMCP's repo-root files, incl. its own
# CLAUDE.md/AGENTS.md, are never vendored). A conservative prune then drops legacy v2 docs
# and FastMCP-internal contributor docs. Records the source commit in UPSTREAM_COMMIT.txt.
docs-sync:
    #!/usr/bin/env bash
    set -euo pipefail
    tmp="$(mktemp -d)"
    trap 'rm -rf "$tmp"' EXIT
    git clone --depth 1 --filter=blob:none --sparse https://github.com/PrefectHQ/fastmcp "$tmp"
    git -C "$tmp" sparse-checkout set docs
    rm -rf docs/vendor/fastmcp
    mkdir -p docs/vendor/fastmcp
    cp -R "$tmp/docs" docs/vendor/fastmcp/docs
    # Conservative prune — drop what is definitely not needed for building usesend-mcp:
    rm -rf docs/vendor/fastmcp/docs/v2                       # legacy FastMCP 2
    rm -f  docs/vendor/fastmcp/docs/development/contributing.mdx \
           docs/vendor/fastmcp/docs/development/releases.mdx \
           docs/vendor/fastmcp/docs/development/tests.mdx    # contributing to FastMCP itself
    git -C "$tmp" rev-parse HEAD > docs/vendor/fastmcp/UPSTREAM_COMMIT.txt
    echo "FastMCP docs synced -> docs/vendor/fastmcp/docs/ ($(find docs/vendor/fastmcp/docs -name '*.mdx' | wc -l | tr -d ' ') mdx, commit $(cat docs/vendor/fastmcp/UPSTREAM_COMMIT.txt))"

# Vendor the current useSend API docs (llms-full.txt + openapi.json + per-endpoint markdown).
usesend-docs-sync:
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p docs/vendor/usesend
    base="https://docs.usesend.com"
    curl -fsSL "$base/llms-full.txt" -o docs/vendor/usesend/llms-full.txt
    curl -fsSL "$base/llms.txt"      -o docs/vendor/usesend/llms.txt
    curl -fsSL "$base/api-reference/openapi.json" -o docs/vendor/usesend/openapi.json
    # Fetch each api-reference page listed in llms.txt as markdown (.md variant).
    grep -oE 'https://docs\.usesend\.com/api-reference/[^)]+\.md' docs/vendor/usesend/llms.txt \
      | sort -u | while read -r url; do
        rel="${url#https://docs.usesend.com/}"
        mkdir -p "docs/vendor/usesend/$(dirname "$rel")"
        curl -fsSL "$url" -o "docs/vendor/usesend/$rel"
      done
    date -u +"%Y-%m-%dT%H:%M:%SZ" > docs/vendor/usesend/FETCHED_AT.txt
    echo "useSend docs synced -> docs/vendor/usesend/"

# Refresh both vendored doc sets.
docs-sync-all: docs-sync usesend-docs-sync

# --- Development tasks -------------------------------------------------------

# Install/sync the dev environment.
install:
    uv sync

# Lint with Ruff.
lint:
    uv run ruff check .

# Auto-format with Ruff.
format:
    uv run ruff format .

# Verify formatting without writing.
format-check:
    uv run ruff format --check .

# Strict type-check gate.
typecheck:
    uv run basedpyright

# Architecture contracts.
imports:
    uv run lint-imports

# Dependency hygiene (depend on what you import).
deps:
    uv run deptry src

# Audit the locked dependencies for known vulnerabilities (OSV/PyPI advisory DB).
# Network-dependent, so it is a CI gate of its own and is NOT part of `check`.
# Triaged false positives are suppressed via IDs in `.pip-audit-ignore`.
# CI runs this same logic inline (see .github/workflows/ci.yml); keep them in sync.
audit:
    #!/usr/bin/env bash
    set -euo pipefail
    uv export --frozen --no-emit-project --no-hashes --all-groups \
        --format requirements-txt > requirements.audit.txt
    ignore=""
    while read -r id; do
        case "$id" in ''|\#*) continue ;; esac
        ignore="$ignore --ignore-vuln=$id"
    done < .pip-audit-ignore
    # --no-deps --disable-pip: audit the fully-pinned export as-is (uv already
    # locked every transitive dep), so pip-audit neither resolves nor builds a venv.
    uvx pip-audit --strict --no-deps --disable-pip --requirement requirements.audit.txt $ignore

# Run the test suite with branch coverage.
test:
    uv run pytest --cov --cov-branch --cov-report=term-missing

# Coverage XML for diff-cover.
cov:
    uv run pytest --cov --cov-branch --cov-report=xml --cov-report=term-missing

# Enforce 100% coverage on changed lines vs a base ref (default: local main).
cov-diff base="main": cov
    uv run diff-cover coverage.xml --compare-branch={{base}} --fail-under=100

# Full local gate — the offline code gate. Mirrors CI except the network-bound
# pip-audit step (run `just audit` separately). cov-diff depends on cov (runs tests).
check: lint format-check typecheck imports deps cov-diff

# Update the capability-surface snapshot (tests/__snapshots__/). That snapshot is the
# reviewed MCP API contract, so regenerating it is a deliberate act: update, then review
# the diff before committing.
snapshot-update:
    uv run pytest --snapshot-update

# Run the server over HTTP.
run:
    uv run python -m usesend_mcp

# Run with auto-reload for development.
dev:
    uv run fastmcp run fastmcp.json --transport http --reload --skip-env

# Run all pre-commit hooks.
precommit:
    uv run pre-commit run --all-files

# Refresh the lockfile.
lock:
    uv lock
