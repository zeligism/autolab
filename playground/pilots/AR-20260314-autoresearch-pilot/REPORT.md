---
id: AR-20260314-autoresearch-pilot-report
created: 2026-03-14
status: complete
---

# Autoresearch pilot report

## Setup

- Date: 2026-03-15
- Hardware: Apple Silicon (arm64), no NVIDIA GPU detected
- OS: macOS 15.6.1 (Darwin 24.6.0)
- Python: 3.9.6 (system), 3.12.1 (conda)
- Pilot repo: `karpathy/autoresearch` at commit `c2450ad`

## What I ran

- Baseline setup checks:
  - `git clone https://github.com/karpathy/autoresearch`
  - `PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile prepare.py train.py` (pass)
  - `python -m uv sync` (fails on platform wheel compatibility)
- Optional modified run:
  - Not attempted; baseline cannot execute training on this host.

## Results

- Metric(s):
  - Training metric (`val_bpb`) not available because baseline run could not start.
  - Validation signal collected: setup and compatibility pass.
- Runtime:
  - Setup/validation pass: ~5 minutes wall-clock including tool installation attempts.
- Blocking errors:
  - `uv` was initially missing on host.
  - After installing `uv`, dependency resolution failed because `torch==2.9.1+cu128` has no `macosx_15_0_arm64` wheel.
  - `nvidia-smi` unavailable; host does not provide required single-NVIDIA-GPU path.

## Lessons for our org design

- What autoresearch does well:
  - Tight experiment loop and fixed time budget create clean comparability.
  - Keeping almost all mutable logic in one file (`train.py`) makes diffs and rollback simple.
- What we should copy:
  - Mandatory fixed-budget metric for apples-to-apples agent iterations.
  - Explicit "one mutable file" boundary for autonomous edits in early rounds.
- What we should not copy:
  - Hard CUDA lock-in in the default setup. For our org, this should be feature-gated with CPU/MPS smoke mode.
  - Platform-specific dependency pinning in baseline path without compatibility fallback.

## Follow-up ideas

- Idea 1: Add a preflight script (`python`, `gpu`, `package wheel`) that fails fast before starting a round.
- Idea 2: Maintain two tiers for pilot repos:
  - Tier A: full-run hosts (NVIDIA/CUDA)
  - Tier B: logic-validation hosts (syntax/unit/smoke only)
