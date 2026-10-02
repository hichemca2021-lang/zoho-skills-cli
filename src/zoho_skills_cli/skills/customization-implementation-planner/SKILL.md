---
name: customization-implementation-planner
description: Given a validated Zoho CRM design package (the handoff YAML produced by crm-data-model-customizer), think step by step through the build order and produce a single, credential-free Markdown implementation plan that a later Claude Code session can execute via the Zoho CRM API, discovery-first and with explicit per-step write confirmation. Use when a pre-sales engineer has a validated design package for a prospect and wants a plan to actually build it in a real demo org.
---

# Customization Implementation Plan Generator

> **Process**: Implementation Planning — turn a validated design package into an executable,
> credential-free build sequence.
> **Outcome**: `output/<prospect-slug>/14-implementation-plan.md`, ready to hand to a separate
> Claude Code session with a live API token, for Demo Packaging (`demo-package`) afterward.

## What this skill does, and does not, do

This skill reads one input file and writes one output file. It never calls any Zoho CRM API
itself and never touches a live org (spec Assumptions). It is the bridge between a design
package (what to build) and a build (how a *separate* Claude Code session, run later, with its
own token, actually builds it).

- **Input**: `output/<prospect-slug>/12-handoff-spec.yaml`, produced by the upstream
  `crm-data-model-customizer` skill, matching
  `specs/004-crm-data-model-customizer/contracts/handoff-spec.schema.md`.
- **Output**: `output/<prospect-slug>/14-implementation-plan.md`, matching
  `specs/006-customization-implementation-plan/contracts/implementation-plan.schema.md` and
  built from `templates/implementation-plan.md`.

If asked to call a CRM API, create/modify/delete anything in a real org, or skip straight to
"just build it," decline and explain this skill only produces the plan file — a separate
Claude Code execution session, given this plan and a live token, does the building.

---

## Step 0 — Input validation gate (spec FR-001, FR-002)

Before anything else:

1. Read `output/<prospect-slug>/12-handoff-spec.yaml`.
2. Confirm `validation.blocking_failure_count == 0`. If it is missing, non-zero, or the
   `validation` block is absent entirely: **refuse**. Report exactly which check is
   failing/missing and stop — do not generate a partial plan.
3. Confirm every one of these top-level arrays is present (each may be empty, but the key must
   exist): `modules`, `pipelines`, `blueprints`, `automation_rules`, `personas`. If any is
   missing: **refuse** and name the missing array(s).
4. Only once both checks pass, proceed to Step 1.

This mirrors the upstream skill's own gating discipline — never guess past a missing
precondition.

---

## Step 1 — Decompose into Build Steps (spec FR-003, FR-011, FR-012)

Walk the handoff spec and emit exactly one Build Step per design element, using this ID scheme
for `design_element_ref` (stable, derived directly from the handoff YAML, never invented):

| Element | `design_element_ref` format |
|---|---|
| Module | `module:<api_name>` |
| Field | `module:<module_api_name>.field:<field_api_name>` |
| Relationship | `module:<module_api_name>.relationship:<target_module>` |
| Pipeline stage | `pipeline:<pipeline_name>.stage:<stage_name>` |
| Blueprint transition | `blueprint:<module>.transition:<from>-><to>` |
| Automation rule | `automation:<rule_id>` |
| Persona dashboard | `persona:<persona_name>` |

Every Build Step has: `step_number`, `design_element_ref`, `build_method`, `operation`,
`required_scope`, `depends_on[]`, and (for mutating `api` steps) a `confirmation_instruction`
— per `specs/006-customization-implementation-plan/data-model.md`'s Build Step entity.

**No element may be skipped and no step may reference an element absent from the handoff
spec** — this is checked explicitly in Step 5 (Traceability).

---

## Step 2 — Determine build method per element (spec FR-013; research.md §5)

