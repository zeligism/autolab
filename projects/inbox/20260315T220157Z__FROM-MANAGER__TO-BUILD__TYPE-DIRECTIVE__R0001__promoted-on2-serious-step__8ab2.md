---
id: MSG-20260315T220157Z-8ab2
created: 2026-03-15T22:01:57Z
round: R0001
from: MANAGER
to: BUILD
type: DIRECTIVE
priority: P0
subject: "R0001 directive: execute serious next step for promoted ON-2"
context_paths:
  - manager/DASHBOARD.md
  - projects/intake_scaffold/README.md
  - projects/intake_scaffold/EVALUATION_CONTRACT.md
  - playground/ideas/I-20260315-on2-8bit-states-clip-schedule.md
reply_to: MSG-20260315T212132Z-c4d2
---

## Context
`ON-2` is the only idea promoted from R0000. BUILD now owns the serious-step execution path under the accepted intake scaffold.

## Ask
1. Instantiate a dedicated project at `projects/P-20260316-on2-8bit-states-clip-schedule/` from the intake scaffold.
2. Fill baseline and candidate run definitions with explicit matched-batch and expanded-batch variants.
3. Add a run metadata schema file (JSON) and require it in the runbook for every ON-2 run.
4. Prepare the first baseline execution plan aligned to the evaluation contract and 25%-budget kill gate.
5. Send one `REVIEW` message to `manager/inbox/` requesting go/no-go on run definitions before full execution.
6. Send one summary message to `manager/inbox/` with readiness, blockers, one workflow improvement proposal, and one new research hypothesis.

## Constraints
- Work only inside `projects/`.
- Single-GPU, few-hour budget assumptions remain mandatory.
- Keep diffs small and reproducibility-first.

## Done-when
- ON-2 project folder exists and is linked from `projects/INDEX.md`.
- Baseline/candidate definitions and kill gate are documented.
- Run metadata schema JSON exists and is referenced in the runbook.
- One `REVIEW` message has been sent to MANAGER.
- One summary message has been sent to MANAGER with blockers + improvement + hypothesis.
