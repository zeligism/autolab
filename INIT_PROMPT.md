=== BEGIN CODEX PROMPT ===
Populate the seed repo with the exact file tree and file contents below.
If a file already exists, overwrite it. Create any missing directories.
Do not add extra files beyond what is specified.

## File: .gitignore
```gitignore
# Python
__pycache__/
*.py[cod]
*.so

# Virtual envs
.venv/
venv/

# Jupyter
.ipynb_checkpoints/

# OS
.DS_Store

# Editor
.vscode/
.idea/

# Logs / runs / artifacts
*.log
runs/
outputs/
wandb/

# Large ML artifacts
*.pt
*.pth
*.bin
*.safetensors
*.ckpt
*.onnx

# Data / caches
**/data/
**/datasets/
**/.cache/

# External repos cloned into playground pilots
playground/**/external/

# Autoresearch-specific: results tables should stay local unless curated
**/results.tsv
```

## File: README.md
```markdown
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
```

## File: CONSTITUTION.md
```markdown
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
```

## File: MESSAGE_PROTOCOL.md
```markdown
# Message Protocol (inbox directories)

Inter-agent communication happens **only** through message files.

- Each agent has an `inbox/` directory.
- **To message an agent:** create a new `.md` file in the recipient’s `inbox/`.
- Never edit or delete existing message files.

## Filename convention

Use a collision-resistant filename so parallel writers don’t conflict:

```
YYYYMMDDTHHMMSSZ__FROM-<SENDER>__TO-<RECIPIENT>__TYPE-<TYPE>__R<0000>__<slug>__<rand>.md
```

Example:

```
20260314T120501Z__FROM-MANAGER__TO-LIT__TYPE-DIRECTIVE__R0000__build-topic-map__a1b2.md
```

- `<rand>` can be 4–8 hex chars.
- `<slug>` should be short; avoid spaces.

## Message body format

Each message file starts with YAML front matter:

```yaml
---
id: MSG-20260314T120501Z-a1b2
created: 2026-03-14T12:05:01Z
round: R0000
from: MANAGER
to: LIT
type: DIRECTIVE      # DIRECTIVE|REQUEST|REVIEW|INFO|DECISION|BLOCKER
priority: P1         # P0|P1|P2
subject: "Build efficient-training topic map"
context_paths:
  - lit_review/INDEX.md
reply_to: null       # set to an id when replying
---
```

Then a short markdown body:

```md
## Context
<what this is about>

## Ask
<what you want done>

## Constraints
<time/compute/format>

## Done-when
<explicit acceptance criteria>
```

## Replying

To reply, create a new message file in the sender’s inbox:

- Set `reply_to: <original id>`
- Quote the key parts you’re responding to (briefly)
- Provide your answer + links to artifacts

## “Cleaning” the inbox

Recipients do **not** delete messages. Instead:

- Agents use `STATE.json` (`round`, `done`) to stay idempotent.
- Optionally, MANAGER may later archive older messages by moving them into an `inbox/archive/` folder.

(Archiving is optional; start simple.)
```

## File: ROUNDS.md
```markdown
# Rounds

This org runs in discrete **rounds** to keep parallel work coherent.

## Round lifecycle

### 0) Pre-round (human)
- You (human) may edit any `AGENT.md`.
- You may also pause/stop the org by editing `manager/STATE.json` (see `CODEX_RUNBOOK.md`).

### 1) Manager opens Round Rk
Manager does:
1. Set `manager/STATE.json.current_round = k` and `phase = "open"`.
2. Review carry-overs from last round.
3. Create task messages into:
   - `lit_review/inbox/`
   - `playground/inbox/`
   - `projects/inbox/`
4. Optionally create cross-review tasks (e.g., PLAY asks LIT to sanity-check).
5. Update `manager/DASHBOARD.md` with the round goals.

### 2) Agents execute in parallel
Each non-manager agent:
1. Read `AGENT.md` (charter) and root docs (`CONSTITUTION.md`, `MESSAGE_PROTOCOL.md`).
2. Read all messages in `inbox/` with `round: Rk`.
3. Perform work **only inside their own directory**.
4. Send results back to `manager/inbox/`.
5. Set their `STATE.json`:
   - `current_round = k`
   - `phase = "done"`
   - `done = true`

### 3) Manager closes Round Rk
Manager waits until all other agents have `done=true` for round k (or decides to proceed anyway).

Then Manager:
1. Reviews inbound messages and artifacts.
2. Records decisions + rationale.
3. Promotes a small number of items (e.g., PLAY idea → PROJECT).
4. Updates the long-term agenda if needed.
5. Sets `manager/STATE.json.phase = "closed"` and `done=true`.

## State file (`STATE.json`) expectations

Each agent owns their own `STATE.json`. At minimum it tracks:

- `agent` (string)
- `current_round` (int)
- `phase` (string: idle|working|done|open|closed)
- `done` (bool)
- `run_state` (string: RUNNING|PAUSED|STOPPED)

The manager may add fields later, but keep it simple.
```

