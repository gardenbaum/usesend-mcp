# usesend-mcp

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![uv](https://img.shields.io/badge/package%20manager-uv-de5fe9)](https://docs.astral.sh/uv/)

A [Model Context Protocol](https://modelcontextprotocol.io) server exposing the [useSend](https://usesend.com) email platform to MCP clients over stdio.

## Overview

[useSend](https://usesend.com) is an open-source email sending platform (a self-hosted alternative to Resend/Postmark) covering transactional email, contact/audience management, and marketing campaigns.

**usesend-mcp** is a [FastMCP](https://gofastmcp.com) server that wraps the useSend REST API as 33 MCP tools across six domains: emails, contact books, contacts, campaigns, domains, and analytics. It speaks **stdio only** — no HTTP server, no ports to expose — so it runs as a subprocess launched directly by your MCP client.

## Quick Start

### uvx (recommended)

```bash
USESEND_API_KEY=us_your_api_key_here uvx usesend-mcp
```

`uvx` downloads and runs the [`usesend-mcp`](https://pypi.org/project/usesend-mcp/) package from PyPI on the fly — no local install required.

### Docker

```bash
docker run -i --rm -e USESEND_API_KEY=us_your_api_key_here ghcr.io/gardenbaum/usesend-mcp
```

The `-i` flag is required: MCP over stdio needs an interactive stdin/stdout stream, and `--rm` cleans up the container on exit.

## API key

All tools authenticate with a useSend API key (format `us_...`). Create one from your useSend dashboard at [app.usesend.com](https://app.usesend.com) (or your self-hosted instance) under **Settings → API Keys**, then set it as `USESEND_API_KEY`.

## IDE / client integration

Every client below launches the server the same way — `uvx usesend-mcp` with `USESEND_API_KEY` in the environment — only the config file and location differ. Replace `us_your_api_key_here` with your real key.

### Claude Code / Claude Desktop

Add to `.mcp.json` (project) or `claude_desktop_config.json` (Desktop app):

```json
{
  "mcpServers": {
    "usesend": {
      "command": "uvx",
      "args": ["usesend-mcp"],
      "env": {
        "USESEND_API_KEY": "us_your_api_key_here"
      }
    }
  }
}
```

Or via the Claude Code CLI:

```bash
claude mcp add usesend --env USESEND_API_KEY=us_your_api_key_here -- uvx usesend-mcp
```

### Cursor

Add to `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):

```json
{
  "mcpServers": {
    "usesend": {
      "command": "uvx",
      "args": ["usesend-mcp"],
      "env": {
        "USESEND_API_KEY": "us_your_api_key_here"
      }
    }
  }
}
```

### VS Code (Cline)

Add to Cline's `cline_mcp_settings.json` (via **Cline → MCP Servers → Configure MCP Servers**):

```json
{
  "mcpServers": {
    "usesend": {
      "command": "uvx",
      "args": ["usesend-mcp"],
      "env": {
        "USESEND_API_KEY": "us_your_api_key_here"
      }
    }
  }
}
```

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "usesend": {
      "command": "uvx",
      "args": ["usesend-mcp"],
      "env": {
        "USESEND_API_KEY": "us_your_api_key_here"
      }
    }
  }
}
```

### Codex CLI

Codex CLI reads MCP server config from `~/.codex/config.toml` (TOML, not JSON):

```toml
[mcp_servers.usesend]
command = "uvx"
args = ["usesend-mcp"]
env = { USESEND_API_KEY = "us_your_api_key_here" }
```

Or via the CLI:

```bash
codex mcp add usesend --env USESEND_API_KEY=us_your_api_key_here -- uvx usesend-mcp
```

### MCP Inspector

```bash
USESEND_API_KEY=us_your_api_key_here npx @modelcontextprotocol/inspector uvx usesend-mcp
```

Inspector also accepts the same `mcpServers` JSON shape used above via `--config <file> --server usesend`.

### Docker variant

Any of the JSON-based clients above can run the server from the container image instead of `uvx`:

```json
{
  "mcpServers": {
    "usesend": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "USESEND_API_KEY", "ghcr.io/gardenbaum/usesend-mcp"],
      "env": {
        "USESEND_API_KEY": "us_your_api_key_here"
      }
    }
  }
}
```

`-e USESEND_API_KEY` (no `=value`) tells Docker to forward the variable from its own environment — which the MCP client populates from the `env` block above — into the container.

## Available tools

Every tool below also accepts an optional `response_format` parameter (`"markdown"` default, or `"json"` for machine-readable output).

### Emails (6)

| Tool | Description |
|---|---|
| `usesend_send_email` | Send a single transactional email (falls back to `USESEND_DEFAULT_FROM` if `from_address` is omitted). |
| `usesend_batch_send_emails` | Send up to 100 emails in a single request. |
| `usesend_list_emails` | List emails with pagination (`page`, `limit`); optional `start_date`/`end_date` (ISO-8601) and `domain_id` filters. |
| `usesend_get_email` | Get details for a specific email. |
| `usesend_cancel_email` | Cancel a scheduled email. |
| `usesend_update_email_schedule` | Reschedule a scheduled email. |

### Contact Books (5)

| Tool | Description |
|---|---|
| `usesend_list_contact_books` | List all contact books accessible by the API key (unpaginated). |
| `usesend_get_contact_book` | Get details for a specific contact book. |
| `usesend_create_contact_book` | Create a new contact book, optionally with double opt-in. |
| `usesend_update_contact_book` | Update a contact book's name or double opt-in setting. |
| `usesend_delete_contact_book` | Delete a contact book. |

### Contacts (8)

| Tool | Description |
|---|---|
| `usesend_list_contacts` | List contacts in a contact book with pagination (`page`, `limit`). |
| `usesend_get_contact` | Get details for a specific contact. |
| `usesend_create_contact` | Create a new contact in a contact book. |
| `usesend_update_contact` | Update a contact's mutable fields. |
| `usesend_upsert_contact` | Create or update a contact by email address. |
| `usesend_delete_contact` | Delete a contact from a contact book. |
| `usesend_bulk_create_contacts` | Create multiple contacts in a single request. |
| `usesend_bulk_delete_contacts` | Delete multiple contacts in a single request. |

### Campaigns (7)

| Tool | Description |
|---|---|
| `usesend_create_campaign` | Create a new email campaign (`name`, `from_address`, `subject`, `contact_book_id`, optional `html`). |
| `usesend_get_campaign` | Get details for a specific campaign. |
| `usesend_list_campaigns` | List campaigns (`page`; optional `status` — `DRAFT`/`SCHEDULED`/`RUNNING`/`PAUSED`/`SENT` — and `search` over name/subject; no `limit` override). |
| `usesend_delete_campaign` | Delete a campaign. |
| `usesend_pause_campaign` | Pause a running campaign. |
| `usesend_resume_campaign` | Resume a paused campaign. |
| `usesend_schedule_campaign` | Schedule a campaign to be sent at a future time. |

### Domains (5)

| Tool | Description |
|---|---|
| `usesend_list_domains` | List all domains. |
| `usesend_get_domain` | Get details for a specific domain. |
| `usesend_create_domain` | Create a new domain (`name` and `region` are both required). |
| `usesend_verify_domain` | Trigger DNS verification for a domain. |
| `usesend_delete_domain` | Delete a domain. |

### Analytics (2)

| Tool | Description |
|---|---|
| `usesend_email_time_series` | Get email volume time series analytics (`days`: `"7"` or `"30"`, default 30; optional `domain_id` filter). |
| `usesend_reputation_metrics` | Get sending reputation metrics (bounce/complaint rates); optional `domain_id` filter. |

## Configuration

All settings are environment variables with the `USESEND_` prefix (also loadable from a `.env` file).

| Variable | Default | Description |
|---|---|---|
| `USESEND_API_KEY` | _(required)_ | useSend API key, format `us_...`. |
| `USESEND_BASE_URL` | `https://app.usesend.com` | Base URL of the useSend API; override for a self-hosted instance. |
| `USESEND_DEFAULT_FROM` | _(unset)_ | Default sender address used by `usesend_send_email` / `usesend_batch_send_emails` when `from_address` is omitted. |
| `USESEND_LOG_LEVEL` | `INFO` | Log verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). |
| `USESEND_TIMEOUT` | `30` | HTTP request timeout to the useSend API, in seconds. |

## Example prompts

- "Send an email to jane@example.com with subject 'Welcome' and a short greeting."
- "List my contact books."
- "Show email stats for the last 7 days."
- "Create a contact book called 'Newsletter' with double opt-in enabled."
- "Pause campaign abc123 and reschedule it for next Monday at 9am."
- "What's our current sender reputation?"

## Development

```bash
uv sync --dev          # install runtime + dev dependencies
just check             # lint + format-check + typecheck + import contracts + tests w/ 100% diff coverage
just docs-sync-all     # refresh vendored FastMCP docs + useSend OpenAPI spec
```

The server communicates over stdio, so `stdout` is reserved exclusively for the MCP protocol — all logs (structured JSON) are written to `stderr`.

Architecturally significant decisions are recorded as lightweight ADRs in [`docs/adr/`](docs/adr/).

## License

[MIT](LICENSE)
