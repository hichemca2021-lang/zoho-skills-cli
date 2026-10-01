# Source Tagging & Regulated Claims

Used by Phase 5 (transcript) when writing every claim, and by Phase 6 (validation) when
checking the transcript for compliance. This is not its own pipeline phase — it's a shared rule.

## The six source tags

Every factual claim in every generated artifact carries exactly one of:

| Tag | Meaning |
|---|---|
| `ORG` | Directly observed in `org-snapshot.json` / the live demo org |
| `DOCS` | Confirmed on an official Zoho documentation/help-center domain |
| `CUSTOMER` | Stated by the customer in the Brief or Detailed Case |
| `WEB` | From general web research (not an official Zoho domain), on the customer/industry |
| `INFERRED` | Reasoning the agent performed itself, not a verification of an external fact |
| `UNVERIFIED` | A Zoho product-capability claim that could not be confirmed against `DOCS` or `WEB` |

A claim with no tag is invalid output — it must be tagged or removed before delivery.

## Source hierarchy for Zoho product-capability claims

1. Check official Zoho documentation domains first. If confirmed, tag `DOCS` (cite the page).
2. If not found there, check general web sources. If confirmed, tag `WEB`.
3. If neither confirms it, tag `UNVERIFIED` — never assert it under `DOCS`, `WEB`, or any other
   tag just because it sounds plausible or matches trained knowledge of Zoho CRM. `INFERRED` is
   reserved for the agent's own reasoning, not for unconfirmed product facts.

## Regulated claims

Any claim about pricing, discounts, roadmap dates, SLAs, certifications, contract terms, or
competitor feature/pricing comparisons is regulated:

- If it has a `DOCS` citation, it may be stated, tagged `DOCS`, with the citation.
- Otherwise, it MUST be written with `human_review: true` and a `human_review_reason`, and MUST
  NOT be phrased as a plain asserted fact anywhere in `demo-script.md`. Route it to
  `gaps-and-risks.md` for the engineer to resolve manually.

## Applying this in practice

When drafting transcript claims (Phase 5), decompose each spoken sentence into its constituent
factual claims and tag each one individually per `references/schemas.md`'s `claims[]` structure.
A single spoken sentence may contain claims with different tags (e.g., an `ORG` observation
followed by a `DOCS`-sourced explanation of why the feature behaves that way).
