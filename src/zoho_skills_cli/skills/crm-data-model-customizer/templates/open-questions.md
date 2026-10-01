# Open Questions: [PROSPECT NAME]

**Version**: [N] | **Date**: [DATE] | **Status**: [Draft/Final]

## BLOCKING

> A phase MUST NOT proceed past a point depending on a BLOCKING question with no resolution
> (data-model.md > OpenQuestion validation; spec FR-005).

| ID | Decision Unblocked | Proposed Default | Conflicting Source IDs | Resolution |
|----|----------------------|-------------------|--------------------------|------------|
| OQ-001 | [what this decision gates] | [default if any] | [SRC-### list, if conflict-driven] | _(pending)_ |

## NON-BLOCKING

| ID | Decision Unblocked | Proposed Default | Conflicting Source IDs | Resolution |
|----|----------------------|-------------------|--------------------------|------------|
| OQ-101 | [what this decision affects] | [default if any] | [SRC-### list, if conflict-driven] | [resolved value, or "resolved by precedence rule: ..."] |

<!--
  Every detected source conflict MUST appear here (spec FR-004), even if resolved by the
  default precedence rule (most recent customer statement > customer docs > prospect website
  > third-party web > INFERRED) — resolution-by-precedence is still recorded, never silent.
-->