## File: ORCHESTRATION.md
```markdown
# Orchestration design (upgrade-friendly)

This repo uses a **disk-backed protocol** that is intentionally compatible with more advanced orchestrators later.

## Current runner (simple)

- You manually run each agent (e.g., via Codex) once per round.
- The repo is the shared state.

## Stable on-disk contract

Each agent directory exposes:

- **Charter**: `AGENT.md` (human-edited, immutable for agents)
- **State**: `STATE.json` (machine-readable)
- **Messages**: `inbox/*.md` (append-only)
- **Artifacts**: normal files in the agent directory

If we preserve this contract, we can swap in a runner later.

## LangGraph-style mapping

- Graph nodes = agents
- Global state = a merged view of the `STATE.json` files
- Edges/messages = `inbox/` message events

## Agents SDK-style mapping

- Agents = each directory
- Handoffs = message files
- Guardrails = constraints in `AGENT.md` + `CONSTITUTION.md`

The goal is to keep the repo protocol stable, while upgrading the runtime.
```

## File: CODEX_RUNBOOK.md
```markdown
# Codex Runbook

This is a **practical guide** for running the 4-agent org using Codex (or any coding agent) in **rounds**.

## One-time setup

1) Initialize a git repo (recommended):

```bash
git init
```

2) Skim these docs once:
- `CONSTITUTION.md`
- `MESSAGE_PROTOCOL.md`
- `ROUNDS.md`

3) Optional: create a clean working branch:

```bash
git checkout -b run
```

## The mental model

- You are the **orchestrator** (lightweight).
- Codex runs each agent **independently**.
- The repo is the shared memory.
- Synchronization happens at the **end of a round**, when the manager closes it.

## Starting Round 0

### Step A — Run MANAGER (opens the round)

Open a Codex session with repo access.
Paste something like this (edit only the round number if you want):

```text
You are the MANAGER agent.

Hard rules:
- You MUST follow manager/AGENT.md.
- You MUST NOT edit any AGENT.md file.
- You MUST follow CONSTITUTION.md and MESSAGE_PROTOCOL.md.

Round: R0000.

Your job now:
1) Read manager/STATE.json. If run_state is PAUSED or STOPPED, do not open the round.
2) Open Round R0000:
   - Set manager/STATE.json current_round=0, phase="open", done=false.
   - Write clear task messages (one file per message) into:
     - lit_review/inbox/
     - playground/inbox/
     - projects/inbox/
   - Ensure tasks align with the agenda "efficient training of deep learning".
3) Update manager/DASHBOARD.md with:
   - round goals
   - expected deliverables from each agent
   - review plan
4) Stop after opening the round (do NOT close it yet).
```

### Step B — Run LIT, PLAY, BUILD in parallel

Open 3 additional Codex sessions (or do sequentially), one per agent.
Each agent runs exactly one round and then stops.

#### LIT prompt

```text
You are the LIT agent.

Hard rules:
- Follow lit_review/AGENT.md.
- Do NOT edit any AGENT.md.
- Follow CONSTITUTION.md and MESSAGE_PROTOCOL.md.

Now:
1) Read lit_review/STATE.json.
2) Read messages in lit_review/inbox/ for your current round.
3) Do the work requested, writing only inside lit_review/.
4) Send a results summary to manager/inbox/ (new message file).
5) Update lit_review/STATE.json: phase="done", done=true.
Then stop.
```

#### PLAY prompt

```text
You are the PLAY agent.

Hard rules:
- Follow playground/AGENT.md.
- Do NOT edit any AGENT.md.
- Follow CONSTITUTION.md and MESSAGE_PROTOCOL.md.

Now:
1) Read playground/STATE.json.
2) Read messages in playground/inbox/ for your current round.
3) Do the work requested, writing only inside playground/.
4) Send a results summary to manager/inbox/ (new message file).
5) Update playground/STATE.json: phase="done", done=true.
Then stop.
```

#### BUILD prompt

```text
You are the BUILD agent.

Hard rules:
- Follow projects/AGENT.md.
- Do NOT edit any AGENT.md.
- Follow CONSTITUTION.md and MESSAGE_PROTOCOL.md.

Now:
1) Read projects/STATE.json.
2) Read messages in projects/inbox/ for your current round.
3) Do the work requested, writing only inside projects/.
4) Send a results summary to manager/inbox/ (new message file).
5) Update projects/STATE.json: phase="done", done=true.
Then stop.
```

### Step C — Run MANAGER again (closes the round)

When the other agents are done, run MANAGER again:

```text
You are the MANAGER agent.

Hard rules:
- Follow manager/AGENT.md.
- Do NOT edit any AGENT.md.
- Follow CONSTITUTION.md and MESSAGE_PROTOCOL.md.

Round: R0000.

Now:
1) Read all inbound messages in manager/inbox/ for round R0000.
2) Review new artifacts produced by other agents.
3) Update manager/DASHBOARD.md with decisions.
4) If appropriate, promote exactly ONE idea into a more serious next step.
5) Set manager/STATE.json: phase="closed", done=true.
6) Create next-round task messages (R0001) OR explicitly say why you are not opening the next round.
Then stop.
```

## Monitoring progress

- Quick check: open each `*/STATE.json` and look for `done=true`.
- View message traffic: list files in `*/inbox/`.
- Optional CLI helper:

```bash
python scripts/status.py
```

## Pausing / stopping

This workflow is **human-controlled**.

- To pause: set `manager/STATE.json.run_state = "PAUSED"`.
  - When MANAGER runs and sees PAUSED, it should not open a new round.
- To stop entirely: set `manager/STATE.json.run_state = "STOPPED"`.

To resume later:
- set `run_state` back to `RUNNING`
- run MANAGER to open the next round.

## Upgrading later (Agents SDK / LangGraph)

This repo already exposes a clean interface:

- **State**: `STATE.json`
- **Messages**: files in `inbox/`
- **Outputs**: normal files in the agent directory

That maps naturally to:
- LangGraph-style state machines (nodes = agents, state = JSON)
- Agents SDK / handoffs (messages = events)

Keep the on-disk protocol stable so you can swap the runner later.
```

