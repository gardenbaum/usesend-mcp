# usesend-mcp

[![CI](https://github.com/gardenbaum/usesend-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/gardenbaum/usesend-mcp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/usesend-mcp?logo=pypi&logoColor=white)](https://pypi.org/project/usesend-mcp/)
[![Docker Hub](https://img.shields.io/badge/docker%20hub-gardenbaum%2Fusesend--mcp-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/gardenbaum/usesend-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)

An [MCP](https://modelcontextprotocol.io) server for the [useSend](https://usesend.com) email platform (an open-source Resend/Postmark alternative). It gives any MCP client — Claude, Cursor, VS Code, Windsurf, Codex — **33 tools** for transactional email, contacts, campaigns, domains, and analytics, over stdio.

## Setup

**1. Get a useSend API key** (`us_…`) from **Settings → API Keys** at [app.usesend.com](https://app.usesend.com) (or your self-hosted instance).

**2. Add the server to your MCP client.** Almost every client uses the same JSON — paste this in and swap in your key:

```json
{
  "mcpServers": {
    "usesend": {
      "command": "uvx",
      "args": ["usesend-mcp"],
      "env": { "USESEND_API_KEY": "us_your_api_key_here" }
    }
  }
}
```

`uvx` (from [uv](https://docs.astral.sh/uv/)) downloads and runs the server from PyPI on demand — nothing to install first.

**Where does that JSON go?**

| Client | Config file |
|---|---|
| Claude Code | `.mcp.json` (project root) |
| Claude Desktop | `claude_desktop_config.json` |
| Cursor | `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` |
| VS Code (Cline) | `cline_mcp_settings.json` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` |

Prefer the command line?

```bash
claude mcp add usesend --env USESEND_API_KEY=us_your_api_key_here -- uvx usesend-mcp   # Claude Code
codex  mcp add usesend --env USESEND_API_KEY=us_your_api_key_here -- uvx usesend-mcp   # Codex CLI
```

Done — ask your assistant *"list my useSend contact books"* or *"send a welcome email to jane@example.com"* to check it works.

<details>
<summary><b>Run with Docker instead of uvx</b></summary>

Use the published image in any JSON config above:

```json
{
  "mcpServers": {
    "usesend": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "USESEND_API_KEY", "gardenbaum/usesend-mcp"],
      "env": { "USESEND_API_KEY": "us_your_api_key_here" }
    }
  }
}
```

Or run it directly (`-i` keeps stdin open for the stdio protocol, `--rm` cleans up on exit):

```bash
docker run -i --rm -e USESEND_API_KEY=us_your_api_key_here gardenbaum/usesend-mcp
```

Images: [`gardenbaum/usesend-mcp`](https://hub.docker.com/r/gardenbaum/usesend-mcp) on Docker Hub, mirrored to `ghcr.io/gardenbaum/usesend-mcp` — `linux/amd64` + `linux/arm64`.
</details>

## Configuration

Environment variables (prefix `USESEND_`, also read from a `.env` file):

| Variable | Default | Description |
|---|---|---|
| `USESEND_API_KEY` | _(required)_ | API key, format `us_…`. |
| `USESEND_BASE_URL` | `https://app.usesend.com` | API base URL; change for a self-hosted instance. |
| `USESEND_DEFAULT_FROM` | _(unset)_ | Default sender for `send_email` / `batch_send_emails`. |
| `USESEND_LOG_LEVEL` | `INFO` | Log verbosity (`DEBUG` … `CRITICAL`). |
| `USESEND_TIMEOUT` | `30` | HTTP request timeout, in seconds. |

## Tools

**33 tools across 6 domains.** Every tool also accepts an optional `response_format` (`"markdown"` default, or `"json"` for machine-readable output).

<details>
<summary><b>Full tool list</b></summary>

### Emails (6)

| Tool | Description |
|---|---|
| `usesend_send_email` | Send a single transactional email (falls back to `USESEND_DEFAULT_FROM` if `from_address` is omitted). |
| `usesend_batch_send_emails` | Send up to 100 emails in a single request. |
| `usesend_list_emails` | List emails with pagination; optional `start_date`/`end_date` (ISO-8601) and `domain_id` filters. |
| `usesend_get_email` | Get details for a specific email. |
| `usesend_cancel_email` | Cancel a scheduled email. |
| `usesend_update_email_schedule` | Reschedule a scheduled email. |

### Contact Books (5)

| Tool | Description |
|---|---|
| `usesend_list_contact_books` | List all contact books accessible by the API key. |
| `usesend_get_contact_book` | Get details for a specific contact book. |
| `usesend_create_contact_book` | Create a contact book, optionally with double opt-in. |
| `usesend_update_contact_book` | Update a contact book's name or double opt-in setting. |
| `usesend_delete_contact_book` | Delete a contact book. |

### Contacts (8)

| Tool | Description |
|---|---|
| `usesend_list_contacts` | List contacts in a contact book, with pagination. |
| `usesend_get_contact` | Get details for a specific contact. |
| `usesend_create_contact` | Create a contact in a contact book. |
| `usesend_update_contact` | Update a contact's mutable fields. |
| `usesend_upsert_contact` | Create or update a contact by email address. |
| `usesend_delete_contact` | Delete a contact from a contact book. |
| `usesend_bulk_create_contacts` | Create multiple contacts in a single request. |
| `usesend_bulk_delete_contacts` | Delete multiple contacts in a single request. |

### Campaigns (7)

| Tool | Description |
|---|---|
| `usesend_create_campaign` | Create an email campaign. |
| `usesend_get_campaign` | Get details for a specific campaign. |
| `usesend_list_campaigns` | List campaigns; optional `status` and `search` filters. |
| `usesend_delete_campaign` | Delete a campaign. |
| `usesend_pause_campaign` | Pause a running campaign. |
| `usesend_resume_campaign` | Resume a paused campaign. |
| `usesend_schedule_campaign` | Schedule a campaign for a future time. |

### Domains (5)

| Tool | Description |
|---|---|
| `usesend_list_domains` | List all domains. |
| `usesend_get_domain` | Get details for a specific domain. |
| `usesend_create_domain` | Create a domain (`name` and `region` required). |
| `usesend_verify_domain` | Trigger DNS verification for a domain. |
| `usesend_delete_domain` | Delete a domain. |

### Analytics (2)

| Tool | Description |
|---|---|
| `usesend_email_time_series` | Email volume time series (`days`: `"7"` or `"30"`); optional `domain_id`. |
| `usesend_reputation_metrics` | Sending reputation metrics (bounce/complaint rates); optional `domain_id`. |

</details>

## Development

```bash
uv sync --dev      # install runtime + dev dependencies
just check         # lint, format, types, import contracts, tests @ 100% diff coverage
```

Work happens on `dev`; `main` is the release branch (push a `v*` tag to publish). Architectural
decisions are recorded as ADRs in [`docs/adr/`](docs/adr/). Logs go to `stderr` — `stdout` is
reserved for the MCP protocol.

## Contributing · Security · License

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).
Report vulnerabilities privately via [SECURITY.md](SECURITY.md), not public issues.
Licensed under [MIT](LICENSE) © gardenbaum.
