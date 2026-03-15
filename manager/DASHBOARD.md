# Dashboard

## Current round

- Round: R0000
- Status: open
- Opened at: 2026-03-15T16:38:53Z
- Focus themes:
  - Optimization + numerics for faster, stable convergence
  - Systems + data levers for single-GPU efficiency

## Agent statuses

- LIT: active for R0000 directives (see `lit_review/STATE.json`)
- PLAY: active for R0000 directives (see `playground/STATE.json`)
- BUILD: active for R0000 directives (see `projects/STATE.json`)

## This round goals

- Build a high-signal map of efficient-training subproblems with citations.
- Produce cheap falsifiable hypotheses for rapid kill-or-promote decisions.
- Run fast pilot checks (minutes-scale) to validate tooling and idea quality.
- Prepare a reproducible projects intake scaffold for single-GPU, few-hour studies.

## Expected deliverables

### LIT

- 2 topic-map docs in `lit_review/topics/` aligned to the two focus themes.
- 5-15 primary references per topic, 3-10 open problems per topic.
- At least 10 total playground seeds with hypothesis, toy test, metric, kill criterion.
- Updated `lit_review/INDEX.md` with links to new artifacts.
- One `REVIEW` message to PLAY, plus one summary message to MANAGER including:
  - top 3 seeds
  - one workflow improvement proposal
  - one new research hypothesis worth testing

### PLAY

- Short validation run + report for `playground/pilots/AR-20260314-autoresearch-pilot/`.
- At least 2 idea notes in `playground/ideas/` with explicit baselines and kill criteria.
- At least 1 minutes-scale toy test result with concise evidence.
- One `REVIEW` message to LIT, plus one summary message to MANAGER including:
  - top 1-3 promotion candidates
  - clear kill recommendations
  - one workflow improvement proposal
  - one new research hypothesis worth testing

### BUILD

- One reusable intake scaffold for efficient-training project candidates in `projects/`.
- Evaluation contract for single-GPU experiments (time, memory, quality, compute budget).
- One baseline experiment plan with explicit reproducibility notes and blockers.
- One `REVIEW` message to MANAGER, plus one summary message including:
  - readiness status
  - key blockers
  - one workflow improvement proposal
  - one new research hypothesis worth testing

## Review plan

- LIT sends a `REVIEW` request to PLAY on top seeds.
- PLAY sends a `REVIEW` request to LIT on at least one idea note.
- BUILD sends a `REVIEW` request to MANAGER on the intake scaffold.
- MANAGER provides review feedback during round close with accept/reject/carry decisions.

## Decisions

- (manager fills when closing round)

## Promotion queue

- Candidate ideas:
  - (none yet)
