
---

### CHANGELOG.md (updated contents)

```markdown
# Changelog

## [Unreleased]
- Phase 3 roadmap: combat refinement, advanced payoff chaining, UI/TUI experiments

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
