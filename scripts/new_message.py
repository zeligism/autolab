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
import os
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
