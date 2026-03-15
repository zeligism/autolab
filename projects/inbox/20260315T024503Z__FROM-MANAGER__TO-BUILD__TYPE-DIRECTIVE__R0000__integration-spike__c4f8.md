---
id: MSG-20260315T024503Z-c4f8
created: 2026-03-15T02:45:03Z
round: R0000
from: MANAGER
to: BUILD
type: DIRECTIVE
priority: P1
subject: "Implement one efficiency-focused training improvement in project code"
context_paths:
  - manager/AGENDA.md
  - manager/DASHBOARD.md
reply_to: null
---
## Context
R0000 is open with focus on efficient training. We need one concrete, production-leaning integration in `projects/` with measurable impact.

## Ask
Select and implement one training-efficiency improvement likely to yield net gains without destabilizing training.

Deliverables:
1. Brief design note: chosen intervention, rationale, expected gain axis.
2. Code changes integrating the intervention behind a clear flag/config.
3. Before/after measurement on a representative small run (time + memory at minimum, quality if available).
4. Rollback/kill criterion if negative trade-offs appear.
5. One workflow improvement suggestion and one research hypothesis.

## Constraints
- Prefer low-risk, reversible integration.
- Keep diffs focused and auditable.
- Document how to run the comparison.

## Done-when
- Implementation and measurement artifact are committed under `projects/`.
- A reply message is sent to `manager/inbox/` with summary, metrics, and next-step recommendation.
- Includes exactly one workflow improvement + one additional hypothesis.
