# Changelog

## [Unreleased] - 2025-10-03
### Added
- Phase 3 content fill: canonical `data/chapters.json` with scene IDs for CH01→CH13.
- Scene templates added in `data/scenes/` for each chapter; festival scene updated to `festival_awaken`.
- Chronosense / Tech Pulse settings added per chapter to support per-chapter mechanics.
- PayoffManager robustness improvements: safer loading and precise triggering logic.
- Seeds list deduplicated and corrected (`data/seeds.json`).

### Fixed
- Normalized scene IDs and fixed duplicate seed IDs (S99 duplication).
- Fixed payoff triggering logic and player flags persistence.

### Notes
- Some src modules were trimmed and validated. Additional polish and full script-based QA recommended (see `project_outline.md` Console UX patterns).

## [Unreleased] - 2025-10-03
### Added
- Phase 3 scaffolding:
  - `src/chapter_manager.py` — per-chapter state manager (chronosense reset, tech-pulse recharge).
  - `src/boss_fight.py` — lightweight multi-phase boss engine.
  - `data/chapters.json` — canonical chapters (skeleton).
  - Placeholder scene files for CH02→CH13 in `data/scenes/`.
  - Player attributes for Chronosense & Tech Pulse (via `src/player.py`).
- UI / QoL:
  - Status bar now shows `Chronosense` uses and `TechPulse` charges.
  - Memory Cost preview now tags protected Chronicle entries with `[PROTECTED]`.
- Fixes:
  - `run_game.py` fixed to call `Game().run()` (previous import of non-existent `main`).
  - Improved memory-cost apply flow to block protected seeds and report blocked IDs.

### Changed
- Updated memory cost manager to clearly indicate protected items and prevent accidental removal.
- Minor wiring: `ChapterManager` is now optional and integrated in-game if present.

## [0.2.0] - 2025-10-03
### Added
- Richer CLI in `src/game.py`
  - Breadcrumb header
  - Status bar showing player state
  - Toast messages for feedback
  - Confirm prompts for saves/memory removal
  - Cleaner pagination and menus
- Documentation updates: README expanded with walkthrough and UX notes

### Changed
- `game.py` fully wired into Phase 2 systems (payoffs, relationships, memory costs, monster encounters)
- Save system now warns before overwriting

### Fixed
- Defensive fallbacks if `Player` or `Scene` modules are missing
- Safer loading of seeds, scenes, monsters

## [0.1.0] - Initial release
### Added
- Basic project scaffolding
- Seed/scene data loading
- Minimal player and save/load system
