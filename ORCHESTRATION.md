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
