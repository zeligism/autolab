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
