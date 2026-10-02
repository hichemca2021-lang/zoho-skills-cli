# Session Persistence and Resume (FR-012)

## Write-after-every-answer rule

After recording any Captured Answer (SKILL.md "one-question-per-turn loop" step 5), write the
updated `output/<prospect-slug>/session-state.yaml` immediately — do not batch writes until the
end of a session. A session can end at any point (the customer closes the chat, loses
connectivity, or simply stops responding), and the next session must be able to resume from
exactly that point.

## Resuming a new session

1. Load `output/<prospect-slug>/session-state.yaml`. If it doesn't exist, this is a brand-new
   engagement — initialize from `templates/session-state.yaml`.
2. Do not greet the customer with a question that repeats anything already `answered` or
   `deferred` in `question_tree_state`. Briefly acknowledge what's already been covered if it
   helps orient the customer, but never re-ask it.
3. Resume at the next eligible question exactly as determined by SKILL.md "one-question-per-turn
   loop" step 2 (dependency-eligible, status `unasked`).
4. If the stop condition (SKILL.md "Stop condition") was already satisfied in a prior session,
   do not resume asking questions — go straight to "Finalizing the brief," unless the customer
   explicitly asks to revisit or add something.

## Contradiction handling (Edge Cases)

If a new answer to a question that already has an `answered` Captured Answer contradicts the
existing value (e.g., the customer now describes winning deals differently than they did in an
earlier session):

1. Do **not** overwrite or delete the earlier Captured Answer.
2. Append the new answer to the question's `answers` list with its own origin tag and
   `source_exchange_ref`.
3. Set the earlier answer's `superseded_by` field to the new answer's `source_exchange_ref`.
4. When rendering `customer-brief.md`, use the most recent (non-superseded) answer as the
   current value in the relevant coverage section, but surface the conflict explicitly — e.g.,
   a one-line note under that bullet: "Note: an earlier session described this differently (see
   session state); customer's most recent statement is used here." Never silently present only
   the latest answer as if no conflict existed.

## Source precedence (Edge Cases)

If an `[WEB]`/`[DOC]` ingested-source finding is later contradicted by something the customer
says directly, the customer's direct statement always takes precedence. Do not delete the stale
source finding — mark it superseded in the same way as a contradicted Captured Answer, so the
divergence between public/provided material and the customer's actual statement remains visible
for whoever reviews the brief.
