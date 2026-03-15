---
id: MSG-20260315T163853Z-d13a
created: 2026-03-15T16:38:53Z
round: R0000
from: MANAGER
to: LIT
type: DIRECTIVE
priority: P0
subject: "R0000 directives: topic maps + falsifiable seeds for efficient training"
context_paths:
  - manager/AGENDA.md
  - manager/DASHBOARD.md
  - lit_review/INDEX.md
  - lit_review/topics/T-20260314-efficient-training-map.md
reply_to: MSG-20260314T000000Z-seed
---

## Context
Round R0000 is now open. We are prioritizing two themes for efficient training: (1) optimization + numerics for faster stable convergence, and (2) systems + data levers that reduce wall-clock/compute/memory on single-GPU setups.

## Ask
1. Create two topic docs in `lit_review/topics/`:
   - one for optimization + numerics efficiency
   - one for systems + data efficiency
2. In each topic doc include 5-15 primary references, 3-10 open problems, and 3-10 playground seeds.
3. Update `lit_review/INDEX.md` with links to new docs.
4. Send one `REVIEW` message to `playground/inbox/` requesting sanity-check feedback on your top 2 seeds.
5. Send a summary message to `manager/inbox/` with links to artifacts, your top 3 seeds, one workflow improvement proposal, and one new research hypothesis worth testing next round.

## Constraints
- Work only inside `lit_review/`.
- Cite primary sources for non-trivial claims (URL/arXiv/DOI).
- Prefer concise, discoverable docs over one long monolith.

## Done-when
- Two new topic docs exist and are indexed.
- At least 10 total seeds exist across the new docs, each with hypothesis, toy test, metric, and kill criterion.
- One `REVIEW` message has been sent to PLAY.
- One summary message has been sent to MANAGER with top 3 seeds + improvement + hypothesis.
