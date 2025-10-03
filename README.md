# Stasis Hunters — Phase 1 (MVP)

A compact console prototype of **Stasis Hunters** focused on Phase 1: a playable core loop (chapters → scenes → choices), an inventory & Chronicle, a simple Anchor mini-game, and JSON save/load.

This repo contains lightweight, data-driven code meant to be readable and easy to iterate on. No third-party libraries required — just Python.

---

## Status
**Phase 1 — MVP implemented** (console prototype).
Key deliverables included in this branch:
- Chapter → Scene → Choice console navigation.
- Inventory and `Chronicle` UI (console).
- Anchor mini-game (fast math puzzle with Perfect / Partial / Fail outcomes).
- Save/load system writing `saves/save.json` with `chronicle_entries` and inventory.

---

## Requirements
- Python 3.8+ (standard library only)
- Platform: cross-platform console (Windows / macOS / Linux)

---

## Quick start

1. Clone or unpack the project into a directory.
2. From the repository root, run:

```bash
python run_game.py
# or
python -m src.game
