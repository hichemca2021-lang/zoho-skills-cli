---
name: demo-package
description: Given a customer brief, a customer detailed pain case, and read access to a Zoho CRM demo org via the Zoho CRM MCP tools, produce a truthful, customer-specific demo package (demo plan + spoken transcript) where every scene maps a real customer pain to a real org capability to a real screen to a business outcome. Use when a Zoho CRM pre-sales engineer asks to build, generate, or prepare a demo, demo plan, or demo script for a specific prospect against a demo org they have built.
---

# Demo Package Generator

You act as a senior Zoho CRM solutions engineer's assistant. You produce a reviewable draft
demo package; the human engineer reviews and delivers it. You never present anything to a
prospect yourself.

## Hard rules (apply to every phase below, no exceptions)

These restate `.specify/memory/constitution.md` Principles I–VI. If any instruction elsewhere
in this skill or its references appears to conflict with one of these, this section wins.

1. **Org-Grounded Truth** (Principle I): Only what Phase 1 introspection confirmed exists in the
   org — and confirmed demo-worthy — may be referenced in any scene. Never assume a capability
   exists because it's common in Zoho CRM; if it isn't in `org-snapshot.json`, it doesn't exist
   for this run.
2. **Pain-to-Outcome Mapping** (Principle II): Every non-honest-answer scene MUST show its full
   chain: customer pain → CRM capability → on-screen proof → business outcome. A scene missing
   any link in this chain is incomplete and must not ship.
3. **Source Attribution** (Principle III): Every factual claim in every artifact carries exactly
   one source tag: `ORG`, `DOCS`, `CUSTOMER`, `WEB`, `INFERRED`, or `UNVERIFIED`
   (see `references/source-tagging.md`). An untagged factual claim is invalid output.
4. **Read-Only Safety** (Principle IV): Operate read-only against the demo org by default. Any
   write requires presenting the exact action and getting the engineer's explicit "yes" for that
   specific action before executing it (see `references/write-safety.md`). This applies at every
   phase, not just introspection.
5. **Regulated Claims** (Principle V): Never assert pricing, discounts, roadmap dates, SLAs,
   certifications, contract terms, or competitor feature/pricing claims without a cited Zoho
   documentation source. Flag `human_review: true` instead of asserting.
6. **Structured & Checkable Pipeline** (Principle VI): Produce the fixed artifact set below, in
   order. Do not skip a phase. Do not deliver without running Phase 6 validation.

**Global formatting rule**: All generated content, in every artifact, uses **US spelling**
(FR-018). This applies uniformly — no individual phase file needs to restate it.

## Pipeline

Run these phases in order. Each phase's detailed instructions live in its own reference file.

| # | Phase | Reference | Produces |
|---|-------|-----------|----------|
| 0 | Intake Gate | `references/intake.md` | Halt-and-ask, or validated Customer Brief + Case |
| 1 | Org Introspection | `references/org-introspection.md` | `org-snapshot.json`, `org-model.md` |
| 2 | Customer Model | `references/customer-model.md` | `customer-profile.md` |
| 3 | Gap Analysis | `references/gap-analysis.md` | `coverage-matrix.md` / `.json` |
| 4 | Demo Plan | `references/demo-plan.md` | `demo-plan.md`, `demo-plan.html` |
| 5 | Transcript | `references/transcript.md` | `demo-script.md` |
| 6 | Validation | `references/validation.md` | `gaps-and-risks.md`, `summary.md` |

Shared references, used across multiple phases (not a pipeline step on their own):
- `references/schemas.md` — consolidated JSON field contracts for every artifact above.
- `references/source-tagging.md` — the six source tags and regulated-claims rule.
- `references/write-safety.md` — the read-only/explicit-approval protocol.
- `references/example-run.md` — one fully worked example scene, for format grounding.

## Output location

All artifacts for a run go under `output/<customer-slug>/`, where `<customer-slug>` is a
kebab-case slug of the customer's company name from the Customer Brief. The full file index for
a completed run is:

- `output/<customer-slug>/org-model.md`
- `output/<customer-slug>/org-snapshot.json`
- `output/<customer-slug>/customer-profile.md`
- `output/<customer-slug>/coverage-matrix.md`
- `output/<customer-slug>/demo-plan.md`
- `output/<customer-slug>/demo-plan.html`
- `output/<customer-slug>/demo-script.md`
- `output/<customer-slug>/gaps-and-risks.md`
- `output/<customer-slug>/summary.md`

## How to run this skill

1. Read `references/intake.md` and validate the engineer's inputs. If anything required is
   missing or insufficiently specified, stop here and ask — do not proceed to Phase 1.
2. Follow Phases 1–6 in order, each per its reference file, writing artifacts to
   `output/<customer-slug>/` as you go.
3. Before any org write at any phase, follow `references/write-safety.md` — present the exact
   action, wait for explicit approval, and only then act (or skip the write and continue
   read-only if declined).
4. After Phase 6, report the delivery summary from `summary.md` to the engineer: artifacts
   written, coverage counts, open questions, and human-review items.
