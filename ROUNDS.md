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
