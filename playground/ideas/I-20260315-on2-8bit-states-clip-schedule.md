---
id: I-20260315-on2-8bit-states-clip-schedule
created: 2026-03-15
status: draft
area: efficient-training
---

# Seed ON-2: 8-bit optimizer states + clip schedule

## Hypothesis

Quantizing Adam states to 8-bit while using a staged clipping schedule reduces VRAM materially without harming time-to-target convergence on small single-GPU language-model training.

Reference:
- Dettmers et al., "8-bit Optimizers via Block-wise Quantization" (https://arxiv.org/abs/2110.02861)

## Minimal toy test

- Setup:
  - Small transformer (50M-100M params), single GPU, fixed 45-minute wall-clock budget.
  - Three seeds per arm for variance control.
  - Treatment:
    - 8-bit optimizer states.
    - Clip schedule: `1.0` (warmup) -> `0.7` (mid) -> `0.5` (late).
- Baseline:
  - AdamW with fp32 optimizer states and static clip `1.0`.
- Metric:
  - Peak VRAM.
  - Time to reach a fixed validation-loss threshold.
  - Divergence count (NaN/overflow or loss explosion).
- Expected outcome:
  - >=20% lower peak VRAM.
  - <=5% regression in time-to-threshold.
  - No increase in divergence events.

## Kill criterion

Kill if any of the following happen:
- time-to-threshold is >10% slower vs baseline (median over seeds),
- divergence appears in >=2 of 3 treatment runs,
- VRAM savings are <15%.

## Notes / risks

- Hidden confounder: larger effective batch enabled by freed memory can fake optimizer gains.
- Mitigation: run matched-effective-batch and expanded-batch variants separately.
- Hidden confounder: gradient clipping schedule may dominate the effect, not 8-bit states.

## Next step if it works

Promote into `projects/` as a reusable low-memory optimizer recipe with a standard clipping protocol.
