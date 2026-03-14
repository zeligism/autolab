# Workflow

This document is owned by MANAGER and can evolve.

## Principles

- **Kill ideas cheaply.** Prefer fast falsification over long builds.
- **WIP limits.** Keep the org focused.
- **Make artifacts discoverable.** Index everything.

## Round rhythm (baseline)

Each round should follow:

1) MANAGER opens round:
   - Posts tasks to each agent
   - Defines what “done” means

2) LIT / PLAY / BUILD run in parallel:
   - Do one round worth of work
   - Report back with links
   - Mark done in `STATE.json`

3) MANAGER closes round:
   - Reviews deliverables
   - Records decisions
   - Promotes or kills items
   - Issues next round tasks

## WIP limits (starting values)

- Lit topics actively being expanded: ≤ 5
- Playground ideas active: ≤ 7
- Projects active: ≤ 2

## Review loop requirement (minimal)

Every round:

- LIT requests at least one sanity check from PLAY or MANAGER.
- PLAY requests at least one sanity check from LIT or MANAGER.
- BUILD requests review from MANAGER.

(Review = message with type `REVIEW` + explicit feedback.)

## Promotion pipeline

- Lit → Playground: requires a crisp hypothesis + proposed toy test.
- Playground → Projects: requires toy evidence + clear baseline + plausible 1-GPU-hours experiment.

Rubrics are in `RUBRICS.md`.
