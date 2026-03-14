# Short run instructions

We keep external repos out of git history.

## 0) Clone autoresearch

From repo root:

```bash
mkdir -p playground/pilots/AR-20260314-autoresearch-pilot/external
cd playground/pilots/AR-20260314-autoresearch-pilot/external

git clone https://github.com/karpathy/autoresearch
cd autoresearch
```

(Directory `external/` is git-ignored by default.)

## 1) Follow the repo quickstart (baseline)

Autoresearch uses `uv` for env management.

Typical baseline commands:

```bash
uv sync
uv run prepare.py
uv run train.py
```

A single `train.py` run is designed to take ~5 minutes wall clock.

## 2) Time-boxing

For this pilot, do ONE of the following:

- **Option A (simplest):** run `uv run train.py` once, record metric.
- **Option B (still short):** run baseline once, then let an agent propose ONE change to `train.py`, and run once more.

Stop after ~2 experiments.

## 3) Record results

Fill in `REPORT.md`:
- hardware
- time per run
- metric reported by autoresearch
- what changed (if you did Option B)
