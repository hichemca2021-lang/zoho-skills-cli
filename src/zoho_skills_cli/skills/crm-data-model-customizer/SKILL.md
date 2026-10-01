---
name: crm-data-model-customizer
description: Given discovery material about a prospect (calls, notes, emails, documents, website, web research), produce a traceable, validated Zoho CRM design package (data model, pipelines, blueprints, automation, persona dashboards) for a pre-sales engineer, ready to hand off to a downstream demo-building agent. Use when a Zoho CRM pre-sales engineer asks to design, customize, or model a CRM solution for a specific prospect before any demo org is built.
---

# CRM Data Model Customizer

## Read-only safety boundary (spec FR-018)

**This skill never writes to any live CRM organization.** Every phase below (0 through 9)
produces only Markdown/YAML documents under `output/<prospect-slug>/`. There is no "apply to
org" capability in this skill — that is explicitly out of scope for this version (see spec.md
Assumptions). If a user asks this skill to create/modify/delete anything in a real CRM org,
decline and explain that this skill only produces a design package.

## Overview

Pipeline: `Intake → Extraction → Synthesis/Gap-Interview → Data Model → Pipelines →
Blueprints → Automation → Personas → Validation → Handoff`.

Each phase writes one or more documents to `output/<prospect-slug>/`, using the templates in
`templates/`. Every later phase reads only the documents already written by earlier phases —
never invents facts the evidence doesn't support (spec FR-001–FR-003).

All documents share a header: prospect name, version, date, source-register version, status
(spec FR-023).

---

## Phase 0 — Intake & Source Register

**Input**: every file/transcript/email/document/website excerpt the engineer provides, plus
permission to crawl the prospect's public website and run public web research unless the
engineer restricts it (spec Assumptions).

**Steps**:
1. Inventory every input. For each, create a row in `00-source-register.md` (copy
   `templates/source-register.md`) with a stable `SRC-###` ID, `type`
   (call_transcript/email/document/website/web_research), `date`, `reliability` (H/M/L — your
   judgment of how authoritative this *kind* of source is, independent of recency), and
   `language`.
2. Confidentiality guard (spec FR-021): before issuing any web search/crawl call, strip the
   prospect's name, contact names, and any other identifying detail from the outbound query.
   Scope queries to public company/industry facts only (research.md §5).
