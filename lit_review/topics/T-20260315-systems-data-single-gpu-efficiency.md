---
id: T-20260315-systems-data-single-gpu-efficiency
created: 2026-03-15
updated: 2026-03-15
area: efficient-training
status: draft
---

# Systems + data levers for single-GPU training efficiency

## Why this matters

On a single GPU, memory pressure and input-data quality both dominate practical progress. The best results usually come from jointly tuning systems throughput and data efficiency, not from either in isolation.

## Problem statement

Given one commodity GPU and a few-hour budget, what system/data decisions maximize quality gained per wall-clock and per FLOP?

## Key ideas / taxonomy

### 1) Memory-saving systems knobs

- Activation checkpointing granularity
- Optimizer/parameter offload to CPU/NVMe
- Paged optimizers and unified-memory aware strategies

### 2) Throughput kernels and execution

- FlashAttention-family kernels for attention bottlenecks
- Graph capture and compiler paths (`torch.compile`)
- DataLoader overlap and sequence packing to reduce stalls

### 3) Data efficiency levers

- Deduplication to reduce redundant tokens
- Mixture reweighting/curriculum for faster learning
- Compute-optimal token budgeting and model/data ratio planning

### 4) Joint system-data effects

- Better data can lower required steps, changing best systems configuration
- Systems speedups can alter optimal sampling and curriculum schedules

## Key references (primary)

- Chen et al., "Training Deep Nets with Sublinear Memory Cost" (arXiv:1604.06174) — https://arxiv.org/abs/1604.06174
- Rajbhandari et al., "ZeRO-Offload: Democratizing Billion-Scale Model Training" (arXiv:2101.06840) — https://arxiv.org/abs/2101.06840
- Ren et al., "ZeRO-Infinity: Breaking the GPU Memory Wall" (arXiv:2104.07857) — https://arxiv.org/abs/2104.07857
- Dao et al., "FlashAttention: Fast and Memory-Efficient Exact Attention" (arXiv:2205.14135) — https://arxiv.org/abs/2205.14135
- Dao, "FlashAttention-2: Faster Attention with Better Parallelism" (arXiv:2307.08691) — https://arxiv.org/abs/2307.08691
- Dettmers et al., "QLoRA: Efficient Finetuning of Quantized LLMs" (arXiv:2305.14314) — https://arxiv.org/abs/2305.14314
- Lee et al., "Deduplicating Training Data Makes Language Models Better" (arXiv:2107.06499) — https://arxiv.org/abs/2107.06499
- Hoffmann et al., "Training Compute-Optimal Large Language Models" (arXiv:2203.15556) — https://arxiv.org/abs/2203.15556
- Xie et al., "DoReMi: Data Mixture Reweighting for Efficient LLM Pretraining" (arXiv:2305.10429) — https://arxiv.org/abs/2305.10429
- Eldan and Li, "TinyStories: How Small Can Language Models Be and Still Speak Coherent English?" (arXiv:2305.07759) — https://arxiv.org/abs/2305.07759

## Open problems

1. Reproducible single-GPU benchmarks for memory/time tradeoffs across checkpointing/offload/kernels.
2. Break-even rules for CPU/NVMe offload under different PCIe and storage speeds.
3. How much deduplication is beneficial before useful long-tail signal is removed.
4. Practical recipe for combining data-mixture reweighting with strict wall-clock budgets.
5. Whether compute-optimal scaling guidance transfers cleanly to <1B parameter regimes.
6. Choosing sequence packing strategies that improve throughput without harming optimization dynamics.

## Playground seeds (hypotheses + toy tests)

### Seed SD-1: selective checkpointing by depth

- Hypothesis: Checkpointing only upper transformer blocks captures most memory savings at materially lower overhead than full checkpointing.
- Baseline: No checkpointing.
- Toy test: Three arms (none, top-half only, full) on identical model and batch size.
- Metric: peak VRAM, tokens/sec, validation loss after fixed wall-clock.
- Kill criterion: top-half checkpointing saves <20% VRAM or slows throughput >12% with no loss benefit.

### Seed SD-2: flash-attention break-even curve

- Hypothesis: FlashAttention-2 wins strongly at medium/long sequence lengths but offers limited gain at short context.
- Baseline: PyTorch native scaled-dot-product attention path.
- Toy test: Sweep sequence lengths {128, 256, 512, 1024} with fixed model width/depth.
- Metric: tokens/sec, peak memory, and end-of-budget validation loss.
- Kill criterion: no throughput gain at sequence length >=512 or numerical instability appears.

### Seed SD-3: offload vs smaller-batch baseline

- Hypothesis: Optimizer-state CPU offload can beat a smaller all-GPU baseline in time-to-target quality under the same GPU memory cap.
- Baseline: All-GPU training with reduced micro-batch to fit memory.
- Toy test: Compare offload-enabled run against reduced-batch baseline for 60 minutes.
- Metric: wall-clock to target validation loss, throughput, host RAM usage.
- Kill criterion: offload run is >25% slower to target or host-memory pressure causes repeated stalls.

### Seed SD-4: lightweight dedup for faster convergence

- Hypothesis: MinHash-style near-duplicate filtering reduces required tokens to hit a target loss on small corpora.
- Baseline: Same corpus without deduplication.
- Toy test: Build 2-3 dedup levels (none, moderate, aggressive) and train identical small models.
- Metric: tokens consumed to reach target loss, final perplexity at fixed token budget.
- Kill criterion: dedup saves <2% tokens-to-target or harms final perplexity by >1.0.

### Seed SD-5: compute-optimal token budget at tiny scale

- Hypothesis: Chinchilla-style token/parameter balancing improves quality under fixed FLOP budgets even for 50M-300M models.
- Baseline: Conventional fixed-token budget independent of model size.
- Toy test: Train multiple model sizes with matched FLOPs and varying token budgets.
- Metric: best validation perplexity at fixed FLOPs, training-time efficiency.
- Kill criterion: balanced budget does not outperform baseline for at least two model sizes.
