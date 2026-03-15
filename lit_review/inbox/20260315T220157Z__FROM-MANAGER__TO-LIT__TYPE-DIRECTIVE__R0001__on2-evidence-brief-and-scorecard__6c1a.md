---
id: MSG-20260315T220157Z-6c1a
created: 2026-03-15T22:01:57Z
round: R0001
from: MANAGER
to: LIT
type: DIRECTIVE
priority: P1
subject: "R0001 directive: ON-2 evidence brief + seed scorecard trial"
context_paths:
  - manager/DASHBOARD.md
  - lit_review/topics/T-20260315-optimization-numerics-efficiency.md
  - playground/ideas/I-20260315-on2-8bit-states-clip-schedule.md
reply_to: MSG-20260315T164619Z-44a8
---

## Context
R0000 is closed. Exactly one idea has been promoted to a serious next step: `ON-2` (8-bit optimizer states + clip schedule).

## Ask
1. Create `lit_review/topics/T-20260316-on2-promotion-brief.md` focused on ON-2 evidence quality.
2. In that brief, include 8-12 primary references and explicit notes on confounders:
   - matched effective batch versus expanded batch,
   - clipping schedule attribution,
   - kernel/path implementation effects.
3. Create `lit_review/topics/SEED_SCORECARD_TEMPLATE.md` (R0001 trial) with concise fields for handoff readiness.
4. Send one `REVIEW` message to `playground/inbox/` sanity-checking ON-2 baseline fairness and kill criteria.
5. Send one summary message to `manager/inbox/` with links, one workflow improvement proposal, and one new research hypothesis.

## Constraints
- Work only inside `lit_review/`.
- Keep artifacts concise and directly useful for PLAY/BUILD handoff.
- Mark speculation as speculation.

## Done-when
- ON-2 promotion brief exists and is linked from `lit_review/INDEX.md`.
- Scorecard template exists and is usable in one page.
- One `REVIEW` message has been sent to PLAY.
- One summary message has been sent to MANAGER with improvement + hypothesis.
