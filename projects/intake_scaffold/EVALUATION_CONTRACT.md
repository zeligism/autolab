# Evaluation Contract (Single-GPU, Few-Hour)

This contract defines how promoted efficient-training candidates are judged.

## Scope

- Hardware: one GPU.
- Runtime target: few-hour run suitable for fast iteration.
- Comparison unit: candidate vs. baseline under the same data split and seed set.

## Required metrics

1. `time_to_target_min`
- Definition: minutes required to reach the pre-declared quality target.
- Target declaration: must be set before the run (example: validation loss <= X).
- Better direction: lower.

2. `peak_memory_mb`
- Definition: max GPU memory allocated during training.
- Capture: from runtime logs or profiler trace.
- Better direction: lower.

3. `quality_at_budget`
- Definition: quality metric at the fixed compute budget endpoint.
- Examples: validation loss, top-1 accuracy, perplexity.
- Better direction: task-dependent (must be stated in run notes).

4. `compute_budget_gpu_hours`
- Definition: total GPU-hours consumed for each run.
- Constraint: candidate run must stay within the declared budget.
- Better direction: lower, while preserving or improving quality.

## Baseline requirements

- Same dataset split, preprocessing, and evaluation code path.
- Same seed list and reporting windows.
- Same max compute budget and early-stop policy.

## Decision rules

A candidate is **promotion-ready** if all are true:

1. Meets or beats baseline `quality_at_budget`.
2. Improves one efficiency axis (`time_to_target_min` or `peak_memory_mb`) by >= 10%.
3. Does not exceed baseline `compute_budget_gpu_hours`.

## Kill criterion

Kill candidate for this round if either condition is met:

1. At 25% of budget, quality trails baseline by >= 5% relative (or equivalent task metric delta).
2. Projected completion exceeds compute budget without a plausible recovery mechanism.

## Reporting format

Each run report should include:

- hypothesis
- baseline identifier
- candidate identifier
- metric table for all required metrics
- pass/fail against each decision rule
- kill/continue verdict with one-paragraph rationale
