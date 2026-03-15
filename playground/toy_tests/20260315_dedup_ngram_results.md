---
id: TT-20260315-dedup-ngram
created: 2026-03-15
status: complete
area: efficient-training
---

# Toy test: lightweight dedup vs no dedup (synthetic char n-gram)

## Hypothesis

Moderate dedup can reduce tokens-to-target without hurting validation quality.

## Setup

- Script: `playground/toy_tests/20260315_dedup_ngram_toy.py`
- Dataset: synthetic text corpus with heavy duplicate skew
- Model: char 3-gram LM (`alpha=0.5`)
- Arms:
  - `none` (no dedup)
  - `moderate` (exact normalized dedup)
  - `aggressive` (exact + near-duplicate fingerprint)
- Metrics:
  - final validation bits/char (`val_bpc`, lower is better)
  - chars to reach target `val_bpc` (target set to best final + 0.02)

## Result

| Arm | Train chars | Final val_bpc | Chars-to-target |
|---|---:|---:|---:|
| none | 237,096 | 1.57189 | 165,934 |
| moderate | 76,660 | 1.60719 | not reached |
| aggressive | 65,528 | 1.62247 | not reached |

- Runtime: `1.119s`
- Raw JSON: `playground/toy_tests/20260315_dedup_ngram_results.json`

## Takeaway

This toy setting falsifies the naive SD-4 variant: both dedup treatments removed enough coverage that quality dropped and target quality was not reached.

## Reproduce

```bash
python3 playground/toy_tests/20260315_dedup_ngram_toy.py
```
