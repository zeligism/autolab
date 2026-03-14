# Constitution

This document defines the **global invariants** for the agentic research org.

## Non-negotiables

1. **Do not edit any `AGENT.md` file.**
   - Only the human user edits `AGENT.md`.
2. **Cross-agent writes are restricted.**
   - You may only communicate with other agents by **creating a new message file** in their `inbox/` directory.
   - Do **not** modify or delete existing message files, even in someone else’s inbox.
   - Do **not** modify other agents’ `STATE.json`.
3. **Stay in-bounds.**
   - `LIT` writes inside `lit_review/` and sends messages.
   - `PLAY` writes inside `playground/` and sends messages.
   - `BUILD` writes inside `projects/` and sends messages.
   - `MANAGER` writes inside `manager/`, may edit root docs, and sends messages.
4. **Small diffs by default.**
   - Default limit per run: ≤ 10 files changed, ≤ 500 lines diff (unless MANAGER explicitly requests more).
5. **Be reproducible by default.**
   - When you propose an experiment, include: hypothesis, metric, baseline, and a kill-criterion.
6. **No secrets.**
   - Never write API keys/tokens into the repo.
7. **Truthfulness + citations.**
   - For non-trivial factual claims (papers, numbers, APIs), include a source (URL, arXiv, DOI).
   - Mark speculation as speculation.

## Authority

- `MANAGER` directives are highest priority.
- Other agents can suggest alternatives; MANAGER decides.

## Feedback loop (minimum viable)

Every round must include at least:

- Each non-manager agent sends MANAGER:
  - A short summary of what changed
  - Links to key artifacts
  - 1–3 suggestions (technical or workflow)

MANAGER should respond with:
- Clear acceptance/rejection decisions
- Follow-up tasks for next round

## Rounds

Rounds are the “synchronization barrier” for parallel work.

- MANAGER opens a round by issuing tasks.
- Non-manager agents do not advance the round number.
- MANAGER closes the round and decides what carries over.

See `ROUNDS.md`.
