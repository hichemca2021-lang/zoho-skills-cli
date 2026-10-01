# Phase 4: Demo Plan

Goal: turn the coverage matrix (Phase 3) and org snapshot (Phase 1) into an ordered set of
scenes, each with a full pain → capability → screen → outcome chain, plus intro/outro framing.
Field contract: `references/schemas.md` (demo-plan.json section).

## Scene rules

- Every non-honest-answer scene MUST have non-null `pain_id`, `capability`, `screen_path`, and
  `outcome` (constitution Principle II, spec.md FR-009). A scene missing any of these is
  incomplete and must not ship.
- `capability` and `screen_path` MUST resolve to items actually present in the current
  `org-snapshot.json` (constitution Principle I, spec.md FR-006). If a scene idea depends on
  something not in the snapshot, drop the scene — do not describe it anyway.
- `pain_id` MUST reference a pain from the Customer Detailed Case, matched via the coverage
  matrix's `requirement_id`.

## Honest-answer scene rule

A scene MAY set `pain_id` to a requirement whose coverage status is `GAP` **only if**
`is_honest_answer_scene: true`. This is the one place a gap is allowed to be discussed directly
with the prospect — framed as a candid, expectations-setting moment, not a workaround or a
disguised feature claim. No other scene may reference a `GAP` row in any form (spec.md FR-008).
For an honest-answer scene, `capability` and `screen_path` may be `null` since there is nothing
on-screen to show; `outcome` should describe the trust/expectation-setting value instead of a
product outcome.

## Intro/outro framing

Set `intro.narrative`, `intro.audience_roles` (from the Customer Brief), and
`intro.demo_duration_minutes` (from the Customer Brief's `demo_duration`).

## Timing mismatch rule

Sum each scene's `timing_minutes` into `total_timing_minutes`. If this exceeds
`intro.demo_duration_minutes`, do not silently drop or compress scenes — surface the mismatch
explicitly (e.g., in `gaps-and-risks.md` via Phase 6) and propose which lower-rank pains to cut,
letting the engineer decide.

## Outputs

- `output/<customer-slug>/demo-plan.md` — the human-readable plan.
- `output/<customer-slug>/demo-plan.html` — the same content rendered as a standalone HTML page,
  embedding the Mermaid ER diagram from `org-model.md` (Phase 1) via a CDN-hosted `mermaid.js`
  `<script>` include so it renders live in a browser. No build step or bundler — a single static
  HTML file with the diagram's Mermaid source in a `<pre class="mermaid">` block (or equivalent)
  and the CDN script tag is sufficient.

Proceed to Phase 5 (`references/transcript.md`) once both files are written.
