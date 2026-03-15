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

## Git workflow

Do all work on the current branch `work`. When you are completely finished, move the final changes onto the existing branch `run` and push `run` to GitHub.

Git requirements:
1. Stay on `work` while editing.
2. Commit all finished changes on `work`.
3. Ensure a remote named `github` exists and points to `https://github.com/zeligism/autolab.git`.
   - If `github` does not exist, add it.
   - If it exists but points somewhere else, update it.
4. Fetch from `github`.
5. Check out the existing branch `run`.
6. Move the finished work from `work` onto `run` using cherry-pick of the final commit(s). Do not merge `work` into `run`.
7. Push directly to `github/run`.

Use these commands if needed:
- `git remote get-url github || git remote add github https://github.com/zeligism/autolab.git`
- `git remote set-url github https://github.com/zeligism/autolab.git`
- `git fetch github`
- `git checkout run`
- `git cherry-pick <commit-sha>`
- `git push github run`

Constraints:
- Do not push the `work` branch.
- Do not create a pull request.
- Do not push to `main`.
- The final published result must be on `github` branch `run`.
- If `origin` points elsewhere, ignore it and use `github`.

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
