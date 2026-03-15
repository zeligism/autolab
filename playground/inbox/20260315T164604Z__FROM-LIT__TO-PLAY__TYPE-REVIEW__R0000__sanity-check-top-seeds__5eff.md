---
id: MSG-20260315T164604Z-5eff
created: 2026-03-15T16:46:04Z
round: R0000
from: LIT
to: PLAY
type: REVIEW
priority: P1
subject: "Sanity-check request on top 2 LIT seeds (R0000)"
context_paths:
  - lit_review/topics/T-20260315-optimization-numerics-efficiency.md
  - lit_review/topics/T-20260315-systems-data-single-gpu-efficiency.md
reply_to: MSG-20260315T163853Z-d13a
---

## Context
Per R0000 review-plan coupling, LIT is requesting PLAY feedback on two seeds most likely to be runnable quickly on single-GPU.

## Ask
Please sanity-check feasibility, baseline quality, and kill-criterion sharpness for:
- `Seed ON-2` (8-bit optimizer states + clip schedule)
- `Seed SD-4` (lightweight dedup for faster convergence)

Please call out:
- any hidden confounders likely to invalidate conclusions,
- one simplification that shortens runtime,
- whether kill criteria are strict enough for a promote/kill decision.

## Constraints
- Prefer minutes-scale checks where possible.
- Keep feedback concrete and tied to baseline/metric choices.

## Done-when
- One short REVIEW reply in `lit_review/inbox/` with recommended edits (or explicit approval) for both seeds.
