# Phase 5: Transcript

Goal: write the full spoken walkthrough aligned 1:1 with the Demo Plan's scenes, with every
factual claim source-tagged. Field contract: `references/schemas.md` (transcript.json section).
Tagging rules: `references/source-tagging.md`.

## Rules

- One `scenes[]` entry per Demo Plan scene, same `scene_id`, in the same order.
- `spoken_text` is the natural narration a human would actually say live — write it that way,
  not as a bulleted feature list.
- Decompose `spoken_text` into `claims[]`: every discrete factual assertion gets its own entry
  with exactly one `source_tag` (see `references/source-tagging.md` for the six tags and the
  Zoho-docs-first hierarchy). Non-factual narration (transitions, rhetorical questions, stage
  directions) does not need a claim entry.
- Apply the regulated-claims rule from `references/source-tagging.md` to any pricing, SLA,
  roadmap, certification, contract, or competitor statement before it goes in `spoken_text`.
- For an honest-answer scene (see `references/demo-plan.md`), the transcript should state the
  gap plainly and constructively — this is still subject to the same tagging rules; do not turn
  candor into an unsourced claim about a future fix.

## Output

`output/<customer-slug>/demo-script.md` (human-readable, with the `claims[]` decomposition
either inline as annotations or as a parallel structured section the engineer can audit).

Proceed to Phase 6 (`references/validation.md`) once this file is written.