## Directory: scripts

### File: scripts/README.md
```markdown
# Scripts

These scripts are **optional** quality-of-life helpers.

They do not run agents; they help you inspect and manage the repo state.

- `new_message.py` — create a properly formatted message file in a recipient inbox.
- `status.py` — print a quick overview of round/done status across agents.
```

### File: scripts/new_message.py
```python
#!/usr/bin/env python3
"""Create a new message file in an agent inbox.

Usage example:
  python scripts/new_message.py \
    --to LIT --from MANAGER --type DIRECTIVE --priority P1 --round R0000 \
    --subject "Build topic map" \
    --context lit_review/INDEX.md \
    --ask "Create a taxonomy + open problems list" \
    --constraints "~2 pages; cite sources" \
    --done_when "A new topic map doc exists + index updated"
"""

from __future__ import annotations

import argparse
import secrets
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


AGENT_DIR = {
    "MANAGER": "manager",
    "LIT": "lit_review",
    "PLAY": "playground",
    "BUILD": "projects",
    "USER": "manager",  # user messages typically go to manager
}


@dataclass
class Msg:
    msg_id: str
    created_iso: str
    round_id: str
    sender: str
    recipient: str
    msg_type: str
    priority: str
    subject: str
    context_paths: List[str]
    reply_to: Optional[str]
    context: str
    ask: str
    constraints: str
    done_when: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def slugify(s: str) -> str:
    s = s.strip().lower()
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch in {" ", "-", "_"}:
            out.append("-")
    slug = "".join(out)
    slug = "-".join([p for p in slug.split("-") if p])
    return slug[:60] or "message"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True, help="Recipient agent tag (MANAGER|LIT|PLAY|BUILD)")
    ap.add_argument("--from", dest="sender", required=True, help="Sender agent tag")
    ap.add_argument("--type", dest="msg_type", default="INFO", help="DIRECTIVE|REQUEST|REVIEW|INFO|DECISION|BLOCKER")
    ap.add_argument("--priority", default="P2", help="P0|P1|P2")
    ap.add_argument("--round", dest="round_id", required=True, help="Round id like R0000")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--context", action="append", default=[], help="Context path(s) (repeatable)")
    ap.add_argument("--reply-to", default=None)
    ap.add_argument("--context-text", default="")
    ap.add_argument("--ask", default="")
    ap.add_argument("--constraints", default="")
    ap.add_argument("--done-when", default="")

    args = ap.parse_args()

    to = args.to.strip().upper()
    sender = args.sender.strip().upper()
    msg_type = args.msg_type.strip().upper()
    priority = args.priority.strip().upper()
    round_id = args.round_id.strip().upper()

    if to not in AGENT_DIR:
        raise SystemExit(f"Unknown --to {to}. Expected one of {sorted(AGENT_DIR.keys())}")

    now = utc_now()
    ts = now.strftime("%Y%m%dT%H%M%SZ")
    rand = secrets.token_hex(2)
    msg_id = f"MSG-{ts}-{rand}"

    slug = slugify(args.subject)
    fname = f"{ts}__FROM-{sender}__TO-{to}__TYPE-{msg_type}__{round_id}__{slug}__{rand}.md"

    inbox_dir = Path(AGENT_DIR[to]) / "inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)

    path = inbox_dir / fname

    m = Msg(
        msg_id=msg_id,
        created_iso=now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        round_id=round_id,
        sender=sender,
        recipient=to,
        msg_type=msg_type,
        priority=priority,
        subject=args.subject,
        context_paths=args.context,
        reply_to=args.reply_to,
        context=args.context_text,
        ask=args.ask,
        constraints=args.constraints,
        done_when=args.done_when,
    )

    yaml_lines = [
        "---",
        f"id: {m.msg_id}",
        f"created: {m.created_iso}",
        f"round: {m.round_id}",
        f"from: {m.sender}",
        f"to: {m.recipient}",
        f"type: {m.msg_type}",
        f"priority: {m.priority}",
        f"subject: \"{m.subject.replace('\\"', '\\"')}\"",
        "context_paths:",
    ]
    for cp in m.context_paths:
        yaml_lines.append(f"  - {cp}")
    yaml_lines.append(f"reply_to: {m.reply_to if m.reply_to else 'null'}")
    yaml_lines.append("---")

    body = f"""# {m.subject}

## Context
{m.context or "(none)"}

## Ask
{m.ask or "(none)"}

## Constraints
{m.constraints or "(none)"}

## Done-when
{m.done_when or "(none)"}
"""

    path.write_text("\n".join(yaml_lines) + "\n\n" + body, encoding="utf-8")
    print(str(path))


if __name__ == "__main__":
    main()
```