3. Check the **blocking-inputs gate**: industry, top pains, sales process description, user
   roles, and target Zoho CRM edition. If any of these cannot be determined from the inputs
   so far, do not guess — record each missing one as a `blocking` row in
   `03-open-questions.md` (Phase 2's template, created here if needed) and halt before Phase 1
   for that item. Only proceed past a blocking gap once the engineer provides an answer.

**Output**: `00-source-register.md`.

---

## Phase 1 — Extraction

**Input**: `00-source-register.md`, raw inputs.

**Steps**:
1. For every requirement (explicit or clearly implied) found in the inputs, create a row in
   `01-requirements-register.md` (copy `templates/requirements-register.md`) with:
   - A stable, sequential `REQ-###` ID (never reused across a re-run — research.md §4).
   - `statement`, `type` (functional/process/data/report/integration/compliance).
   - `source_id` (→ `00-source-register.md`) and a **verbatim** `quote` — both required, no
     exceptions (spec FR-002; data-model.md > Requirement validation).
   - `tag` — exactly one of `CUSTOMER`, `DOCS`, `WEB`, `ORG`, `INFERRED` (spec FR-003). An
     untagged factual claim anywhere in any document you produce — not just here — is invalid
     output; carry this discipline into every later phase too.
   - `confidence` (H/M/L) and `priority` (high/medium/low).
   - **Rule**: a row tagged `INFERRED` must never also be `confidence = H` — inference is
     never high-confidence fact (data-model.md > Requirement validation).
2. Also extract and append to the same document: a glossary of customer terms, actors/roles,
   entities and their lifecycles, volumes, existing systems/integrations mentioned, and ranked
   pains/KPIs.

**Output**: `01-requirements-register.md` (spec FR-002).

---

## Phase 2 — Synthesis & Gap Interview

**Input**: `01-requirements-register.md`.

**Steps**:
1. Write `02-customer-understanding.md` (copy `templates/customer-understanding.md`):
   business model, as-is vs. to-be process, entity lifecycles, stakeholders, and a
   terminology map (customer term → Zoho object/field equivalent).
2. **Precedence rule for conflicts** (spec Assumptions; research.md §/spec Assumptions): when
   two sources disagree, the default order is: most recent direct customer statement
   (call/email) > customer-supplied documents > the prospect's own public website > third-party
   web research > the agent's own inference. Apply this to decide which statement is the
   current truth — **but every conflict you detect, including ones resolved by this rule, MUST
   be recorded as a row in `03-open-questions.md`** (copy `templates/open-questions.md`),
   never silently dropped (spec FR-004). Mark conflict rows as `NON-BLOCKING` with the
   resolution explained, unless the conflict itself blocks a later phase.
3. Marketing-copy guard: treat a prospect website's aspirational claims (e.g., "zero missed
   deadlines", "fully automated") as `WEB`-tagged marketing language, never as a confirmed
   as-is process, unless a call or document independently confirms the same claim.
4. **Blocking halt** (spec FR-005; data-model.md > OpenQuestion validation): if any `BLOCKING`
   row in `03-open-questions.md` has no `resolution` yet, **stop here**. Present the engineer
   with the exact blocking question list from `03-open-questions.md` and wait. Do not proceed
   to Phase 3 until every blocking row is resolved.

**Output**: `02-customer-understanding.md`, `03-open-questions.md` (spec FR-004, FR-005).

---

## Phase 3 — Data Model

**Precondition**: zero unresolved `blocking` rows in `03-open-questions.md`.

**Input**: `01-requirements-register.md`, `02-customer-understanding.md`.

**Steps**:
1. Initialize this engagement's copy of `templates/handoff-spec.yaml` (the canonical model)
   with `prospect_slug`, `source_register_version`, `generated_at` filled in.
2. For every requirement needing a data element, decide the module/field placement:
   - **Prefer standard Zoho modules/fields.** Only introduce a custom module or field when no
     standard element can reasonably satisfy the same requirement(s) (spec FR-007;
     data-model.md > DesignModelElement validation: `is_standard = false` is only valid when no
     standard element satisfies the same `req_ids`).
   - Custom module only when the entity has its own lifecycle, ownership, or permissions
     distinct from existing modules, or represents a genuine many-to-many relationship that
     needs its own data (plan.md decision rules) — not just because a field doesn't fit neatly
     elsewhere.
   - Every module/field/relationship entry in the YAML **must** carry a non-empty `req_ids`
     list (spec FR-006, SC-002 — zero orphan elements). Never add an element "just in case."
3. **Capability verification** (spec FR-008): for any claim about what Zoho CRM can do, its
   limits, or edition availability, verify it against an authoritative Zoho Documentation
   source and cite it. If you cannot verify it, label it `[UNVERIFIED]` in the written
   document — never assert a capability, limit, or edition restriction from memory.
4. Write `04-data-model.md`: a field-level table per module (module, field, type, standard or
   custom, `req_ids`, notes/decision log), citing every capability claim per step 3.
5. Generate diagrams from the YAML, never by hand:
   - `python3 scripts/yaml_to_mermaid.py <engagement>.yaml 04a-erd-overview.mmd` (keys +
     relationships only, all modules).
   - For each domain with >~12 entities in the overview, generate a focused diagram:
     `python3 scripts/yaml_to_mermaid.py <engagement>.yaml 04b-erd-<domain>.mmd --domain
     <domain>`.
   - Embed both as fenced ` ```mermaid ` blocks inside `04-data-model.md` (spec FR-009 — the
     document and diagrams must never disagree, because the diagrams are generated from the
     same YAML the document describes, not hand-drawn).
6. Cardinality mapping when writing module relationships into the YAML (idea-doc Mermaid
   rules, carried through by the generator):
   - Lookup field on child → `many_to_one`.
   - Multi-select lookup → `many_to_many` (model a junction module if the relationship itself
     carries data).
   - Subform → `subform`, labeled `subform:<name>` (child has no independent lifecycle).
   - Self-reference (e.g., parent account) → relationship with `target_module` equal to its
     own module.

**Output**: `04-data-model.md`, `04a-erd-overview.mmd`, `04b-erd-<domain>.mmd` (spec FR-006,
FR-007, FR-008, FR-009).

---

## Phase 4 — Pipelines

**Input**: `04-data-model.md` + YAML.

**Steps**: For each pipeline the prospect needs (default: one, unless requirements call for
more — spec Assumptions), define stages in the YAML `pipelines` section and in
`05-pipelines.md`: `name`, `probability`, `forecast_category`, `entry_criteria`,
`exit_criteria`, `required_fields` (must already exist in the Phase 3 data model —
data-model.md > PipelineStage validation), and `req_ids` (non-empty).

**Output**: `05-pipelines.md` (spec FR-010).

---

## Phase 5 — Blueprints

**Input**: `04-data-model.md` + YAML.

**Steps**: Write `06-blueprint-leads.md` and `07-blueprint-deals.md`. For each state and
transition: `mandatory_fields` (must resolve to existing data-model elements), `validations`,
`approvals`, `time_rules`, and `req_ids` (non-empty). Every state must map to an actual field
value in the data model (data-model.md > BlueprintState/Transition validation). Include a
Mermaid state diagram per blueprint, generated the same disciplined way as Phase 3's ER
diagrams (hand-drawn-but-reference-checked is acceptable here since state diagrams are not
produced by `yaml_to_mermaid.py`; cross-check every state/field name against the YAML before
finalizing).

**Output**: `06-blueprint-leads.md`, `07-blueprint-deals.md` (spec FR-011).

---

## Phase 6 — Automation

**Input**: `04-data-model.md`, `05-pipelines.md`, blueprints.

**Steps**: Write `08-automation.md` with workflow and assignment rules: `trigger`,
`condition`, `action`, `reads_fields`, `writes_fields`, `req_ids` (non-empty). After drafting
all rules, scan for conflicts: flag any two rules that both write the same field, and flag any
trigger→action chain that could re-trigger itself (a loop) (spec FR-012; data-model.md >
AutomationRule validation).

**Output**: `08-automation.md` (spec FR-012).

---

## Phase 7 — Personas & Home Pages

**Input**: `02-customer-understanding.md` (roles discovered), `04-data-model.md`.

**Steps**: Select personas from the roles actually discovered during discovery — not a fixed
universal list — and confirm the selection with the engineer (spec Assumptions). For each
persona, write goals, daily decisions, dashboard layout, reports, and KPIs into
`09-personas-homepages.md`. **Every KPI's `source_fields` must resolve to an existing
data-model element** (data-model.md > PersonaHomePage validation, spec FR-013). If a KPI the
prospect wants cannot be computed from the current data model, either add the missing field in
the Phase 3 model (and keep it REQ-ID-justified) or drop the KPI — never leave an unsupported
KPI in the document.

**Output**: `09-personas-homepages.md` (spec FR-013).

---

## Phase 8 — Validation (mandatory gate before handoff)

**Input**: all documents produced so far.

**Steps**: Run every check below and record pass/fail for each as a `ValidationRun` with a
`blocking_failure_count`:
1. No orphan design elements — every module/field/relationship/stage/state/rule/KPI has a
   non-empty `req_ids`.
2. Every field/module/stage/value referenced anywhere (blueprint, automation, dashboard)
   exists in `04-data-model.md` with a matching type.
3. Every stage/state/picklist value used anywhere matches its canonical definition.
4. Every requirement in `01-requirements-register.md` is either covered, partial, a gap (with
   rationale), or deferred — write this mapping into `10-traceability-matrix.md` (spec
   FR-016).
5. Every `[DOCS]`-tagged claim has a citation; every `[UNVERIFIED]` claim is listed.
6. **Every factual claim across *all* produced documents — not only the requirements register
   and data-model capability claims — carries one of `[CUSTOMER]`/`[DOCS]`/`[WEB]`/`[ORG]`/
   `[INFERRED]`** (spec FR-003). Scan `02-customer-understanding.md`,
   `09-personas-homepages.md`, and the automation/blueprint documents too, not just Phases 1
   and 3.
7. Naming conventions (labels, API names, terminology map) are consistent across all
   documents.
8. Every `.mmd` file renders without error (`npx -p @mermaid-js/mermaid-cli mmdc -i file.mmd -o
   out.svg`).
9. Every entity in the diagrams exists as a module in the YAML, and vice versa; every
   attribute in the diagrams matches the YAML with the same API name and type token; the
   overview diagram's entity set equals the union of the per-domain diagrams' entity sets.
10. No entity or attribute lacks a `req_ids` comment, except explicitly-listed system fields.

**If any check fails**: fix the underlying document, don't suppress the failure, and re-run
validation. **Do not proceed to Phase 9 while `blocking_failure_count > 0`** (spec FR-014,
FR-015; data-model.md > ValidationRun).

**Output**: `10-traceability-matrix.md`, a `ValidationRun` record (spec FR-014, FR-015,
FR-016).

---

## Phase 9 — Handoff

**Precondition**: the latest `ValidationRun.blocking_failure_count == 0`.

**Steps**:
1. Write `11-assumptions-risks-review.md`: every assumption made, every `[INFERRED]` item,
   every `[HUMAN REVIEW]`-flagged item (see the regulated-claims guard below), and known risks.
2. Finalize the engagement's YAML as `12-handoff-spec.yaml`, matching
   `specs/004-crm-data-model-customizer/contracts/handoff-spec.schema.md` exactly: `modules`,
   `pipelines`, `blueprints`, `automation_rules`, `personas`, `traceability_summary`,
   `validation`, `erd_source` (path to the overview `.mmd`), and `erd_content_hash` (hash of
   the modules/fields/relationships section, so the downstream agent can detect staleness)
   (spec FR-017; data-model.md > HandoffPackage).
3. Print the final summary (see "Final summary" below).

**Output**: `11-assumptions-risks-review.md`, `12-handoff-spec.yaml` (spec FR-015, FR-017).

This is the single artifact a separate, downstream demo-building agent consumes. This skill
has no knowledge of and no dependency on that agent's internals — see the contract's
"Non-goals" section.

---

## Regulated-claims guard (applies across Phases 4–9)

Any pricing, discount, roadmap date, SLA, certification, contract term, or competitor claim
**must not** be asserted in any document unless backed by a cited authoritative source. If you
cannot cite one, flag it `[HUMAN REVIEW]` in the document instead of stating it as fact (spec
FR-020).

## Incremental re-run behavior

When the engineer supplies new or corrected inputs after an initial run: diff the new inputs
against `00-source-register.md`, add new `SRC-###`/`REQ-###` entries rather than renumbering
existing ones, update only the documents actually affected by the change, and append a dated
changelog entry at the top of each updated document describing what changed and why. Never
discard prior, still-valid work and start over (spec FR-022, SC-007).

## Final summary

At the end of any run (full or incremental), report: files written, requirement counts by
status (covered/partial/gap/deferred), remaining blocking questions (should be zero at
handoff), and counts of `[UNVERIFIED]` and `[HUMAN REVIEW]` items.
