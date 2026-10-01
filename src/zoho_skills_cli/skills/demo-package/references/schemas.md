# Schemas Reference

Consolidated field contracts for every artifact the `demo-package` skill produces. This is the
single authoritative reference every phase file (`references/*.md`) should cite instead of
restating field lists inline. Source of truth: `specs/001-demo-package-generator/contracts/`.

## org-snapshot.json (Phase 1 output)

```json
{
  "captured_at": "2026-09-30T14:00:00Z",
  "modules": [
    {
      "api_name": "Deals",
      "label": "Deals",
      "is_custom": false,
      "fields": [
        { "api_name": "Stage", "type": "picklist", "required": true, "picklist_values": ["Qualification", "Closed Won"] },
        { "api_name": "Amount", "type": "currency", "required": false }
      ],
      "related_lists": ["Contacts", "Activities"]
    }
  ],
  "automation": [
    { "type": "blueprint", "name": "Deal Approval", "introspectable": true },
    { "type": "custom_function", "name": "score_lead", "introspectable": false }
  ],
  "access_model": { "roles": ["Sales Rep", "Sales Manager"], "territories": ["North America"] },
  "pipelines": [
    { "module": "Deals", "stages": ["Qualification", "Proposal", "Closed Won", "Closed Lost"] }
  ],
  "reporting_assets": [ { "type": "dashboard", "name": "Pipeline Overview" } ],
  "record_quality": [ { "module": "Deals", "sample_count": 42, "demo_worthy": true } ],
  "unreadable_areas": [
    { "area": "Canvas views", "reason": "not exposed by available connector tools" }
  ]
}
```

Rules:
- `captured_at` MUST be set every time this file is written (Phase 1 and Phase 6).
- Anything not present under `modules`, `automation` (`introspectable: true`), `pipelines`, or
  `reporting_assets` is treated as non-existent for demo-scripting purposes.
- `unreadable_areas` MUST list anything the connector could not return, so downstream phases and
  the engineer both know the introspection boundary.

## coverage-matrix.json (Phase 3 output)

```json
{
  "requirements": [
    {
      "requirement_id": "pain-1",
      "status": "COVERED",
      "matched_org_items": ["Deals.Stage", "Deals blueprint: Deal Approval"],
      "limitation": null,
      "gap_reason": null,
      "human_review": false,
      "human_review_reason": null
    }
  ]
}
```

Rules:
- `status` MUST be one of `COVERED`, `PARTIAL`, `GAP` — no other values.
- `PARTIAL` rows MUST have a non-empty `limitation`.
- `GAP` rows MUST have a non-empty `gap_reason` and MUST NOT appear in `matched_org_items` for
  any non-honest-answer Demo Scene.
- `requirement_id` MUST correspond 1:1 to a `pain_id` from the Customer Detailed Case.

## demo-plan.json (Phase 4 output, backs demo-plan.md / demo-plan.html)

```json
{
  "intro": {
    "narrative": "Short framing of why this demo, for whom, and what it will prove",
    "audience_roles": ["VP Sales", "RevOps Manager"],
    "demo_duration_minutes": 30
  },
  "scenes": [
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
  ],
  "total_timing_minutes": 28
}
```

Rules:
- Every scene where `is_honest_answer_scene: false` MUST have non-null `pain_id`, `capability`,
  `screen_path`, and `outcome`.
- `capability` and `screen_path` MUST reference items present in the current `org-snapshot.json`.
- A scene MAY only set `pain_id` to a `GAP`-status requirement if `is_honest_answer_scene: true`.
- `total_timing_minutes` SHOULD NOT exceed `intro.demo_duration_minutes`; if it does, surface the
  mismatch rather than silently truncating.

## transcript.json (Phase 5 output, backs demo-script.md)

```json
{
  "scenes": [
    {
      "scene_id": "scene-1",
      "spoken_text": "Let's look at how deals get stuck in Proposal today...",
      "claims": [
        { "text": "This deal has been in Proposal stage for 14 days without an update", "source_tag": "ORG", "human_review": false, "human_review_reason": null },
        { "text": "Zoho's Blueprint feature enforces this approval step automatically", "source_tag": "DOCS", "human_review": false, "human_review_reason": null },
        { "text": "Teams using this pattern typically resolve stalled deals faster", "source_tag": "INFERRED", "human_review": false, "human_review_reason": null },
        { "text": "Zoho CRM supports real-time inventory sync across all warehouses", "source_tag": "UNVERIFIED", "human_review": false, "human_review_reason": null }
      ]
    }
  ]
}
```

Rules:
- Every `claims[]` entry MUST have exactly one `source_tag` from
  `{ORG, DOCS, CUSTOMER, WEB, INFERRED, UNVERIFIED}`.
- A Zoho product-capability claim that cannot be confirmed against `DOCS` or `WEB` MUST use
  `source_tag: "UNVERIFIED"` rather than being asserted under any other tag.
- A claim matching pricing, discounts, roadmap dates, SLAs, certifications, contract terms, or
  competitor feature/pricing comparisons MUST have `source_tag: "DOCS"` with a citation, or MUST
  have `human_review: true` and a `human_review_reason` — never a plain asserted claim.
