# Phase 0: Intake Gate

Run this before any other phase. Do not proceed to Phase 1 until every check below passes.

## Required: Customer Brief

All of the following fields are required. If any is missing, halt and list exactly which ones:

- `company`
- `industry`
- `size`
- `pain_points` (summary list)
- `current_tools_process`
- `audience_roles` (list)
- `demo_duration`
- `success_criteria`

## Required: Customer Detailed Case

One entry per pain. Each entry requires:

- `pain_id`, `rank`
- `customer_words` (verbatim quote)
- `quantified_impact`
- `process_location` — one of: `lead capture`, `qualification`, `pipeline`, `quoting`,
  `handoff`, `renewal`, `reporting`
- `affected_role`
- `failure_example`
- `root_cause`
- `evaluation_trigger`
- `prior_attempts`
- `priority_flag` — `must-solve` or `nice-to-solve`

If any pain entry is missing a required field, halt and list exactly which pain and which
field(s) are missing.

## Must-solve validation rule

A pain flagged `priority_flag: must-solve` MUST have non-empty `quantified_impact` AND
non-empty `failure_example`. If either is empty for a must-solve pain, flag that pain as
insufficiently specified and halt — do not silently downgrade it or proceed without it. Name
the specific pain and the specific missing field(s) when you ask.

## Halting behavior

When any of the above checks fail:

1. Do not generate any demo content.
2. List every missing or insufficient field/pain in one message (not one round-trip per field).
3. Wait for the engineer to supply the missing information before re-attempting Phase 0.

When all checks pass, proceed to Phase 1 (`references/org-introspection.md`) using the
validated Customer Brief and Customer Detailed Case as input to Phase 2
(`references/customer-model.md`) and Phase 3 (`references/gap-analysis.md`).
