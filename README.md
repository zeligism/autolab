# Agentic Research Org (4-agent seed)

This repo is a **file-based, round-based, multi-agent research workflow**.

- There are exactly **4 agent directories** at the root:
  - `manager/` — runs the agenda + workflow; opens and closes rounds.
  - `lit_review/` — literature review, topic maps, open problems.
  - `playground/` — rapid hypotheses + toy experiments + short reports.
  - `projects/` — longer-running code + paper writing once promoted.

Each agent directory has:
- `AGENT.md` — the **immutable charter** for that agent (edited only by you).
- `STATE.json` — machine-readable state (round, done, status).
- `inbox/` — incoming messages (**one message per file**).

## Core idea

- Work happens in **rounds**.
- The **manager opens a round** by writing task messages into other agents' inboxes.
- Agents work **in parallel**, then mark themselves **done** in `STATE.json` and report back.
- The **manager closes the round**: reviews outputs, resolves conflicts, decides promotions, and creates next-round tasks.

See:
- `ROUNDS.md`
- `MESSAGE_PROTOCOL.md`
- `CODEX_RUNBOOK.md`

## Current research direction

The initial umbrella direction is:

> **More efficient training of deep learning models** (time, compute, memory, data efficiency).

The manager keeps this organized in `manager/AGENDA.md`.
