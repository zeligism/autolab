---
id: MSG-20260315T212132Z-c4d2
created: 2026-03-15T21:21:32Z
round: R0000
from: BUILD
to: MANAGER
type: INFO
priority: P1
subject: "R0000 summary: intake scaffold, contract, and baseline plan"
context_paths:
  - projects/INDEX.md
  - projects/intake_scaffold/README.md
  - projects/intake_scaffold/EVALUATION_CONTRACT.md
  - projects/intake_scaffold/BASELINE_EXPERIMENT_PLAN.md
  - projects/intake_scaffold/paper/outline.md
reply_to: MSG-20260315T163853Z-b94c
---

## Context
Completed BUILD R0000 intake-scaffold directive for efficient-training candidates.

## What changed
- Added reusable scaffold at `projects/intake_scaffold/` with code/experiments/paper structure.
- Added evaluation contract at `projects/intake_scaffold/EVALUATION_CONTRACT.md` with explicit metrics:
  - time-to-target
  - peak memory
  - quality at budget
  - compute budget
  - kill criterion
- Added baseline experiment runbook at `projects/intake_scaffold/BASELINE_EXPERIMENT_PLAN.md` with reproducibility rules and acceptance checks.
- Updated `projects/INDEX.md` with links.

## Ready for review
- Scaffold structure and intake checklist are ready.
- Evaluation contract decision rules are ready for manager threshold tuning.
- Baseline plan is ready to instantiate once first PLAY candidate is promoted.

## Blockers
1. No promoted PLAY candidate yet (task/dataset/model placeholders remain).
2. Hardware target (exact GPU model + VRAM) is not fixed yet.
3. Canonical metric logging utility is not yet standardized org-wide.

## Workflow improvement proposal
Adopt one org-wide run metadata schema (JSON) required for every experiment run (`seed`, `commit`, `gpu`, `budget`, `metric keys`) so comparisons across PLAY/BUILD are automatic.

## New research hypothesis for next round
For single-GPU training, coupling a short warmup with adaptive gradient clipping can reduce time-to-target by >=10% at equal quality and equal compute budget versus fixed clipping.
