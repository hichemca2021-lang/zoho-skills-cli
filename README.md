# zoho-skills-cli

Installable toolkit of Zoho CRM pre-sales skills for Claude Code (and other
skill-compatible coding agents), in the spirit of [GitHub Spec Kit](https://github.com/github/spec-kit).

Ships two skills:

- **CRM Data Model Customizer** (`/crm-data-model-customizer`) — turns prospect
  discovery material into a traceable, validated Zoho CRM design package
  (data model, pipelines, blueprints, automation, persona dashboards).
- **Demo Pulse** (`/demo-package`) — turns a customer brief, pain case, and a
  connected Zoho CRM demo org into a truthful, screen-by-screen demo plan and
  spoken transcript.

## Install

No local install required — run directly with [uv](https://docs.astral.sh/uv/):

```bash
# Create a new project directory and install the skills into it
uvx --from git+https://github.com/hichemca2021-lang/zoho-skills-cli.git zoho-skills init my-project

# Or install into the current directory
uvx --from git+https://github.com/hichemca2021-lang/zoho-skills-cli.git zoho-skills init --here
```

This copies both skills into `.claude/skills/` in the target project. Start
Claude Code in that directory and the skills are immediately available via
`/crm-data-model-customizer` and `/demo-package`.

## Suggested workflow

1. `/crm-data-model-customizer` — produce a design package for a specific prospect.
2. `/demo-package` — hand that package (plus a connected Zoho CRM MCP server) to
   generate the demo plan and spoken transcript.

## Development

```bash
uv sync
uv run zoho-skills init --here
```
