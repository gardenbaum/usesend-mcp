# Security Policy

## Reporting a vulnerability

**Please do not report security vulnerabilities through public GitHub issues,
discussions, or pull requests.**

Instead, report them privately through GitHub's built-in
[**Report a vulnerability**](https://github.com/gardenbaum/usesend-mcp/security/advisories/new)
form (Security → Advisories → *Report a vulnerability*). This routes your report
confidentially to the maintainer.

Please include as much of the following as you can:

- The type of issue and the component affected.
- Steps to reproduce, or a proof-of-concept.
- The impact, including how an attacker might exploit it.
- The version / commit you tested against.

You can expect an initial acknowledgement within **7 days**. We will keep you
informed of progress toward a fix and public disclosure, and will credit you in
the advisory unless you prefer to remain anonymous.

## Supported versions

usesend-mcp is pre-1.0 and released from `main`. Security fixes are applied to
the latest released version. Please always run the most recent release.

| Version | Supported |
|---|---|
| latest release | ✅ |
| older releases  | ❌ |

## Scope and handling of secrets

- **API keys never touch the repository.** The useSend API key is read only from
  the `USESEND_API_KEY` environment variable (or a local `.env` that is
  git-ignored). Never commit real keys, and never paste a key into an issue,
  discussion, or log excerpt.
- The server speaks **stdio only** — it opens no network listener and exposes no
  port. `stdout` carries the MCP protocol; logs go to `stderr` and are scrubbed
  of the API key.
- Outbound requests go only to the configured `USESEND_BASE_URL`
  (default `https://app.usesend.com`).

## Supply chain

- Dependencies are pinned via `uv.lock` and audited in CI with `pip-audit`
  (`just audit`).
- Dependency and GitHub Actions updates are proposed automatically via
  Dependabot.
- Releases are published to PyPI using [Trusted Publishing (OIDC)][tp] — no
  long-lived API tokens are stored in the repository.

[tp]: https://docs.pypi.org/trusted-publishers/