### File: scripts/status.py
```python
#!/usr/bin/env python3
"""Quick status view for the 4-agent org."""

from __future__ import annotations

import json
from pathlib import Path

AGENTS = [
    ("MANAGER", Path("manager")),
    ("LIT", Path("lit_review")),
    ("PLAY", Path("playground")),
    ("BUILD", Path("projects")),
]


def load_state(p: Path) -> dict:
    try:
        return json.loads((p / "STATE.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def count_inbox(p: Path, round_id: str) -> tuple[int, int]:
    inbox = p / "inbox"
    if not inbox.exists():
        return (0, 0)
    files = [f for f in inbox.iterdir() if f.is_file() and f.suffix.lower() == ".md"]
    total = len(files)
    cur = len([f for f in files if round_id in f.name])
    return (total, cur)


def main() -> None:
    print("Agent status")
    print("=" * 60)
    for tag, p in AGENTS:
        st = load_state(p)
        r = st.get("current_round", 0)
        round_id = f"R{int(r):04d}" if isinstance(r, (int, float, str)) else "R0000"
        phase = st.get("phase", "?")
        done = st.get("done", False)
        run_state = st.get("run_state", "?")
        updated_at = st.get("updated_at", "?")
        total, cur = count_inbox(p, round_id)
        print(f"{tag:7s} | round={round_id:5s} | phase={phase:7s} | done={str(done):5s} | run_state={run_state:7s} | inbox(total={total}, this_round={cur}) | updated_at={updated_at}")


if __name__ == "__main__":
    main()
```

## Directory: manager

### File: manager/AGENT.md
```markdown
# MANAGER Agent Charter (read-only; human-edited)

You are **MANAGER**.

Your job is to make this multi-agent research org:
- coherent,
- productive,
- self-improving,
- and easy to audit.

You are also the **reviewer-of-record** for promoted projects.

## Absolute rules

- **Never edit any `AGENT.md` file** (including this one).
- Follow `CONSTITUTION.md`, `MESSAGE_PROTOCOL.md`, `ROUNDS.md`.
- You may only communicate with other agents by **creating new message files** in their `inbox/` directories.
- Do not edit or delete existing message files.
- Do not edit other agents’ `STATE.json`.

## Research direction

Current umbrella direction:

> **More efficient training of deep learning models** (time/compute/memory/data efficiency).

Maintain and refine the agenda in `manager/AGENDA.md`.

## Responsibilities

### Orchestration

- Open each round by:
  - updating `manager/STATE.json` (`phase="open"`, `done=false`)
  - writing task messages into other agents’ inboxes (one file per task)
  - updating `manager/DASHBOARD.md`

- Close each round by:
  - reading inbound messages in `manager/inbox/`
  - reviewing artifacts
  - making decisions (promote/kill/carry)
  - recording decisions in `manager/DASHBOARD.md` and (if durable) in `DECISIONS.md`
  - setting `manager/STATE.json` to `phase="closed"`, `done=true`

### Quality control

- Enforce WIP limits (see `manager/WORKFLOW.md`).
- Ensure at least one review interaction occurs per non-manager agent per round.
- Keep diffs small and artifacts discoverable.

### Self-improvement

Each round, solicit from every agent:
- 1 improvement to workflow
- 1 research hypothesis worth testing

Decide whether to adopt improvements and update `manager/WORKFLOW.md` accordingly.

## What to write

You primarily write in:

- `manager/` (agenda, workflow, dashboard)
- root docs when needed

You may write new message files into:

- `lit_review/inbox/`
- `playground/inbox/`
- `projects/inbox/`

## Round procedure (one MANAGER run)

1) Read:
   - `manager/STATE.json`
   - `manager/AGENDA.md`
   - `manager/DASHBOARD.md`
   - inbound messages in `manager/inbox/` for the current round

2) If `run_state` is `PAUSED` or `STOPPED`:
   - do not open a new round
   - optionally write a short note in `manager/LOG.md`
   - stop

3) If opening a round:
   - pick 1–2 focus themes
   - issue tasks with explicit done-when

4) If closing a round:
   - summarize outcomes
   - decide promotions
   - write next-round tasks OR explicitly pause

## Style

- Be explicit and operational.
- Use checklists and acceptance criteria.
- Prefer short messages over long essays.
```

### File: manager/STATE.json
```json
{
  "agent": "MANAGER",
  "current_round": 0,
  "phase": "idle",
  "done": false,
  "run_state": "RUNNING",
  "updated_at": "2026-03-14T00:00:00Z",
  "notes": "Edit run_state to PAUSED/STOPPED to halt new rounds."
}
```

### File: manager/INBOX.md
```markdown
# Inbox

This agent's inbox is the `inbox/` directory.

- Each incoming message is a **separate `.md` file**.
- Other agents communicate with you by creating new files in `inbox/`.
- Do not delete or edit message files.

See the global protocol in `MESSAGE_PROTOCOL.md`.
```

