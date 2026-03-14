---
id: MSG-20260314T000000Z-seed
created: 2026-03-14T00:00:00Z
round: R0000
from: USER
to: MANAGER
type: DIRECTIVE
priority: P0
subject: "Initial steering + direction"
context_paths:
  - manager/AGENDA.md
reply_to: null
---

# Initial steering + direction

## Context
We are seeding a 4-agent research org.

## Ask
- Use round-based workflow.
- Keep repo simple, robust, and easy to upgrade later.
- Initial research direction: **more efficient training of deep learning models**.
- Start with a playground pilot based on Karpathy's `autoresearch`.

## Constraints
- Agents must never edit `AGENT.md`.
- Inter-agent comms via inbox message files only.

## Done-when
- Round 0 tasks are issued.
