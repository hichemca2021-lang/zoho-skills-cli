<!--
  Template for the generated Implementation Plan file.
  Source of truth for structure: specs/006-customization-implementation-plan/contracts/implementation-plan.schema.md
  Fill every [BRACKETED] placeholder; remove this comment block from the final output.
  The "## Manual Steps Summary" section is CONDITIONAL — include it only if at least one
  build step has build_method: manual. Omit it entirely (not just emptied) otherwise.
-->
# Implementation Plan: [PROSPECT NAME]

**Generated from**: `output/[prospect-slug]/12-handoff-spec.yaml` (source_register_version: [N])
**Generated at**: [ISO-8601 timestamp]

## Prerequisites

### Required API Scopes

- [ScopeA]
- [ScopeB]
<!-- One line per distinct scope referenced by any step below. Union, no duplicates. -->

**This file contains no credentials.** Before proceeding, request a live API token with the
scopes above from the engineer running this plan. Do not attempt any call — read or write —
until a token is confirmed available.

<!-- CONDITIONAL SECTION — include only if >=1 step below has build_method: manual -->
## Manual Steps Summary

The following design elements have no direct API equivalent in the available tool surface and
must be built by hand in the Zoho CRM UI. They are still listed as numbered steps below for
full traceability, but flagged here so you can plan your own involvement before execution
starts.

- Step [N]: [design_element_ref] — [one-line reason no API path exists]
<!-- end conditional section -->

## Phase 1: Discovery (read-only)

Perform every call below before any step in Phase 3+. None of these require write access.

1. [Read call description] — discovers: [element types this reveals]
2. ...

## Phase 2: Reconciliation

For each element the design package assumes, compare the Phase 1 discovery finding against
that assumption:

- If the element does not exist in the org and the design package assumed it would be created
  here: proceed to the corresponding Phase 3+ step normally.
- If the element already exists in the org with a **different** configuration than the design
  package assumes: **STOP** — report the exact mismatch (element, expected vs. actual) to the
  engineer and wait for instruction before touching that element.
- If the element already exists in the org with the **same** configuration the design package
  assumes: skip the corresponding Phase 3+ step (already satisfied) and note it as such in your
  final summary.

Do not proceed to any Phase 3+ step for an element whose reconciliation is unresolved.

## Phase 3+: Build Steps

<!-- Grouped, in this fixed order: Modules -> Fields -> Relationships -> Pipelines ->
     Blueprints -> Automation Rules -> Dashboards. Each step follows this shape: -->

### Modules

#### Step [N]: [design_element_ref]

- **Build method**: `api` | `manual`
- **Operation**: [tool/endpoint name and parameters, or UI action for manual]
- **Required scope**: [scope, or "none (manual step)"]
- **Depends on**: [step numbers, or "none"]
- **Design package reference**: [element ID(s) from the handoff spec]

> STOP — ask the engineer for explicit confirmation before executing this step.
<!-- Confirmation line appears on every step whose build_method is api AND which mutates org
     state. Omit it only for read-only or purely-informational steps (there should be none in
     this section — Phase 3+ is write-only by definition). -->

### Fields

...

### Relationships

...

### Pipelines

...

### Blueprints

...

### Automation Rules

...

### Dashboards

...

## Traceability

| Design Element ID | Step Number(s) | Covered? |
|---|---|---|
| [element id] | [N] | yes |
| [element id] | [N] | manual |
<!-- Every element from the handoff spec appears exactly once (or more, if one element needs
     multiple steps). No blank or "no" values are permitted here — contract invariant C-04. -->
