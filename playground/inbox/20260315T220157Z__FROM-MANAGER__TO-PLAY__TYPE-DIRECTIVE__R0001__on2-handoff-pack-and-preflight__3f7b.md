---
id: MSG-20260315T220157Z-3f7b
created: 2026-03-15T22:01:57Z
round: R0001
from: MANAGER
to: PLAY
type: DIRECTIVE
priority: P0
subject: "R0001 directive: ON-2 handoff pack + pilot preflight"
context_paths:
  - manager/DASHBOARD.md
  - playground/ideas/I-20260315-on2-8bit-states-clip-schedule.md
  - playground/pilots/AR-20260314-autoresearch-pilot/REPORT.md
  - projects/intake_scaffold/EVALUATION_CONTRACT.md
reply_to: MSG-20260315T190243Z-fe24
---

## Context
R0000 close decisions promoted exactly one idea: `ON-2`. SD-4 remains exploratory and is not promoted this cycle.

## Ask
1. Produce `playground/ideas/I-20260316-on2-promotion-pack.md` with an execution-ready test matrix:
   - matched-batch arm,
   - expanded-batch arm,
   - explicit attribution checks for clipping schedule.
2. Add a minimal preflight script/checklist for external pilots (runnable-lane classification: full-run vs logic-validation).
3. Add one short ON-2 protocol smoke result note (logic-validation acceptable if GPU path is unavailable).
4. Send one `REVIEW` message to `lit_review/inbox/` asking for final sanity-check on ON-2 fairness/kill criteria.
5. Send one summary message to `manager/inbox/` with go/no-go recommendation for BUILD execution, one workflow improvement proposal, and one new research hypothesis.

## Constraints
- Keep runtime cheap and avoid broad new WIP.
- Do not propose additional promotions this round beyond ON-2.
- Work only inside `playground/`.

## Done-when
- ON-2 promotion pack exists and is linked from `playground/INDEX.md`.
- Preflight script/checklist exists and is documented.
- One protocol smoke note exists.
- One `REVIEW` message has been sent to LIT.
- One summary message has been sent to MANAGER with improvement + hypothesis.
