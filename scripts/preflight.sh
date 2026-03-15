#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

info() {
  echo "[preflight] $*"
}

command -v git >/dev/null 2>&1 || fail "git is required."
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || fail "Not inside a git repository."

branch="$(git branch --show-current)"
[ "$branch" = "run" ] || fail "Current branch is '$branch'; expected 'run'."

origin_url="$(git remote get-url origin 2>/dev/null || true)"
[ -n "$origin_url" ] || fail "Remote 'origin' is not configured."
info "origin=$origin_url"

[ -z "$(git status --porcelain)" ] || fail "Working tree is dirty; commit/stash/discard local changes first."

git fetch origin run >/dev/null 2>&1 || fail "Unable to fetch origin/run."
git ls-remote --exit-code --heads origin run >/dev/null 2>&1 || fail "origin/run not found. Push/create branch first."

counts="$(git rev-list --left-right --count origin/run...HEAD 2>/dev/null || true)"
[ -n "$counts" ] || fail "Unable to compare local HEAD with origin/run."
behind="$(printf '%s\n' "$counts" | awk '{print $1}')"
ahead="$(printf '%s\n' "$counts" | awk '{print $2}')"

[ "$behind" = "0" ] || fail "Local branch is behind origin/run by $behind commit(s); sync before starting."

missing=()
for var in GITHUB_USERNAME GITHUB_TOKEN; do
  if [ -z "${!var:-}" ]; then
    missing+=("$var")
  fi
done

if [ "${#missing[@]}" -gt 0 ]; then
  fail "Missing required env vars: ${missing[*]}"
fi

if [ "$ahead" != "0" ]; then
  info "Local branch is ahead of origin/run by $ahead commit(s)."
fi

info "branch=run, worktree=clean, origin/run reachable, env vars present."
info "Preflight checks passed."
