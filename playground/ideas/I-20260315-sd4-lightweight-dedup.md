---
id: I-20260315-sd4-lightweight-dedup
created: 2026-03-15
status: draft
area: efficient-training
---

# Seed SD-4: lightweight dedup for faster convergence

## Hypothesis

Coverage-preserving dedup (exact + conservative near-duplicate filtering) can reduce tokens-to-target by removing redundancy without materially harming final perplexity.

Reference:
- Lee et al., "Deduplicating Training Data Makes Language Models Better" (https://arxiv.org/abs/2107.06499)

## Minimal toy test

- Setup:
  - Start with a duplicate-heavy text corpus.
  - Compare three arms: none, moderate dedup, aggressive dedup.
  - Evaluate with a simple char 3-gram model.
- Baseline:
  - No dedup.
- Metric:
  - Final validation bits/char (lower is better).
  - Chars consumed to reach a common target quality.
- Expected outcome:
  - Moderate dedup reaches target with fewer chars.
  - Aggressive dedup may fail due coverage loss.

## Kill criterion

Kill if both conditions hold:
- dedup saves <2% chars-to-target, and
- final quality worsens by >0.02 bits/char relative to baseline.

## Notes / risks

- Current toy evidence is negative for naive dedup:
  - `playground/toy_tests/20260315_dedup_ngram_results.md`
  - Moderate/aggressive variants both underperformed no-dedup.
- Main confounder: too-aggressive fingerprints collapse semantically distinct examples.
- This seed should only survive if the next iteration enforces coverage guards (topic/length mix preservation).

## Next step if it works

Promote to `projects/` with a guarded dedup pipeline that reports redundancy removed by slice and checks coverage drift before training.