### File: manager/inbox/.gitkeep
```text

```

### File: manager/INDEX.md
```markdown
# Manager Index

Key docs:

- `AGENDA.md` — long-term and near-term research agenda (currently: efficient training)
- `WORKFLOW.md` — how rounds and reviews work
- `RUBRICS.md` — promotion rubrics (lit → playground → projects)
- `DASHBOARD.md` — current round status + decisions
- `DECISIONS.md` — durable decisions and rationales
- `LOG.md` — manager log
```

### File: manager/AGENDA.md
```markdown
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
```

### File: manager/WORKFLOW.md
```markdown
# Workflow

This document is owned by MANAGER and can evolve.

## Principles

- **Kill ideas cheaply.** Prefer fast falsification over long builds.
- **WIP limits.** Keep the org focused.
- **Make artifacts discoverable.** Index everything.

## Round rhythm (baseline)

Each round should follow:

1) MANAGER opens round:
   - Posts tasks to each agent
   - Defines what “done” means

2) LIT / PLAY / BUILD run in parallel:
   - Do one round worth of work
   - Report back with links
   - Mark done in `STATE.json`

3) MANAGER closes round:
   - Reviews deliverables
   - Records decisions
   - Promotes or kills items
   - Issues next round tasks

## WIP limits (starting values)

- Lit topics actively being expanded: ≤ 5
- Playground ideas active: ≤ 7
- Projects active: ≤ 2

## Review loop requirement (minimal)

Every round:

- LIT requests at least one sanity check from PLAY or MANAGER.
- PLAY requests at least one sanity check from LIT or MANAGER.
- BUILD requests review from MANAGER.

(Review = message with type `REVIEW` + explicit feedback.)

## Promotion pipeline

- Lit → Playground: requires a crisp hypothesis + proposed toy test.
- Playground → Projects: requires toy evidence + clear baseline + plausible 1-GPU-hours experiment.

Rubrics are in `RUBRICS.md`.
```

### File: manager/RUBRICS.md
```markdown
# Rubrics

## Lit → Playground (should we prototype?)

Score each criterion 0–2.

1) **Clarity**: hypothesis is testable and specific
2) **Cheap test**: toy test can run in minutes (or analytic check)
3) **Novelty**: not a trivial rehash; or a fresh angle on known method
4) **Impact potential**: would matter for efficient training if true
5) **Risk**: manageable failure modes; clear kill criterion

Promote if total ≥ 7/10.

## Playground → Projects (should we invest?)

1) **Toy evidence**: a toy result survives basic ablations
2) **Baseline**: clear baseline and metric
3) **Feasibility**: can run on 1 GPU in a few hours (for now)
4) **Differentiation**: not obviously dominated by existing SOTA
5) **Story**: can be written as a coherent paper section

Promote if total ≥ 8/10.
```

### File: manager/DASHBOARD.md
```markdown
# Dashboard

## Current round

- Round: R0000
- Status: not started

## Agent statuses

- LIT: (see lit_review/STATE.json)
- PLAY: (see playground/STATE.json)
- BUILD: (see projects/STATE.json)

## This round goals

- (manager fills when opening round)

## Decisions

- (manager fills when closing round)

## Promotion queue

- Candidate ideas:
  - (none yet)
```

### File: manager/DECISIONS.md
```markdown
# Decisions

Durable decisions and rationales. Append-only.

Template:

- `YYYY-MM-DD` — **Decision**: ...
  - Rationale:
  - Alternatives considered:
  - Follow-ups:
```

### File: manager/LOG.md
```markdown
# Manager Log

Append-only notes by MANAGER.

Format suggestion:

- `2026-03-14T00:00Z` — note
```

### File: manager/inbox/20260314T000000Z__FROM-USER__TO-MANAGER__TYPE-DIRECTIVE__R0000__initial-steering__seed.md
```markdown
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
```

## Directory: lit_review

### File: lit_review/AGENT.md
```markdown
# LIT Agent Charter (read-only; human-edited)

You are **LIT**.

Your mission is to build a **high-signal, highly discoverable** literature review corpus that feeds rapid prototyping.

## Absolute rules

- **Never edit any `AGENT.md` file**.
- Follow `CONSTITUTION.md`, `MESSAGE_PROTOCOL.md`, `ROUNDS.md`.
- Write only inside `lit_review/`.
- Communicate with others only by creating new message files in their `inbox/`.
- Never edit or delete existing message files.
- Only you edit `lit_review/STATE.json`.

## Scope

Focus on:

> **Efficient training of deep learning models** (time/compute/memory/data efficiency).

## Primary outputs

1) **Topic maps**
   - Taxonomies, subproblems, key references

2) **SOTA summaries**
   - What works, what doesn’t, and why

3) **Open problems + gaps**
   - Under-explored directions
   - Missing baselines
   - Confusing or contradictory results

4) **Playground seeds**
   - Crisp hypotheses + proposed toy tests

## Organization rules

- Put topic docs in `lit_review/topics/`.
- Update `lit_review/INDEX.md` whenever you add a topic.
- Each topic doc should include:
  - 5–15 key references (links/arXiv)
  - 3–10 open problems
  - 3–10 playground seeds

## Citations

- Prefer primary sources (papers, official docs).
- Include URLs or arXiv IDs.
- Mark speculation clearly.

## Round procedure

When you are run for a round:

1) Read `lit_review/STATE.json`.
2) Read messages in `lit_review/inbox/` for `R{current_round:04d}`.
3) Execute requested tasks.
4) Send a summary message to `manager/inbox/` including:
   - links to new/updated docs
   - your top 3 seeds
   - 1 workflow improvement suggestion
5) Update `lit_review/STATE.json` (`phase="done"`, `done=true`, `updated_at=...`).
6) Stop.

## Default constraints

- Prefer many small docs over one giant doc.
- Keep new topic docs to ~2–6 pages unless requested otherwise.
```

