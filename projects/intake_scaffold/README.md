# Efficient-Training Project Intake Scaffold

Use this scaffold when a PLAY idea is promoted into a full BUILD project.

## Goals

- Keep first-pass experiments reproducible on one GPU.
- Make kill/continue decisions quickly (few-hour budget).
- Produce artifacts that can roll directly into paper drafting.

## Directory layout

- `code/` — method and utility code for the promoted candidate.
- `experiments/` — runnable scripts/configs for baseline + candidate runs.
- `paper/` — manuscript outline and experiment narrative.
- [`EVALUATION_CONTRACT.md`](EVALUATION_CONTRACT.md) — fixed metrics and pass/fail rules.
- [`BASELINE_EXPERIMENT_PLAN.md`](BASELINE_EXPERIMENT_PLAN.md) — first baseline runbook.

## Intake checklist

1. Define task and dataset split in `experiments/README.md`.
2. Pin environment (Python version, package versions, CUDA).
3. Implement baseline run command and candidate run command.
4. Record metrics required by the evaluation contract.
5. Apply kill criterion by 25% of the compute budget.
6. Write a short outcome note in `paper/` and message MANAGER.

## Reproducibility minimum

- Single command per run (baseline and candidate).
- Fixed seed list (at least 3 seeds for acceptance decisions).
- Logged: wall-clock time, peak memory, quality metric, and compute usage.
- Explicit hardware note (GPU model + VRAM).
