# Origin Tags

Every statement written into `customer-brief.md` MUST carry exactly one of the tags below. An
untagged factual statement is invalid output (spec FR-003) and must be fixed before the brief is
considered complete (SC-002).

| Tag | Meaning | When to use |
|---|---|---|
| `[CUSTOMER]` | The customer said this unprompted, in open-question form. | Default tag for any direct answer not offered as a suggestion. |
| `[SUGGESTED-ACCEPTED]` | The agent offered this as one of 2-3 options (with a recommended default) and the customer picked it. | Only after the open-first-then-suggest flow (FR-004) and the customer explicitly chose one of the offered options. |
| `[SUGGESTED-REJECTED]` | The agent offered suggested options and the customer declined all of them. | Record what was offered and that none were accepted; do not treat this as a confirmed requirement. |
| `[UNDECIDED-DELEGATED]` | The customer said "whatever you think is best" or equivalent, declining to decide. | Never recorded as a requirement. Downstream questions depending on this one must be skipped/deferred (FR-006). |
| `[WEB]` | A finding sourced from the prospect's public website or other public web research. | Only ever a *finding to confirm*, never written into a coverage section until confirmed (FR-008). |
| `[DOC]` | A finding sourced from a document the prospect or pre-sales engineer provided. | Same promotion rule as `[WEB]` (FR-008). |
| `[INFERRED]` | Reasoning the agent performed itself — e.g., an industry-standard pattern offered only as the basis for a suggested option. | Never presented as the customer's own fact (FR-009). Used for the suggestion itself, not for the customer's eventual answer (which gets `[SUGGESTED-ACCEPTED]`/`[SUGGESTED-REJECTED]`/`[UNDECIDED-DELEGATED]` instead). |

## Promotion rule (FR-008)

An answer tagged `[WEB]` or `[DOC]` MUST NOT be treated as `[CUSTOMER]`-equivalent confirmed fact
until a later Captured Answer with the same `question_id` and a confirming origin tag exists.
Concretely:

1. The agent presents the `[WEB]`/`[DOC]` finding back to the customer ("Your website says you
   serve mainly small retailers — is that still accurate?").
2. If the customer confirms it directly, re-tag the statement `[CUSTOMER]`.
3. If the agent offered it as one of several suggested options instead, re-tag
   `[SUGGESTED-ACCEPTED]` or `[SUGGESTED-REJECTED]` based on the customer's choice.
4. Until step 2 or 3 happens, the finding stays in the brief's "Unconfirmed Findings" section,
   tagged `[WEB]`/`[DOC]`, and MUST NOT appear in any of the five coverage sections.

## Industry-norm rule (FR-009)

An industry-standard pattern or norm (e.g., "most businesses in this vertical track deals by
stage and close date") must never be written as if it were the customer's own fact. It may only
be used as the basis for a suggested option during the open-first-then-suggest flow, and any
statement of the pattern itself is tagged `[WEB]` (if drawn from external research) or
`[INFERRED]` (if the agent reasoned it out). The customer's eventual answer to that suggestion is
tagged per the normal suggestion rules (`[SUGGESTED-ACCEPTED]`/`[SUGGESTED-REJECTED]`), never
`[INFERRED]` itself.