### File: lit_review/STATE.json
```json
{
  "agent": "LIT",
  "current_round": 0,
  "phase": "idle",
  "done": false,
  "run_state": "RUNNING",
  "updated_at": "2026-03-14T00:00:00Z",
  "notes": ""
}
```

### File: lit_review/INBOX.md
```markdown
# Inbox

This agent's inbox is the `inbox/` directory.

- Each incoming message is a **separate `.md` file**.
- Other agents communicate with you by creating new files in `inbox/`.
- Do not delete or edit message files.

See the global protocol in `MESSAGE_PROTOCOL.md`.
```

### File: lit_review/inbox/.gitkeep
```text

```

### File: lit_review/INDEX.md
```markdown
# Lit Review Index

This directory is for **discoverable literature synthesis**.

Structure:

- `topics/` — topic maps and deep dives (one file per topic)
- `topics/TEMPLATE_TOPIC.md` — template

Start here:
- `topics/T-20260314-efficient-training-map.md`
```

### File: lit_review/LOG.md
```markdown
# Lit Review Log

Append-only notes by LIT.
```

### File: lit_review/topics/README.md
```markdown
# Topics

One markdown file per topic.

Naming:
- `T-YYYYMMDD-<slug>.md`

Each topic doc should include:
- a short taxonomy
- key references (URLs/arXiv)
- open problems
- playground seeds (hypotheses + toy tests)
```

### File: lit_review/topics/TEMPLATE_TOPIC.md
```markdown
---
id: T-YYYYMMDD-your-topic
created: YYYY-MM-DD
updated: YYYY-MM-DD
area: efficient-training
status: draft
---

# Title

## Why this matters

## Problem statement

## Key ideas / taxonomy

## Representative methods

## Key references (primary)
- 

## Open problems
- 

## Playground seeds (hypotheses + toy tests)

### Seed 1
- Hypothesis:
- Toy test:
- Metric:
- Kill criterion:

```

### File: lit_review/topics/T-20260314-efficient-training-map.md
```markdown
---
id: T-20260314-efficient-training-map
created: 2026-03-14
updated: 2026-03-14
area: efficient-training
status: seed
---

# Efficient training of deep learning models: a working map (seed)

This is an initial **topic map** to steer early rounds.

## What “efficient” can mean

- **Wall-clock**: tokens/sec, steps/sec, time-to-X
- **Compute**: FLOPs, total training compute for target quality
- **Memory**: peak VRAM, activation/optimizer state footprint
- **Data efficiency**: fewer examples/tokens for same quality
- **Energy/cost**: $ and kWh per run (often derived)

## Taxonomy (v0)

### 1) Numerics & precision

- mixed precision (fp16/bf16)
- low precision formats (e.g., fp8)
- quantized optimizer states
- stability methods (loss scaling, clipping, normalization tweaks)

### 2) Optimization & learning dynamics

- optimizers (Adam variants, SGD variants, second-order approximations)
- LR schedules and warmup strategies
- scaling-law-aware training and early stopping
- faster convergence per token

### 3) Architecture and conditional compute

- sparsity (structured/unstructured)
- mixture-of-experts (MoE)
- parameter sharing / tying
- low-rank structure

### 4) Systems

- memory saving: activation checkpointing, sharding, offloading
- speed: fused kernels, efficient attention kernels, compilation
- communication efficiency (multi-GPU) (future)
- dataloader + I/O bottlenecks

### 5) Data efficiency

- deduplication + quality filtering
- curriculum / sampling strategies
- synthetic data and distillation

## Open problems (starter list)

1) **Comparable evaluation**: how to fairly compare training efficiency across architectures and tokenization choices.
2) **Hardware specificity**: improvements that help on one GPU may hurt on another.
3) **Stability at low precision**: robust recipes that are not fragile to model scale.
4) **Measuring “data quality”**: simple predictors that generalize across domains.
5) **Interaction effects**: e.g., optimizer × precision × architecture.

## Playground seeds

### Seed A — efficiency metrics sanity suite

- Hypothesis: Many “efficiency” claims fail under a fixed, transparent metric suite.
- Toy test: build a tiny benchmark harness on a small model (e.g., MLP/CNN/mini-transformer) that reports:
  - peak memory
  - tokens/sec
  - validation loss after fixed wall-clock budget
- Kill criterion: metrics are too noisy to discriminate within minutes.

### Seed B — optimizer-state footprint reduction

- Hypothesis: Reducing optimizer state precision can reduce memory with minimal loss.
- Toy test: train a tiny transformer with optimizer-state quantization vs baseline.
- Metric: validation loss vs peak memory.
- Kill criterion: instability or large degradation.

### Seed C — activation checkpointing trade curve

- Hypothesis: checkpointing yields predictable memory/time tradeoffs that can be exploited by agent search.
- Toy test: a small transformer training loop with/without checkpointing.
- Metric: peak memory vs throughput vs loss.
- Kill criterion: overhead dominates at small scale.
```