Map each element type to a `build_method` based on the actual Zoho CRM tool surface available
in this environment (the Zoho CRM MCP tools). Do not assume an API exists where none is listed
here — an incorrect `api` tag is worse than an honest `manual` tag, because it sends the
executor toward a call that doesn't exist.

| Element type | `build_method` | Why |
|---|---|---|
| Module (new custom module) | `manual` | No module-creation tool is exposed in this environment's Zoho CRM tool surface; custom module creation is a Setup-console action in Zoho CRM, not a standard API call. |
| Field (on an existing module) | `api` | `createFields` creates custom fields on a module. |
| Relationship (lookup field) | `api` | A lookup relationship is created as a field via `createFields` with a lookup field type. |
| Pipeline / stage | `manual` | No stage-definition tool is exposed; pipeline stages are configured via Setup, not the available API surface. |
| Blueprint / transition | `manual` | No Blueprint read/write tool is exposed in this environment's tool surface. |
| Automation rule | `manual` | No workflow/automation-rule read/write tool is exposed in this environment's tool surface. |
| Persona dashboard | `manual` | No dashboard/home-page tool is exposed in this environment's tool surface. |

If a future environment exposes additional tools (e.g., a Blueprint API), update this table —
do not silently start tagging those elements `api` without a corresponding row here naming the
tool.

Every `manual` step still gets a full Build Step entry (Step 1) for traceability (spec
FR-012); it is additionally listed in the `Manual Steps Summary` (Step 6).

---

## Step 3 — Order steps by dependency (spec FR-004; contract invariant C-06)

Sequence steps so that:
1. All `module` steps come before any `field`/`relationship` step on that module.
2. All `field`/`relationship` steps come before any `pipeline`, `blueprint`, `automation`, or
   `persona` step that references that field by API name.
3. Within the fixed section order required by the template: Modules → Fields → Relationships →
   Pipelines → Blueprints → Automation Rules → Dashboards.

