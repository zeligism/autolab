# Dashboard

## Current round

- Round: R0000
- Status: open

## Agent statuses

- LIT: directive sent (awaiting delivery)
- PLAY: directive sent (awaiting delivery)
- BUILD: directive sent (awaiting delivery)

## This round goals

- Identify high-leverage methods for more efficient deep learning training, emphasizing practical methods that improve time/compute/memory/data efficiency.
- Generate rapid empirical evidence from controlled microbenchmarks to rank candidate interventions.
- Integrate at least one low-risk efficiency improvement into project code with before/after measurements.
- Collect one workflow improvement and one new research hypothesis from each non-manager agent.

## Expected deliverables by agent

- **LIT (lit_review):**
  - Taxonomy of efficient-training methods with citations.
  - Top-3 prototype shortlist with hypothesis + kill criterion.
  - Reply message linking artifacts and recommendations.
- **PLAY (playground):**
  - Reproducible benchmark harness + baseline.
  - Results for >=2 interventions with delta table.
  - Recommendation for BUILD integration priority.
  - Reply message linking scripts/results.
- **BUILD (projects):**
  - One configurable efficiency integration in project code.
  - Before/after measurements and rollback criterion.
  - Reply message linking implementation and metrics.

## Review plan (manager)

- Verify each agent provided explicit hypothesis, baseline/metric definition, and kill criterion.
- Check reproducibility: commands, configs, and artifact paths are present.
- Assess evidence quality and promote at most one intervention to “next-round default candidate.”
- Record accept/reject/carry decisions at round close.

## Decisions

- (manager fills when closing round)

## Promotion queue

- Candidate ideas:
  - (pending agent submissions)
