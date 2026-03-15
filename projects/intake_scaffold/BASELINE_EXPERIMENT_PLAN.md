# Baseline Experiment Plan (For First Promoted PLAY Idea)

## Objective

Establish a strong, auditable baseline before testing the promoted candidate method.

## Hypothesis

A clean baseline run under fixed budget and seeds will provide stable reference numbers for time, memory, and quality, enabling an unambiguous candidate comparison.

## Experimental setup template

- Task: `<to fill at promotion>`
- Dataset: `<to fill at promotion>`
- Model family: `<to fill at promotion>`
- Baseline method: standard training recipe from upstream reference implementation.
- Budget cap: 3 GPU-hours total for baseline sweep.
- Seeds: `[11, 22, 33]`

## Planned procedure

1. Environment lock
- Record Python, CUDA, framework, and dependency versions.
- Save full dependency list to `experiments/env.lock`.

2. Data + split lock
- Define immutable train/validation split artifact.
- Store split hash and preprocessing settings in `experiments/data_spec.md`.

3. Baseline run
- Execute baseline command once per seed.
- Log per-step wall-clock, memory, and quality metric.

4. Aggregate report
- Produce mean and std across seeds for all contract metrics.
- Save summary table to `experiments/baseline_results.md`.

## Reproducibility notes

- All runs must be executable from repo root with explicit CLI arguments.
- No hidden defaults: config values are written to disk per run.
- Each run stores commit hash, seed, and timestamp in output metadata.

## Acceptance criteria for baseline readiness

- Three successful seed runs completed within budget.
- Metrics required by `EVALUATION_CONTRACT.md` are all present.
- Variance is small enough to compare candidate deltas (manager review if uncertain).

## Known blockers (current)

1. No promoted PLAY candidate is attached yet, so task/dataset/model fields are placeholders.
2. Hardware target (exact GPU model) has not been fixed in a manager decision.
3. Canonical logging utility for standardized metric output is not yet selected.
