# Phase 6: Validation

Goal: catch two kinds of pre-delivery risk before the engineer walks into the room — org drift
since Phase 1, and unsourced/unchecked claims in the transcript. This is the final phase; nothing
ships until it passes or its failures are resolved.

## Drift check (org re-read)

1. Re-run the same introspection calls used in Phase 1 (see
   `references/org-introspection.md`'s tool-to-field mapping) to produce a fresh snapshot.
2. For every scene in `demo-plan.json`, check that its `capability` and `screen_path` still
   resolve against the fresh snapshot.
3. Produce `scene_results[]`: one entry per scene, `{ scene_id, status: PASS|FAIL,
   failure_reason? }`. Any scene whose referenced item is missing or changed gets `status: FAIL`
   with a specific `failure_reason` — never silently left as passing.
4. Set `drift_detected: true` if any scene failed for this reason.

## Transcript claim check

1. Re-read `demo-script.md`'s `claims[]` for every scene.
2. Confirm every claim has exactly one `source_tag` from
   `{ORG, DOCS, CUSTOMER, WEB, INFERRED, UNVERIFIED}` (spec.md SC-003). Any claim missing a tag,
   or carrying more than one, fails this check for its scene.
3. Confirm every claim matching pricing, discounts, roadmap dates, SLAs, certifications,
   contract terms, or competitor feature/pricing comparisons either has `source_tag: "DOCS"` with
   a citation, or has `human_review: true` with a `human_review_reason` (spec.md SC-005,
   FR-012). Any regulated claim that is a plain, uncited, non-flagged assertion fails this check.
4. Any scene that fails either part of this check gets added to `scene_results[]` as `FAIL` (if
   not already failing from drift) and every failing claim is added to `human_review_items[]`.
   A scene failing this check blocks delivery of that scene until corrected — it is not
   sufficient to just note it and ship anyway.

## Producing the delivery artifacts

- `output/<customer-slug>/gaps-and-risks.md`: every `GAP` coverage row, every `PARTIAL`
  limitation, every timing mismatch (from Phase 4), and every `human_review_items[]` entry from
  this phase — this is where anything not fit for the live script surfaces for the engineer.
- `output/<customer-slug>/summary.md`: the Delivery Summary —
  `artifacts_written` (list of files produced), `coverage_counts`
  (`{ covered, partial, gap }` from the coverage matrix), `open_questions[]`, and
  `human_review_items[]` (spec.md FR-017).

## Output

`output/<customer-slug>/gaps-and-risks.md`, `output/<customer-slug>/summary.md`.

This is the last phase. Report the delivery summary to the engineer per `SKILL.md`'s
"How to run this skill" step 4.
