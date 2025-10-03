
---

# `CHANGELOG.md`
```markdown
# Changelog

All notable changes to this project will be documented here. This project uses [Semantic Versioning](https://semver.org/) style notes.

## Unreleased
- (No changes yet.)

---

## v0.1.0 — 2025-10-03
Initial Phase 1 — MVP implementation (console prototype).
- Added console navigation: Chapter → Scene → Choice.
- Implemented inventory system and `Chronicle` (mirrors essential/flagged seeds).
- Implemented Anchor mini-game (timed quick puzzle with Perfect / Partial / Fail outcomes).
- Implemented save/load system writing `saves/save.json` with:
  - `player.inventory`
  - `chronicle_entries`
- Added example data files: `data/seeds.json` and `data/scenes.json`.
- Basic playtest instructions added to `README.md`.

---

## Notes
- v0.1.0 is intended as the first playable milestone for design verification and playtesting.
- Future versions will focus on branching narrative support, richer mini-games, and UI improvements.
