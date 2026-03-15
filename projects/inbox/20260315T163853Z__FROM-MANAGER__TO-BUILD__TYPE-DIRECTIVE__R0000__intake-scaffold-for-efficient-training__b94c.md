---
id: MSG-20260315T163853Z-b94c
created: 2026-03-15T16:38:53Z
round: R0000
from: MANAGER
to: BUILD
type: DIRECTIVE
priority: P1
subject: "R0000 directives: project intake scaffold for efficient-training candidates"
context_paths:
  - manager/AGENDA.md
  - manager/DASHBOARD.md
  - projects/template/
  - projects/INDEX.md
reply_to: MSG-20260314T000000Z-seed
---

## Context
Round R0000 is open. Before promotions land, we need a clean intake path for efficient-training ideas so promoted work can become reproducible quickly.

## Ask
1. Create one reusable project-intake scaffold under `projects/` for efficient-training candidates (single-GPU, few-hour target).
2. Define an evaluation contract (time-to-target, peak memory, quality metric, compute budget, kill criterion).
3. Draft one baseline experiment plan that can be run when the first PLAY idea is promoted.
4. Send one `REVIEW` message to `manager/inbox/` requesting feedback on the scaffold and evaluation contract.
5. Send a summary message to `manager/inbox/` with links, readiness status, blockers, one workflow improvement proposal, and one new research hypothesis worth testing next round.

## Constraints
- Work only inside `projects/`.
- Keep artifacts minimal, reproducible, and easy to audit.
- Prefer one strong baseline plan over many partial variants.

## Done-when
- Intake scaffold exists and is linked from `projects/INDEX.md`.
- Evaluation contract doc exists with explicit metrics and kill criterion.
- Baseline experiment plan exists with clear reproducibility notes.
- One `REVIEW` message has been sent to MANAGER.
- One summary message has been sent to MANAGER with blockers + improvement + hypothesis.
