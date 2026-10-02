# 🧩 Zoho Skills CLI

**Turn a prospect conversation into a truthful, build-ready, demo-ready Zoho CRM engagement — with your coding agent.**

[![GitHub Release](https://img.shields.io/github/v/release/hichemca2021-lang/zoho-skills-cli?label=release)](https://github.com/hichemca2021-lang/zoho-skills-cli/releases)
[![GitHub stars](https://img.shields.io/github/stars/hichemca2021-lang/zoho-skills-cli?style=flat)](https://github.com/hichemca2021-lang/zoho-skills-cli/stargazers)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)

Installable toolkit of Zoho CRM pre-sales skills for Claude Code (and other skill-compatible
coding agents), in the spirit of [GitHub Spec Kit](https://github.com/github/spec-kit). Ships
five skills covering the full arc of a prospect engagement — discovery, design, implementation
planning, and demo packaging — so you can start at whichever stage matches where you already
are.

---

## Choose your process

| What you need | Process | Outcome |
|---|---|---|
| Turn a CRM-naive prospect conversation into structured requirements | **Discovery Interview** (`/crm-discovery-interviewer`) | A structured customer brief |
| Start designing without yet having organized discovery material | **Design Prospect, guided intake** (`/design-prospect`) | Discovery material organized and handed to CRM Design |
| Design a Zoho CRM solution for a specific prospect, from scratch | **CRM Design** (`/crm-data-model-customizer`) | A traceable, validated design package (data model, pipelines, blueprints, automation, persona dashboards) |
| Turn a validated design into an executable build sequence | **Implementation Planning** (`/customization-implementation-planner`) | A credential-free Markdown plan a coding agent can run against the Zoho CRM API |
| Prepare and deliver a prospect-specific live demo | **Demo Packaging** (`/demo-package`) | A demo plan + spoken transcript, scene-by-scene traced to real org capability |

These are independent entry points, not five mandatory phases — each produces an artifact the
next one can consume, but any one of them is also useful on its own.

---

## Install

No local install required — run directly with [uv](https://docs.astral.sh/uv/):

```bash
# Create a new project directory and install the skills into it
uvx --from git+https://github.com/hichemca2021-lang/zoho-skills-cli.git zoho-skills init my-project

# Or install into the current directory
uvx --from git+https://github.com/hichemca2021-lang/zoho-skills-cli.git zoho-skills init --here
```

This copies all five skills into `.claude/skills/` in the target project. Start Claude Code (or
another skill-compatible coding agent) in that directory and the skills are immediately
available.

---

## Get started

Launch your coding agent in the project directory and invoke a skill by name or trigger phrase
in chat. Review each stage's output before moving to the next — these are agent skills, not
terminal commands.

```text
/crm-discovery-interviewer    Start a discovery interview for Acme Logistics
/design-prospect              I have a call transcript for Acme Logistics
/crm-data-model-customizer    Design the CRM for Acme Logistics
/customization-implementation-planner   Generate the implementation plan for acme-logistics
/demo-package                 Build the demo plan for Acme Logistics
```

### Suggested workflow

1. `/crm-discovery-interviewer` (or `/design-prospect` if you already have discovery material)
   — produce a structured customer brief for a specific prospect.
2. `/crm-data-model-customizer` — turn that brief into a traceable, validated Zoho CRM design
   package.
3. `/customization-implementation-planner` — turn the validated design package into a
   credential-free, dependency-ordered Markdown plan for building it via the Zoho CRM API.
4. `/demo-package` (with a connected Zoho CRM MCP server, after the plan above has been
   executed against a real demo org) — generate the demo plan and spoken transcript.

---

## What each skill does

- **Discovery Interview** (`/crm-discovery-interviewer`) — interviews a CRM-naive prospect one
  plain-business-language question at a time, across resumable async sessions, and produces a
  structured customer brief.
- **Design Prospect, guided intake** (`/design-prospect`) — the front door for an engineer who
  wants to start a CRM design engagement but hasn't yet gathered or organized discovery
  material; walks them through what to provide, then hands off to CRM Design.
- **CRM Data Model Customizer** (`/crm-data-model-customizer`) — turns prospect discovery
  material into a traceable, validated Zoho CRM design package (data model, pipelines,
  blueprints, automation, persona dashboards), with every element citing the requirement that
  justifies it.
- **Implementation Plan Generator** (`/customization-implementation-planner`) — turns a
  validated design package into a single, credential-free, dependency-ordered Markdown plan a
  *separate* coding-agent session can follow to build it via the Zoho CRM API: discovery-first,
  with explicit per-step write confirmation, never a batch approval.
- **Demo Pulse** (`/demo-package`) — turns a customer brief, pain case, and a connected Zoho
  CRM demo org into a truthful, screen-by-screen demo plan and spoken transcript, where every
  scene maps a real customer pain to a real org capability to a real screen to a business
  outcome.

---

## Development

```bash
uv sync
uv run zoho-skills init --here
uv run zoho-skills check   # list the skills this toolkit installs
```
