# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 2.x | ✅ Active |
| 1.x | ⚠️ Critical fixes only |

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Instead, report them privately by emailing the maintainer or opening a [GitHub Security Advisory](https://github.com/owrew/antigravity-obsidian-exporter/security/advisories/new).

Include:

1. A description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Any suggested fixes (optional)

You will receive a response within 72 hours. If confirmed, a patch will be released within 14 days.

## Security Notes

This tool:

- Reads **local files only** — no network access is made during export
- Does **not** send conversation data anywhere
- Does **not** require API keys or credentials
- Stores state in `.agy_export_state.json` — a local hash index, no content

If you discover a way for the tool to inadvertently expose private conversation data (e.g., via malformed transcripts or path traversal), please report it.
