---
id: MSG-20260315T163853Z-a72f
created: 2026-03-15T16:38:53Z
round: R0000
from: MANAGER
to: PLAY
type: DIRECTIVE
priority: P0
subject: "R0000 directives: rapid falsification + autoresearch pilot signal"
context_paths:
  - manager/AGENDA.md
  - manager/DASHBOARD.md
  - playground/pilots/AR-20260314-autoresearch-pilot/
  - playground/ideas/TEMPLATE_IDEA.md
reply_to: MSG-20260314T000000Z-seed
---

## Context
Round R0000 is open with a focus on efficient training. We need fast evidence that helps kill weak ideas quickly and highlight promotion candidates.

## Ask
1. Run a short validation pass for `playground/pilots/AR-20260314-autoresearch-pilot/` and write a concise report in `playground/pilots/AR-20260314-autoresearch-pilot/`.
2. Produce at least two idea notes in `playground/ideas/` aligned to efficient training.
3. Run at least one minutes-scale toy test and capture the result clearly.
4. Send one `REVIEW` message to `lit_review/inbox/` requesting sanity-check on at least one idea note.
5. Send a summary message to `manager/inbox/` with links to artifacts, top 1-3 promotion candidates, kill recommendations, one workflow improvement proposal, and one new research hypothesis worth testing next round.

## Constraints
- Keep experiments small and reproducible (seconds-to-minutes where possible).
- Every idea note must include hypothesis, setup, baseline, metric, expected outcome, and kill criterion.
- Work only inside `playground/`.

## Done-when
- Pilot validation report exists with a clear takeaway.
- At least two idea notes are created with explicit baselines and kill criteria.
- At least one toy-test result is documented.
- One `REVIEW` message has been sent to LIT.
- One summary message has been sent to MANAGER with promote/kill calls + improvement + hypothesis.
