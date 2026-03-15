---
id: T-20260315-optimization-numerics-efficiency
created: 2026-03-15
updated: 2026-03-15
area: efficient-training
status: draft
---

# Optimization + numerics efficiency for faster stable convergence

## Why this matters

Single-GPU work is usually bottlenecked by unstable low-precision runs, optimizer memory cost, and slow time-to-target quality. This topic maps methods that improve convergence speed per unit wall-clock and per unit memory.

## Problem statement

Given a fixed single-GPU budget, how do we reach target validation quality faster without introducing fragility?

## Key ideas / taxonomy

### 1) Precision policy and stability controls

- Mixed precision (fp16/bf16) with dynamic loss scaling
- fp8 forward/backward paths with high-precision master weights
- Gradient clipping and norm controls to prevent overflow/instability

### 2) Optimizer-state efficiency

- 8-bit optimizer state quantization
- Factorized second-moment estimators (Adafactor)
- Low-memory optimizers versus quality regressions

### 3) Convergence-speed levers

- Learning-rate schedules (cosine, warm restarts, warmup length)
- Decoupled regularization (AdamW)
- Sharpness-aware updates (SAM) in selective phases

### 4) Batch-size and trust-ratio scaling

- Large-batch optimization for better hardware utilization
- Trust-ratio methods when effective batch grows

## Key references (primary)

- Micikevicius et al., "Mixed Precision Training" (arXiv:1710.03740) — https://arxiv.org/abs/1710.03740
- Micikevicius et al., "FP8 Formats for Deep Learning" (arXiv:2209.05433) — https://arxiv.org/abs/2209.05433
- Dettmers et al., "8-bit Optimizers via Block-wise Quantization" (arXiv:2110.02861) — https://arxiv.org/abs/2110.02861
- Shazeer and Stern, "Adafactor" (arXiv:1804.04235) — https://arxiv.org/abs/1804.04235
- Loshchilov and Hutter, "Decoupled Weight Decay Regularization" (arXiv:1711.05101) — https://arxiv.org/abs/1711.05101
- You et al., "Large Batch Optimization for Deep Learning: Training BERT in 76 minutes" (arXiv:1904.00962) — https://arxiv.org/abs/1904.00962
- Loshchilov and Hutter, "SGDR: Stochastic Gradient Descent with Warm Restarts" (arXiv:1608.03983) — https://arxiv.org/abs/1608.03983
- Foret et al., "Sharpness-Aware Minimization" (arXiv:2010.01412) — https://arxiv.org/abs/2010.01412
- Chen et al., "Symbolic Discovery of Optimization Algorithms" (arXiv:2302.06675) — https://arxiv.org/abs/2302.06675
- Liu et al., "Sophia: A Scalable Stochastic Second-order Optimizer for Language Model Pre-training" (arXiv:2305.14342) — https://arxiv.org/abs/2305.14342

## Open problems

1. Robust recipes for switching from bf16/fp16 to fp8 mid-training without retuning every model family.
2. Practical optimizer selection under fixed wall-clock: when do low-memory methods actually win time-to-target?
3. How to separate true convergence gains from gains caused only by larger effective batch size.
4. Detecting early instability in low precision before loss spikes become irreversible.
5. Interactions between SAM-style updates and mixed-precision numerical noise.
6. Portable default hyperparameter bundles that transfer across GPU generations.

## Playground seeds (hypotheses + toy tests)

### Seed ON-1: delayed fp8 transition

- Hypothesis: Starting in bf16, then switching selected layers to fp8 after warmup improves throughput with negligible quality loss.
- Baseline: Full-run bf16 training with identical model/data.
- Toy test: Train a 30M-100M parameter transformer for a fixed 45-minute budget; switch to fp8 at 20% steps in treatment.
- Metric: tokens/sec, validation perplexity at budget end, NaN/overflow count.
- Kill criterion: <5% throughput gain or >1.0 perplexity degradation versus baseline.

### Seed ON-2: 8-bit Adam states + clip schedule

- Hypothesis: 8-bit optimizer states plus a simple gradient-clipping schedule preserves convergence while cutting VRAM.
- Baseline: AdamW fp32 states, static clipping.
- Toy test: Same model and seed, compare 8-bit states with clip thresholds {0.5, 1.0}.
- Metric: peak VRAM, time-to-reach target validation loss, divergence rate.
- Kill criterion: >10% slower time-to-target or any repeated divergence across 3 runs.

### Seed ON-3: early-phase SAM only

- Hypothesis: Applying SAM for only the first 15%-25% of steps captures most stability benefit at lower compute overhead.
- Baseline: AdamW without SAM.
- Toy test: Three arms: no SAM, full SAM, early-only SAM on same tokenizer/model.
- Metric: throughput, final validation loss, gradient-norm variance.
- Kill criterion: early-only SAM fails to beat no-SAM on loss while costing >8% throughput.

### Seed ON-4: Adafactor under matched memory

- Hypothesis: Under equal VRAM ceiling, Adafactor with larger batch reaches target quality faster than AdamW with reduced batch.
- Baseline: AdamW configured to fit the same memory ceiling.
- Toy test: Sweep micro-batch sizes under a fixed 12 GB limit for both optimizers.
- Metric: wall-clock to target loss, best achieved loss in 60 minutes.
- Kill criterion: Adafactor never improves wall-clock-to-target in any tested batch regime.

### Seed ON-5: warmup-length sensitivity map

- Hypothesis: A short warmup band (0.5%-2% steps) is sufficient for stable mixed-precision training on small/medium transformers.
- Baseline: Common 5%-10% warmup setting.
- Toy test: Keep all else fixed, sweep warmup fractions across five values.
- Metric: instability events, end-of-budget validation loss, effective throughput.
- Kill criterion: no stable region below 2% warmup or no throughput/quality advantage.
