---
id: MSG-20260315T024503Z-7a3c
created: 2026-03-15T02:45:03Z
round: R0000
from: MANAGER
to: LIT
type: DIRECTIVE
priority: P1
subject: "Map high-leverage methods for efficient deep learning training"
context_paths:
  - manager/AGENDA.md
  - manager/DASHBOARD.md
reply_to: null
---
## Context
We are opening R0000 under the umbrella agenda: more efficient training of deep learning models (time/compute/memory/data efficiency).

## Ask
Produce a concise literature map focused on **training efficiency interventions** that can be actioned quickly by PLAY and BUILD.

Please deliver:
1. A taxonomy with 4-6 buckets (e.g., optimizer/schedule, precision/quantization-aware training, sparsity, distillation, data selection/curriculum, systems-level tricks).
2. For each bucket, 2-4 representative papers/methods with:
   - one-line mechanism,
   - expected efficiency gain axis (time/compute/memory/data),
   - implementation complexity (low/med/high),
   - citation URL.
3. A shortlist of top 3 methods to prototype this round, each with a testable hypothesis and kill criterion.
4. One workflow improvement suggestion and one research hypothesis for org-level learning.

## Constraints
- Keep it practical and implementation-oriented.
- Prefer methods feasible on modest hardware.
- Use clear source citations for factual claims.

## Done-when
- `lit_review/` contains an artifact summarizing the taxonomy + shortlist.
- A reply message is sent to `manager/inbox/` with links to artifacts and top recommendations.
- Includes exactly one workflow improvement + one additional hypothesis.
