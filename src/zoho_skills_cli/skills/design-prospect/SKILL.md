---
name: design-prospect
description: Guided intake for starting a new CRM design engagement. Use when a pre-sales engineer wants to start designing a Zoho CRM solution for a prospect but hasn't yet gathered or organized their discovery material. Walks them through what to provide, then hands off to the crm-data-model-customizer skill. Trigger phrases: "design a CRM for <prospect>", "start a new prospect", "I have a call transcript for <prospect>", "let's design the CRM for <prospect>".
---

# Design Prospect (guided intake)

> **Process**: CRM Design, guided intake — the front door into CRM Design
> (`crm-data-model-customizer`) for an engineer who hasn't yet gathered discovery material.
> **Outcome**: discovery material organized and handed off to `crm-data-model-customizer`.

This is the front door for a pre-sales engineer who wants to start a CRM design engagement but
doesn't want to think about file formats, phases, or which skill to call. Your job here is
only to **gather what's needed, in plain conversation, then hand off** — the actual design work
happens in the `crm-data-model-customizer` skill, not here.

## What you need before handing off

Ask for these one at a time if the engineer hasn't already given them, in this priority order.
Don't ask for everything up front in one wall of questions — take what they've already pasted
or attached, and only ask for what's still missing.

1. **Prospect name** (used for the output folder slug).
2. **Discovery material** — any of: a call transcript/notes, an email, a requirements
   document, a link or pasted excerpt from their website. At least one is required; more is
   better. Accept pasted text, file paths, or uploaded files — whatever's easiest for them.
3. **Target Zoho CRM edition**, if they happen to know it already. If they don't, don't block
   on it here — the design skill will ask for it itself if it turns out to be needed, at the
   point it actually matters (this avoids making the engineer hunt for an answer before they
   even know if it's required).

Do **not** ask the engineer to format anything specially, tag sources, or write requirement
IDs — all of that is the design skill's job, not theirs. Their job is just to hand over what
the prospect said.

## Confirm before handing off

Once you have at least the prospect name and one piece of discovery material, summarize in 2-3
sentences what you're about to pass along ("I've got the call transcript and the requirements
email for Acme Freight — starting the design now.") and proceed. Don't ask for permission to
proceed if they've clearly already handed over material with intent to start — that's an
unnecessary extra round-trip.

## Hand off

Invoke the `crm-data-model-customizer` skill, passing along everything gathered: the prospect
name and all discovery material as given (verbatim — don't summarize or pre-process it
yourself, since source attribution depends on the design skill seeing the original text).

## After handoff

Once the design skill finishes or pauses (e.g. because it needs a blocking question answered,
like the target edition), relay that back to the engineer in plain language — don't make them
go read the agent's internal documents to find out what it needs. If it's just produced a full
design package, tell them where to find it and what's in it in one or two sentences, and offer
to open the key documents (e.g. the data model) rather than assuming they'll go find the files
themselves.
