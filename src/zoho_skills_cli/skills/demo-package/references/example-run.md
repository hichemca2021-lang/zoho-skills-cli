# Worked Example: One Complete Scene

This is a grounding example, not a template to copy verbatim — every field must come from a
real `org-snapshot.json` and a real Customer Detailed Case, never from this example.

## Input fragments

Customer Detailed Case pain:

```json
{
  "pain_id": "pain-1",
  "rank": 1,
  "customer_words": "Deals just sit there and nobody notices until it's too late to save them",
  "quantified_impact": "Est. $400K in stalled pipeline last quarter",
  "process_location": "pipeline",
  "affected_role": "Sales Manager",
  "failure_example": "A $120K deal sat in Proposal for 6 weeks with no follow-up before it was lost",
  "root_cause": "No automated alert when a deal stalls in a stage",
  "priority_flag": "must-solve"
}
```

Matching org-snapshot.json fragment: a `Deals` module with a `Stage` field and a `Deal Approval`
blueprint (`introspectable: true`).

## Resulting coverage-matrix.json row

```json
{ "requirement_id": "pain-1", "status": "COVERED", "matched_org_items": ["Deals.Stage", "Deals blueprint: Deal Approval"], "limitation": null, "gap_reason": null, "human_review": false, "human_review_reason": null }
```

## Resulting demo-plan.json scene

```json
{
  "scene_id": "scene-1",
  "order": 1,
  "title": "Stopping deals from silently stalling",
  "pain_id": "pain-1",
  "capability": "Deals blueprint: Deal Approval + Stage field",
  "screen_path": "Deals module > [Demo Account] deal record > Stage field > click 'Move to Proposal'",
  "outcome": "Sales manager sees exactly which deals are stuck and why, before they die in pipeline",
  "timing_minutes": 5,
  "is_honest_answer_scene": false
}
```

## Resulting transcript.json scene

```json
{
  "scene_id": "scene-1",
  "spoken_text": "Let's look at a deal that's been sitting in Proposal without movement. Here, in the Deals module, the Stage field shows exactly how long it's been stuck. Zoho's Blueprint feature can enforce an approval step here automatically, so a deal like this can't silently sit for six weeks the way it did last quarter.",
  "claims": [
    { "text": "This deal has been in Proposal stage without an update for an extended period", "source_tag": "ORG", "human_review": false, "human_review_reason": null },
    { "text": "Zoho's Blueprint feature can enforce an approval step at a given stage automatically", "source_tag": "DOCS", "human_review": false, "human_review_reason": null },
    { "text": "A deal sat in Proposal for 6 weeks with no follow-up before it was lost", "source_tag": "CUSTOMER", "human_review": false, "human_review_reason": null }
  ]
}
```

Notice: the org observation (`ORG`), the product-capability explanation (`DOCS`), and the
customer's own failure example (`CUSTOMER`) are three separate, individually tagged claims
within one natural spoken paragraph — this is the level of decomposition every scene needs.
