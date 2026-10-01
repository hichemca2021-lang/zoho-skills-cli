# Phase 1: Org Introspection

Goal: produce a timestamped, complete-as-possible picture of what actually exists in the demo
org, so nothing downstream can reference something that isn't real. This phase is read-only.

Field contracts for the output are in `references/schemas.md` (org-snapshot.json section).

## Tool-to-field mapping

For each `org-snapshot.json` field, use these Zoho CRM MCP tools to populate it:

| Snapshot field | Tool call(s) |
|---|---|
| `modules[]` (standard + custom) | `getModules`, `getModuleByApiName` |
| `modules[].fields` | `getFields` |
| `modules[].related_lists` | `getRelatedLists` |
| `automation[]` (blueprints, workflows, assignment/scoring rules) | `getAssignmentRules`; blueprint stage/transition data via `getLayouts` where exposed |
| `access_model` (roles, territories) | `getUsers`, `getAllTerritories` |
| `pipelines[]` (deal/project/opportunity stages) | `getFields` (picklist values on stage fields), `getLayouts` |
| `reporting_assets[]` (dashboards, reports, Canvas) | `getModules`/`getLayouts` where exposed; note as unreadable if not |
| `record_quality[]` | `getRecords` / `searchRecords` / `executeCOQLQuery` (sample counts and completeness) |
| `unreadable_areas[]` | Anything the above calls do not return — see below |

## The unreadable-areas rule

Before designing any scene, determine empirically what the available tools can and cannot
return. For anything spec.md FR-003 asks for that these tool calls do not surface (e.g., custom
function bodies, Canvas view definitions, Zia configuration, full sharing-rule detail), add an
entry to `unreadable_areas[]` with the area name and a short reason. Anything listed here MUST
NOT be referenced in any later phase — it is not "confirmed to exist" per the org-grounded-truth
rule.

## Producing org-model.md and the ER diagram

After `org-snapshot.json` is written:

1. Generate `org-model.md`: a human-readable summary of the snapshot — module list with field
   counts, automation found, pipelines and their stages, reporting assets, and the
   `unreadable_areas` list stated plainly so the engineer knows the introspection boundary.
2. Generate a Mermaid entity-relationship diagram derived directly from the same
   `org-snapshot.json` (modules as entities, `related_lists`/lookups as relationships), embedded
   as a ```mermaid code block inside `org-model.md`. Generate it from the JSON, not by hand, so
   the diagram and the snapshot never drift apart within a run.

## Record-quality / demo-worthy assessment

For each module with sample data, assess `demo_worthy: true/false` based on: record presence,
field completeness on the records that would appear in a scene, and general realism (no
obviously placeholder data like "Test Test"). A module with `demo_worthy: false` should not be
the basis of a scene in Phase 4 unless the engineer is informed and accepts the risk.

## Output

- `output/<customer-slug>/org-snapshot.json` — the structured snapshot, timestamped via
  `captured_at`.
- `output/<customer-slug>/org-model.md` — the human-readable summary + embedded ER diagram.

Proceed to Phase 2 (`references/customer-model.md`) once both files are written.
