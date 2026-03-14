---
id: T-20260314-efficient-training-map
created: 2026-03-14
updated: 2026-03-14
area: efficient-training
status: seed
---

# Efficient training of deep learning models: a working map (seed)

This is an initial **topic map** to steer early rounds.

## What “efficient” can mean

- **Wall-clock**: tokens/sec, steps/sec, time-to-X
- **Compute**: FLOPs, total training compute for target quality
- **Memory**: peak VRAM, activation/optimizer state footprint
- **Data efficiency**: fewer examples/tokens for same quality
- **Energy/cost**: $ and kWh per run (often derived)

## Taxonomy (v0)

### 1) Numerics & precision

- mixed precision (fp16/bf16)
- low precision formats (e.g., fp8)
- quantized optimizer states
- stability methods (loss scaling, clipping, normalization tweaks)

### 2) Optimization & learning dynamics

- optimizers (Adam variants, SGD variants, second-order approximations)
- LR schedules and warmup strategies
- scaling-law-aware training and early stopping
- faster convergence per token

### 3) Architecture and conditional compute

- sparsity (structured/unstructured)
- mixture-of-experts (MoE)
- parameter sharing / tying
- low-rank structure

### 4) Systems

- memory saving: activation checkpointing, sharding, offloading
- speed: fused kernels, efficient attention kernels, compilation
- communication efficiency (multi-GPU) (future)
- dataloader + I/O bottlenecks

### 5) Data efficiency

- deduplication + quality filtering
- curriculum / sampling strategies
- synthetic data and distillation

## Open problems (starter list)

1) **Comparable evaluation**: how to fairly compare training efficiency across architectures and tokenization choices.
2) **Hardware specificity**: improvements that help on one GPU may hurt on another.
3) **Stability at low precision**: robust recipes that are not fragile to model scale.
4) **Measuring “data quality”**: simple predictors that generalize across domains.
5) **Interaction effects**: e.g., optimizer × precision × architecture.

## Playground seeds

### Seed A — efficiency metrics sanity suite

- Hypothesis: Many “efficiency” claims fail under a fixed, transparent metric suite.
- Toy test: build a tiny benchmark harness on a small model (e.g., MLP/CNN/mini-transformer) that reports:
  - peak memory
  - tokens/sec
  - validation loss after fixed wall-clock budget
- Kill criterion: metrics are too noisy to discriminate within minutes.

### Seed B — optimizer-state footprint reduction

- Hypothesis: Reducing optimizer state precision can reduce memory with minimal loss.
- Toy test: train a tiny transformer with optimizer-state quantization vs baseline.
- Metric: validation loss vs peak memory.
- Kill criterion: instability or large degradation.

### Seed C — activation checkpointing trade curve

- Hypothesis: checkpointing yields predictable memory/time tradeoffs that can be exploited by agent search.
- Toy test: a small transformer training loop with/without checkpointing.
- Metric: peak memory vs throughput vs loss.
- Kill criterion: overhead dominates at small scale.
