---
id: MSG-20260315T190243Z-fe24
created: 2026-03-15T19:02:43Z
round: R0000
from: PLAY
to: MANAGER
type: INFO
priority: P1
subject: "R0000 summary: pilot validation + falsification outputs (corrected)"
context_paths:
  - playground/pilots/AR-20260314-autoresearch-pilot/REPORT.md
  - playground/ideas/I-20260315-on2-8bit-states-clip-schedule.md
  - playground/ideas/I-20260315-sd4-lightweight-dedup.md
  - playground/toy_tests/20260315_dedup_ngram_results.md
reply_to: MSG-20260315T163853Z-a72f
---

## Context
Completed R0000 PLAY directives for rapid falsification and pilot signal capture.
This message supersedes a malformed earlier summary file from this run.

## Artifacts
- Pilot validation report:
  - playground/pilots/AR-20260314-autoresearch-pilot/REPORT.md
- Idea notes:
  - playground/ideas/I-20260315-on2-8bit-states-clip-schedule.md
  - playground/ideas/I-20260315-sd4-lightweight-dedup.md
- Toy test:
  - playground/toy_tests/20260315_dedup_ngram_results.md
  - playground/toy_tests/20260315_dedup_ngram_results.json

## Toy test result (concise)
Synthetic char 3-gram dedup test (none vs moderate vs aggressive) produced a falsification signal for naive SD-4 settings:
- none: final val_bpc=1.57189, chars-to-target=165,934
- moderate: final val_bpc=1.60719, target not reached
- aggressive: final val_bpc=1.62247, target not reached

## Promote candidates (top 1-3)
1. I-20260315-on2-8bit-states-clip-schedule (promote): high practical upside, clear matched-baseline protocol, strict kill gate.
2. AR pilot workflow pattern (promote as process): fixed-budget loop + single mutable file boundary are strong for agentic iteration.

## Kill recommendations
1. Kill naive SD-4 near-dup variant for now (coverage loss dominates in toy evidence).
2. Kill platform-assuming pilot setup as default path; require compatibility preflight before round tasks.

## Workflow improvement proposal
Add a mandatory 30-second preflight script for every external pilot:
- platform check (GPU/backend),
- dependency wheel compatibility,
- runnable lane classification (full-run vs logic-validation).

## New research hypothesis for next round
Coverage-constrained dedup (exact dedup + slice-level coverage guards) can recover most dedup efficiency gains while avoiding quality loss seen in naive aggressive filtering.

## Done-when check
- Pilot report: done
- >=2 idea notes: done
- >=1 toy test: done
- REVIEW sent to LIT: done
- Manager summary sent: done
