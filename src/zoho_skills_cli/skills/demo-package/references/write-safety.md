# Write Safety (cross-cutting, all phases)

This applies at every phase of the pipeline, not just Phase 1 introspection — any point where
the skill considers touching the demo org is subject to this protocol.

## Default: read-only

By default, only read operations against the Zoho CRM demo org are permitted (`getModules`,
`getFields`, `getRecords`, `searchRecords`, `executeCOQLQuery`, etc.). No create, update, or
delete operation runs without going through the approval protocol below.

## Approval protocol

If, at any phase, the skill identifies a write that would improve the demo (e.g., seeding a
missing sample record so a scene has demo-worthy data, or tagging a record for the walkthrough):

1. **Stop.** Do not perform the write.
2. **Present the exact action**: which record/field/module, the exact operation (create/update/
   delete), and the exact values involved. Vague descriptions ("I'll add some sample data") are
   not sufficient — state precisely what will change.
3. **Wait for the engineer's explicit "yes"** to that specific action. A general "sounds good,
   proceed" earlier in the conversation does not count as approval for a specific write raised
   later — each write needs its own explicit approval.
4. **If approved**: perform exactly that action, nothing more, and confirm what was done.
5. **If declined or ignored**: skip the write, continue read-only, and note the skipped
   opportunity in `gaps-and-risks.md` (Phase 6) so the engineer knows it's still available if
   they change their mind.

## Why this exists

The demo org is a shared asset used across multiple prospects and engagements. A single
unapproved write can silently break a future demo relied on for another active deal. This
protocol trades a small amount of friction for full engineer control over the org's state.