## Directory: playground

### File: playground/AGENT.md
```markdown
# PLAY Agent Charter (read-only; human-edited)

You are **PLAY**.

Your mission is **rapid falsification**:
- turn lit-review seeds into crisp hypotheses,
- run tiny experiments or analytic checks,
- write short, readable reports,
- and recommend what to promote.

## Absolute rules

- **Never edit any `AGENT.md` file**.
- Follow `CONSTITUTION.md`, `MESSAGE_PROTOCOL.md`, `ROUNDS.md`.
- Write only inside `playground/`.
- Communicate with others only by creating new message files in their `inbox/`.
- Never edit or delete existing message files.
- Only you edit `playground/STATE.json`.

## Scope

Focus on:

> **Efficient training of deep learning models**.

## Primary outputs

- `playground/ideas/`:
  - 1–3 page idea notes
  - hypothesis, method, toy test, kill criteria

- Toy experiments:
  - small scripts/notebooks that run in seconds–minutes
  - clean outputs + tiny writeup

- Recommendations:
  - what to promote to `projects/`
  - what to kill and why

## Special seed project: Autoresearch pilot

There is an initial pilot in:

- `playground/pilots/AR-20260314-autoresearch-pilot/`

Your job is to:
- set it up (clone externally),
- run a **short** validation run,
- and write a short report on what the system teaches us about structuring agentic research.

## Round procedure

1) Read `playground/STATE.json`.
2) Read messages in `playground/inbox/` for the current round.
3) Do the requested work.
4) Request at least one sanity check from LIT (or MANAGER) each round.
5) Send a summary message to `manager/inbox/` including:
   - links to idea reports
   - results of toy tests
   - your top 1–3 promote candidates
   - 1 workflow improvement suggestion
6) Update `playground/STATE.json` (`phase="done"`, `done=true`, `updated_at=...`).
7) Stop.

## Default constraints

- Prefer simple experiments (minutes, not hours).
- Keep code minimal and readable.
```

### File: playground/STATE.json
```json
{
  "agent": "PLAY",
  "current_round": 0,
  "phase": "idle",
  "done": false,
  "run_state": "RUNNING",
  "updated_at": "2026-03-14T00:00:00Z",
  "notes": ""
}
```

### File: playground/INBOX.md
```markdown
# Inbox

This agent's inbox is the `inbox/` directory.

- Each incoming message is a **separate `.md` file**.
- Other agents communicate with you by creating new files in `inbox/`.
- Do not delete or edit message files.

See the global protocol in `MESSAGE_PROTOCOL.md`.
```

### File: playground/inbox/.gitkeep
```text

```

### File: playground/INDEX.md
```markdown
# Playground Index

This directory converts lit-review seeds into **fast hypotheses and toy tests**.

Structure:

- `ideas/` — short idea writeups (1–3 pages)
- `ideas/TEMPLATE_IDEA.md`
- `pilots/` — small external code pilots (e.g., Karpathy's autoresearch)

Start here:
- `pilots/AR-20260314-autoresearch-pilot/`
```

### File: playground/LOG.md
```markdown
# Playground Log

Append-only notes by PLAY.
```

### File: playground/ideas/TEMPLATE_IDEA.md
```markdown
---
id: I-YYYYMMDD-your-idea
created: YYYY-MM-DD
status: draft
area: efficient-training
---

# Title

## Hypothesis

## Minimal toy test

- Setup:
- Baseline:
- Metric:
- Expected outcome:

## Kill criterion

## Notes / risks

## Next step if it works
```

### File: playground/pilots/AR-20260314-autoresearch-pilot/README.md
```markdown
# Autoresearch pilot (Karpathy) — playground seed

Goal: use Karpathy’s **autoresearch** repo as an example “agentic research codebase” and extract:

1) Practical lessons for our org design
2) A short validation run log
3) Potential ideas for efficient training experimentation

## What this pilot is

- A lightweight, time-boxed run (not overnight).
- A structured writeup in `REPORT.md`.

## What this pilot is NOT

- A full reproduction of autoresearch results.
- A long-running sweep.

## Files

- `RUN_SHORT.md` — exact commands for a short run
- `REPORT.md` — results + lessons learned (fill in after running)
- `NOTES.md` — scratchpad
```

### File: playground/pilots/AR-20260314-autoresearch-pilot/RUN_SHORT.md
```markdown
# Short run instructions

We keep external repos out of git history.

## 0) Clone autoresearch

From repo root:

```bash
mkdir -p playground/pilots/AR-20260314-autoresearch-pilot/external
cd playground/pilots/AR-20260314-autoresearch-pilot/external

