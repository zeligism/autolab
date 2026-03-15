# Rounds

This org runs in discrete **rounds** to keep parallel work coherent.

## Round lifecycle

### 0) Pre-round (human)
- You (human) may edit any `AGENT.md`.
- You may also pause/stop the org by editing `manager/STATE.json` (see `CODEX_RUNBOOK.md`).
- For every Codex session, sync local repo from `origin/run` first (see `CODEX_RUNBOOK.md` preflight/startup sequence).

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
1. Sync local repo from `origin/run` at the start of the session.
2. Read `AGENT.md` (charter) and root docs (`CONSTITUTION.md`, `MESSAGE_PROTOCOL.md`).
3. Read all messages in `inbox/` with `round: Rk`.
4. Perform work **only inside their own directory**.
5. Send results back to `manager/inbox/`.
6. Set their `STATE.json`:
   - `current_round = k`
   - `phase = "done"`
   - `done = true`
7. Publish to `origin/run` so other sessions can pick up the latest state.

### 3) Manager closes Round Rk
Manager waits until all other agents have `done=true` for round k (or decides to proceed anyway).

Then Manager:
1. Reviews inbound messages and artifacts.
2. Records decisions + rationale.
3. Promotes a small number of items (e.g., PLAY idea → PROJECT).
4. Updates the long-term agenda if needed.
5. Sets `manager/STATE.json.phase = "closed"` and `done=true`.
6. Publishes the closure state to `origin/run`.

## State file (`STATE.json`) expectations

Each agent owns their own `STATE.json`. At minimum it tracks:

- `agent` (string)
- `current_round` (int)
- `phase` (string: idle|working|done|open|closed)
- `done` (bool)
- `run_state` (string: RUNNING|PAUSED|STOPPED)

The manager may add fields later, but keep it simple.
