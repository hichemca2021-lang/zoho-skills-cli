# Phase 2: Customer Model

Goal: turn the validated Customer Brief and Customer Detailed Case (from Phase 0) into a single
readable `customer-profile.md`, without adding anything not present in the input.

## Rules

- Use only what the engineer supplied in the Customer Brief and Customer Detailed Case. Do not
  invent additional pains, roles, tools, or details, even if they seem plausible for the
  industry — that belongs in Phase 3/4 as `WEB`-tagged industry context if used at all, never
  silently folded into the customer's own profile as if the customer said it.
- Preserve each pain's `customer_words` verbatim — do not paraphrase the customer's own language
  when quoting them.
- Order pains by `rank` (highest priority first).

## customer-profile.md structure

1. **Company overview**: `company`, `industry`, `size`, `current_tools_process`.
2. **Audience & format**: `audience_roles`, `demo_duration`, `success_criteria`.
3. **Pains** (one subsection per pain, in rank order): `customer_words` quote,
   `quantified_impact`, `process_location`, `affected_role`, `failure_example`, `root_cause`,
   `evaluation_trigger`, `prior_attempts`, `priority_flag`.

## Output

`output/<customer-slug>/customer-profile.md`.

Proceed to Phase 3 (`references/gap-analysis.md`), which uses both this profile and
`org-snapshot.json` from Phase 1.
