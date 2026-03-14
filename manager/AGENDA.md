# Research Agenda

## Umbrella direction

**More efficient training of deep learning models**:

- Less wall-clock time
- Less compute (FLOPs)
- Less memory
- Better data efficiency (fewer tokens/examples for same capability)

## Working taxonomy (v0)

Use this taxonomy to organize literature and ideas:

1) **Numerics & precision**
   - mixed precision, low precision, quantized optimizers, stability tricks

2) **Optimization & learning dynamics**
   - faster convergence per step; schedules; optimizers; scaling laws; sharpness

3) **Architecture choices for efficiency**
   - sparsity; MoE; parameter sharing; low-rank structure; conditional compute

4) **Systems & parallelism**
   - activation checkpointing; sharding; memory layout; kernel fusion; comm overlap

5) **Data efficiency**
   - dedup; curricula; filtering; sampling; synthetic data strategies

## Near-term plan (first few rounds)

- **Round 0**: map the space + identify 10–20 cheap falsifiable hypotheses.
- **Round 1–2**: run several toy tests; kill most ideas quickly.
- **Round 3+**: promote 1–2 survivors into a real project scaffold.

## Output expectations

- Lit review should produce **topic maps** and **open problem lists** with citations.
- Playground should produce **1–3 page idea notes** with a toy test or a crisp argument.
- Projects should focus on experiments that can run on **a single GPU in a few hours** (for now).
