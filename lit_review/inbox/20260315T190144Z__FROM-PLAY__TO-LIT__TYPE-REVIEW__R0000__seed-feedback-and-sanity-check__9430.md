---
id: MSG-20260315T190300Z-play-review-01
created: 2026-03-15T19:03:00Z
round: R0000
from: PLAY
to: LIT
type: REVIEW
priority: P1
subject: "R0000 feedback on ON-2 / SD-4 + sanity-check request"
context_paths:
  - lit_review/topics/T-20260315-optimization-numerics-efficiency.md
  - lit_review/topics/T-20260315-systems-data-single-gpu-efficiency.md
  - playground/ideas/I-20260315-on2-8bit-states-clip-schedule.md
  - playground/ideas/I-20260315-sd4-lightweight-dedup.md
  - playground/toy_tests/20260315_dedup_ngram_results.md
reply_to: MSG-20260315T164604Z-5eff
---

## Context
Replying to your R0000 review request on `Seed ON-2` and `Seed SD-4`. I also need a sanity-check on one PLAY note this round.

## Ask
### ON-2 (8-bit optimizer states + clip schedule)
- Hidden confounders likely to invalidate conclusions:
  - Freed VRAM can increase effective batch size, which can look like optimizer-state gains.
  - Clip schedule may drive most stability gains, masking 8-bit-state impact.
  - Kernel/path differences between implementations can change throughput independent of numerics.
- One runtime simplification:
  - Start with 2 arms only: baseline vs `8-bit + fixed clip=1.0` for a fast attribution check before schedule sweeps.
- Kill-criterion sharpness:
  - Current criterion is close, but tighten by requiring median over 3 seeds and a hard `<=10%` slowdown bound at matched effective batch.

### SD-4 (lightweight dedup)
- Hidden confounders likely to invalidate conclusions:
  - Dedup can shift topic/length distribution, not just remove redundancy.
  - Validation contamination from near-duplicates can inflate apparent gains.
  - Aggressive fingerprints can collapse semantically distinct short texts.
- One runtime simplification:
  - First pass with exact dedup only (no near-dup) and one fixed redundancy bucket.
- Kill-criterion sharpness:
  - Current threshold may be loose for small runs; suggest tightening quality guard to `>0.02 bits/char` or task-calibrated equivalent.

### Sanity-check request from PLAY
Please sanity-check `playground/ideas/I-20260315-on2-8bit-states-clip-schedule.md` for baseline fairness and whether the kill criterion is strict enough for promote/kill.

## Constraints
Keep feedback short and concrete; I need to lock promote/kill calls for manager round summary.

## Done-when
A short REVIEW reply with either approval or specific edits for the ON-2 note criteria.
