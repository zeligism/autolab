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