A step's `depends_on` list may only contain step numbers strictly less than its own
`step_number`. If a true circular dependency exists in the handoff spec itself (should be
impossible — the upstream skill's own validation forbids orphan/dangling references), refuse
and report it rather than emitting an invalid plan.

---

## Step 4 — Discovery and Reconciliation (spec FR-006, FR-007; research.md §3; contract C-02)

Generate `Phase 1: Discovery` and `Phase 2: Reconciliation` using only read-level Zoho CRM MCP
tools, before any Phase 3+ step, structurally fixed by the template:

| What to discover | Tool(s) |
|---|---|
| Existing modules | `getModules` |
| Existing fields per module | `getFields` |
| Existing layouts | `getLayouts`, `getLayoutById` |
| Existing related lists / relationships | `getRelatedLists` |

There is no read tool in this environment's surface for pipelines-as-stage-metadata,
blueprints, or automation rules directly; for those, instruct the executor to use `getFields`
on the relevant module to inspect the stage/status picklist values actually configured (this is
how pipeline stages and blueprint states surface in the CRM data model), and note in the
Reconciliation instructions that full blueprint/automation-rule state can only be confirmed
manually in the Zoho CRM Setup UI — call this out explicitly rather than silently treating it
as discovered.

For every discovered element, instruct the executor (per the template's Phase 2 text) to
compare it against the design package's assumption and STOP on any mismatch before touching
that element in Phase 3+.

---

## Step 5 — Traceability (spec FR-011, FR-012; contract C-04, C-05)

Build the `Traceability` table with exactly one row per element ID from the handoff spec
(`modules[].api_name` and nested `fields[]`/`relationships[]`, `pipelines[].stages[]`,
`blueprints[].transitions[]`, `automation_rules[].rule_id`, `personas[].persona`), each row's
`Step Number(s)` pointing to the Build Step(s) from Step 1, and `Covered?` set to `yes` for
`api`-method steps or `manual` for `manual`-method steps. Never leave a row blank or `no`.

Cross-check in both directions before finalizing: every handoff-spec element has a row, and
every Build Step's `design_element_ref` resolves to a real row.

---

## Step 6 — Manual Steps Summary (spec FR-013; research.md §5)

If, and only if, at least one Build Step has `build_method: manual`, include the `Manual Steps
Summary` section (per the template's conditional block) listing each such step's number,
`design_element_ref`, and a one-line reason (reuse the "Why" column from Step 2's table).
Omit the section entirely if every step is `api`.

---

## Step 7 — Prerequisites and credential safety (spec FR-008, FR-009, FR-010, FR-010a)

Fill `Prerequisites`:
1. List the union of every `api`-method step's `required_scope`, deduplicated.
2. Include the literal sentence from the template: "This file contains no credentials. Before
   proceeding, request a live API token with the scopes above from the engineer running this
   plan."
3. Never write a token, secret, or any credential-shaped value anywhere in the generated file.
   Before finalizing output, scan your own draft for anything that looks like a credential
   (long hex/base64 strings, `token:`/`secret:` followed by a value) and remove it — this
   should never occur since no credential is ever an input to this skill, but it is checked as
   a hard gate anyway (contract invariant C-01).

For every `api`-method mutating Build Step, state its `required_scope` directly on the step
(Step 1), not only in the aggregate Prerequisites list.

---

## Step 8 — Per-step write confirmation (spec FR-010a; constitution Principle IV; contract C-03)

Every Build Step whose `build_method` is `api` and whose operation mutates org state (i.e.,
every `api` step in Phase 3+ — read-only discovery in Phase 1 is exempt) MUST end with the
literal line:

> STOP — ask the engineer for explicit confirmation before executing this step.

This appears **individually on every such step** — never as one blanket "approve this whole
plan" statement at the top of Phase 3+. A plan that gates all writes behind a single up-front
approval is non-compliant and must be corrected before being presented as finished (this repo's
constitution, Principle IV: Read-Only Safety — no batch or implicit write approval).

If, at execution time, the engineer's supplied token lacks a scope a step requires, instruct
the executor (via this same per-step text, reused at execution time) to stop and report the
missing scope rather than attempt a workaround or a different, unscoped call (spec FR-010,
Acceptance Scenario 3).

---

## Step 9 — Write the plan file

Render all of the above into `templates/implementation-plan.md`'s structure and save as
`output/<prospect-slug>/14-implementation-plan.md`. This MUST be the only file this skill
writes.

---

## Re-run behavior (spec FR-014; research.md §7)

Each invocation regenerates the plan fresh from the current `12-handoff-spec.yaml` and
overwrites any existing `14-implementation-plan.md` at the same path. There is no diff/merge
against a prior plan version — the handoff YAML, not the plan file, is the durable source of
truth. If the engineer has made manual notes directly in a previous plan file, warn them before
overwriting that re-running will discard those notes.

---

## Final summary

At the end of any run, report: total Build Step count, count by `build_method` (api vs.
manual), the required-scope list, and whether a Manual Steps Summary was included.

---

## Functional Requirements traceability (spec.md FR-001–FR-014, FR-010a)

| Requirement | Where addressed above |
|---|---|
| FR-001 | Step 0 |
| FR-002 | Step 0 |
| FR-003 | Step 1 |
| FR-004 | Step 3 |
| FR-005 (single Markdown file) | Step 9 — one output path, one file |
| FR-006 | Step 4 |
| FR-007 | Step 4 |
| FR-008 | Step 7 |
| FR-009 | Step 7 |
| FR-010 | Step 7, Step 8 |
| FR-010a | Step 8 |
| FR-011 | Step 1, Step 5 |
| FR-012 | Step 1, Step 5 |
| FR-013 | Step 2, Step 6 |
| FR-014 | Re-run behavior |

No gaps identified between this skill's instructions and spec.md's Functional Requirements.
