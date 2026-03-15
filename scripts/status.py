#!/usr/bin/env python3
"""Quick status view for the 4-agent org."""

from __future__ import annotations

import json
import subprocess
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


def normalize_round(value: object) -> str:
    if isinstance(value, (int, float)):
        return f"R{int(value):04d}"
    if isinstance(value, str):
        s = value.strip().upper()
        if s.startswith("R") and s[1:].isdigit():
            return f"R{int(s[1:]):04d}"
        if s.isdigit():
            return f"R{int(s):04d}"
    return "R0000"


def count_inbox(p: Path, round_id: str) -> tuple[int, int]:
    inbox = p / "inbox"
    if not inbox.exists():
        return (0, 0)
    files = [f for f in inbox.iterdir() if f.is_file() and f.suffix.lower() == ".md"]
    total = len(files)
    cur = len([f for f in files if round_id in f.name])
    return (total, cur)


def run_git(args: list[str]) -> tuple[int, str]:
    try:
        cp = subprocess.run(["git", *args], check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return (127, "git not found")
    text = cp.stdout.strip() if cp.stdout else cp.stderr.strip()
    return (cp.returncode, text)


def git_value(args: list[str], default: str = "?") -> str:
    rc, out = run_git(args)
    if rc == 0 and out:
        return out
    return default


def git_clean_state() -> str:
    rc, out = run_git(["status", "--porcelain"])
    if rc != 0:
        return "?"
    return "clean" if not out else "dirty"


def git_sync_state() -> str:
    rc, out = run_git(["rev-list", "--left-right", "--count", "origin/run...HEAD"])
    if rc != 0:
        return "?"
    parts = out.split()
    if len(parts) != 2:
        return "?"
    behind, ahead = parts
    return f"ahead={ahead}, behind={behind}"


def main() -> None:
    print("Git status")
    print("=" * 60)
    branch = git_value(["branch", "--show-current"])
    head = git_value(["rev-parse", "--short", "HEAD"])
    origin = git_value(["remote", "get-url", "origin"])
    clean = git_clean_state()
    sync = git_sync_state()
    print(f"branch={branch} | head={head} | worktree={clean}")
    print(f"origin={origin}")
    print(f"sync_vs_origin_run={sync}")
    print()

    print("Agent status")
    print("=" * 60)
    for tag, p in AGENTS:
        st = load_state(p)
        round_id = normalize_round(st.get("current_round", 0))
        phase = st.get("phase", "?")
        done = st.get("done", False)
        run_state = st.get("run_state", "?")
        updated_at = st.get("updated_at", "?")
        total, cur = count_inbox(p, round_id)
        print(f"{tag:7s} | round={round_id:5s} | phase={phase:7s} | done={str(done):5s} | run_state={run_state:7s} | inbox(total={total}, this_round={cur}) | updated_at={updated_at}")


if __name__ == "__main__":
    main()
