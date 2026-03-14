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
