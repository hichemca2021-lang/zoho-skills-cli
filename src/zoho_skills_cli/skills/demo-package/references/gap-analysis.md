# Phase 3: Gap Analysis

Goal: classify every customer requirement (one per pain, from the Customer Detailed Case)
against what Phase 1 introspection confirmed exists in the org. Field contract:
`references/schemas.md` (coverage-matrix.json section).

## Status rules

- `status` MUST be exactly one of `COVERED`, `PARTIAL`, `GAP` — no other values, no blends.
- `COVERED`: the org has a real, demo-worthy capability that fully addresses the pain.
  `matched_org_items` lists the specific module/field/automation involved.
- `PARTIAL`: a related capability exists but falls short in some specific, statable way (e.g.,
  the field exists but sample data isn't demo-worthy, or it covers part of the pain but not all
  of it). `limitation` MUST be non-empty and specific.
- `GAP`: no matching org capability exists at all. `gap_reason` MUST be non-empty and specific.
  A `GAP` row's `matched_org_items` MUST be empty.

## The gap-exclusion rule

A `GAP` row's `requirement_id` MUST NOT appear as the `pain_id` of any Demo Plan scene where
`is_honest_answer_scene` is `false` or absent (constitution Principle I, spec.md FR-008). It may
only be referenced by a scene explicitly marked `is_honest_answer_scene: true` — see
`references/demo-plan.md`'s honest-answer scene rule. This is what Phase 4 enforces; this phase
just needs to classify accurately so Phase 4 has correct input.

## human_review on coverage rows

If determining a requirement's status would itself require asserting a regulated claim (e.g.,
"this will be covered once the roadmap ships X"), do not write that into `limitation` or
`gap_reason` as fact. Instead set `human_review: true` with a `human_review_reason` explaining
why, and keep the `status` based only on what's confirmed today.

## Output

`output/<customer-slug>/coverage-matrix.md` (human-readable table) plus the backing
`coverage-matrix.json`.

Proceed to Phase 4 (`references/demo-plan.md`) once this file is written.