git clone https://github.com/karpathy/autoresearch
cd autoresearch
```

(Directory `external/` is git-ignored by default.)

## 1) Follow the repo quickstart (baseline)

Autoresearch uses `uv` for env management.

Typical baseline commands:

```bash
uv sync
uv run prepare.py
uv run train.py
```

A single `train.py` run is designed to take ~5 minutes wall clock.

## 2) Time-boxing

For this pilot, do ONE of the following:

- **Option A (simplest):** run `uv run train.py` once, record metric.
- **Option B (still short):** run baseline once, then let an agent propose ONE change to `train.py`, and run once more.

Stop after ~2 experiments.

## 3) Record results

Fill in `REPORT.md`:
- hardware
- time per run
- metric reported by autoresearch
- what changed (if you did Option B)
```

### File: playground/pilots/AR-20260314-autoresearch-pilot/REPORT.md
```markdown
---
id: AR-20260314-autoresearch-pilot-report
created: 2026-03-14
status: draft
---

# Autoresearch pilot report

## Setup

- Date:
- Hardware:
- OS:
- Python:

## What I ran

- Baseline run:
- Optional modified run:

## Results

- Metric(s):
- Runtime:

## Lessons for our org design

- What autoresearch does well:
- What we should copy:
- What we should not copy:

## Follow-up ideas

- Idea 1:
- Idea 2:
```

### File: playground/pilots/AR-20260314-autoresearch-pilot/NOTES.md
```markdown
# Notes

Scratchpad.
```

### File: playground/pilots/AR-20260314-autoresearch-pilot/run_short.sh
```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
PILOT_DIR="$ROOT_DIR/playground/pilots/AR-20260314-autoresearch-pilot"
EXT_DIR="$PILOT_DIR/external"

mkdir -p "$EXT_DIR"
cd "$EXT_DIR"

if [ ! -d "autoresearch" ]; then
  git clone https://github.com/karpathy/autoresearch
fi

cd autoresearch

# Minimal baseline run (requires uv + NVIDIA GPU)
uv sync
uv run prepare.py
uv run train.py
```

## Directory: projects

### File: projects/AGENT.md
```markdown
# BUILD Agent Charter (read-only; human-edited)

You are **BUILD**.

Your mission is to take promoted ideas and turn them into:
- clean codebases,
- reproducible experiments,
- and paper-quality writeups.

(Reviewer-of-record is MANAGER.)

## Absolute rules

- **Never edit any `AGENT.md` file**.
- Follow `CONSTITUTION.md`, `MESSAGE_PROTOCOL.md`, `ROUNDS.md`.
- Write only inside `projects/`.
- Communicate with others only by creating new message files in their `inbox/`.
- Never edit or delete existing message files.
- Only you edit `projects/STATE.json`.

## Scope

Focus on projects aligned with:

> **Efficient training of deep learning models**.

## Primary outputs

- Project scaffolds (reproducible, minimal)
- Experiment scripts runnable on a single GPU (few hours)
- A draft paper outline + sections

## Round procedure

1) Read `projects/STATE.json`.
2) Read messages in `projects/inbox/` for the current round.
3) Do requested work.
4) Send a summary message to `manager/inbox/` with:
   - links to project files
   - what is ready for review
   - what is blocked
5) Update `projects/STATE.json` (`phase="done"`, `done=true`, `updated_at=...`).
6) Stop.

## Default constraints

- Keep experiments simple, isolated, and reproducible.
- Prefer one good baseline over many half-baked variants.
```

### File: projects/STATE.json
```json
{
  "agent": "BUILD",
  "current_round": 0,
  "phase": "idle",
  "done": false,
  "run_state": "RUNNING",
  "updated_at": "2026-03-14T00:00:00Z",
  "notes": ""
}
```

### File: projects/INBOX.md
```markdown
# Inbox

This agent's inbox is the `inbox/` directory.

- Each incoming message is a **separate `.md` file**.
- Other agents communicate with you by creating new files in `inbox/`.
- Do not delete or edit message files.

See the global protocol in `MESSAGE_PROTOCOL.md`.
```

### File: projects/inbox/.gitkeep
```text

```

### File: projects/INDEX.md
```markdown
# Projects Index

This directory is for **promoted** work that deserves longer experiments and paper-quality writing.

For now, it contains a project template:
- `template/`
```

### File: projects/LOG.md
```markdown
# Projects Log

Append-only notes by BUILD.
```

### File: projects/template/README.md
```markdown
# Project template

Copy this folder when promoting a playground idea into a real project.

Suggested structure:

- `code/` — library code
- `experiments/` — runnable scripts + configs
- `paper/` — paper outline + figures

## Minimal expectations

- One command to reproduce main experiment(s)
- Clear baseline
- Logging of key metrics
- Notes on compute budget
```

### File: projects/template/paper/outline.md
```markdown
# Paper outline (template)

## Title

## Abstract

## 1. Introduction

## 2. Related Work

## 3. Method

## 4. Experiments

## 5. Discussion / Limitations

## 6. Conclusion
```


### File: projects/template/code/.gitkeep
```text

```

### File: projects/template/experiments/.gitkeep
```text

```

=== END CODEX PROMPT ===
