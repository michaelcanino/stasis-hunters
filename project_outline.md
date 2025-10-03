# Project Outline

**Changelog**
- 

**Changelog / Version metadata (file):**
- Version: 1.0 - Date: 2025-10-03
- CHANGELOG: 

## Project vision & constraints (solo dev, console, learning OOP)
- **Target platform:** Console (terminal) text game (Windows / macOS / Linux).
- **Primary goals:** workable MVP that teaches OOP, then expand to full narrative, branching payoffs, and data-driven content.
- **Language suggestions:** Python (beginners + OOP friendly), or C# / JavaScript (Node) if preferred. (Plan is language-agnostic; examples below use Python-like pseudocode.)
- **Data approach:** All content (chapters, scenes, seeds, monsters, payoffs) driven from JSON/YAML files so narrative designers edit data instead of code. Chronicle and save flags stored as JSON save files.

---

## High-level phase list (scalable, each phase builds on previous)
- **Phase 0 — Prep & Small Prototype** (optional quick stab)
- **Phase 1 — MVP (playable core loop)**
- **Phase 2 — Core systems & branching**
- **Phase 3 — Content fill & QoL systems**
- **Phase 4 — Polishing, QA & final mechanics**
- **Phase 5 — Complete / Expansion tooling & release**

Each phase below includes deliverables, core classes/data, and scalability notes.

---

## Phase 0 — Prep & Small Prototype

**Goal:** tiny playable loop to prove the concept (1 scene, 1 seed, 1 payoff). Good for learning OOP basics.

**Deliverables**
- Minimal repo with `README`, `run_game.py`, `data/` folder.
- One scene (Festival Awakening) implemented in console.
- Implement a `Seed` pickup → mirror to `Chronicle` mechanic for a single essential seed (e.g., S05 example). 

**Core classes (start with these)**
- `Game` — main loop, scene manager, save/load hooks.
- `Player` — inventory, stats, chronosense uses, relationship map.
- `Seed` — id, description, essential_for_payoff, mirrored flag.
- `Chronicle` — container that stores protected entries.
- `Scene` — text, choices, seed placements.

**Data files**
- `data/chapters.json` (1 chapter stub), `data/seeds.json` (contains S05), data/scenes/festival.json.

**Scalability**
- Keep Scene logic separate from text assets; load scenes from JSON. Later phases will reuse loader.

---

## Phase 1 — MVP (playable core loop)

**Goal:** Implement the core gameplay loop: navigate scenes, pick seeds, simple anchor mini-game (choice/timed), mirror essential seeds, basic save/load.

**Deliverables**
- Console menu navigation (Chapter → Scene → Choice).
- Inventory and simple `Chronicle` UI (console list). Seeds flagged `essential_for_payoff` auto-mirror to Chronicle on pickup. 
- Anchor mini-game: a simple timed prompt or quick choice puzzle with three outcomes (Perfect/Partial/Fail).
- Save system (JSON) with `chronicle_entries` and `essential_seeds_found` flags. 

**Core classes / modules**
- `game.py` (Game loop, routing)
- `scene.py` (Scene loader & runtime)
- `seed.py` (Seed model + mirror logic)
- `chronicle.py` (mirroring, protections)
- `save_manager.py` (serialize/deserialize JSON)
- `mini_game.py` (anchor mini-game engine)

**Data schema (example simplified)**

```json
// data/seeds.json (example entry)
{
  "S05": {
    "id": "S05",
    "payoff": "P02",
    "desc": "Small shrine charm Hana gives Aki at the festival",
    "type": "item",
    "location": "Festival",
    "chapter": 1,
    "discover_method": "pickup",
    "essential_for_payoff": true
  }
}
```

**Milestones**
- Run through at least 3 scenes, picking up one essential and one optional seed. Confirm Chronicles are protected in save file.

---

## Recommended OOP design (simple class overview + responsibilities)

**Top-level**
```
Game
  - start()
  - load_save()
  - save()
  - run_scene(scene_id)

Scene
  - id, text_blocks, choices[], seeds[]
  - render()
  - apply_choice(choice_id)

Player
  - name, inventory, stats, relationships, chronosense_uses

Seed
  - id, desc, essential_for_payoff, mirrored (bool)
  - on_pickup(player): mirror if essential -> Chronicle

Chronicle
  - entries: map(seed_id -> entry)
  - add(seed): enforce protected flag; write_once semantics

PayoffManager
  - payoffs (loaded from JSON)
  - can_trigger(payoff_id, save_state)
  - trigger(payoff_id)
```

**Notes**
- Keep data model small and pass objects around by reference (or ID lookups).
- Favor composition: `Scene` contains `Choice` objects, each `Choice` may call `effects` (add seed, change relationship, start mini-game).

---

## Data-driven formats (templates you should create early)

**Payoff (JSON)**
```json
{
  "P01": {
    "id": "P01",
    "title": "Corporate Corruption Exposed",
    "required_seeds": ["S01","S03","S22"],
    "canonical": true,
    "chapter_trigger": 12
  }
}
```

**Seed (JSON)** — (expand fields from doc)
```json
{
  "S22": {
    "id": "S22",
    "payoff": "P01",
    "desc": "Reliquary core fragment with partial board signatures",
    "location": "Reliquary Vault",
    "chapter": 12,
    "discover_method": "pickup",
    "essential_for_payoff": true,
    "mirror_on_pickup": true
  }
}
```

**Save file sample**
```json
{
  "player": { "name":"Aki", "inventory":[], "relationships":{} },
  "chronicle_entries": ["S10", "S22"],
  "flags": {
    "flag_seed_S22_found": true,
    "flag_seed_S22_mirrored_to_chronicle": true,
    "flag_romance_multi_punishment_triggered": false
  },
  "current_chapter": 3
}
```
---

## Console UX patterns & tips
- Paginate long text: show `-- more --` prompts every ~6–8 lines.
- Choice input: numeric menu (1,2,3). Accept `q` for quit, `s` for save.
- Toasts: print short prefixed messages like `[TOAST] You lost 1 Memory Fragment: Romantic Credibility.` (doc specifies this behavior). 
- Chronicle display: list with `[PROTECTED]` badge for items mirrored to Chronicle.

---

## QA checklist (copy items from doc + actionable tests)
- Implement the per-payoff QA tests from the doc (P01..P05, RomancePunish) as automated or manual test scripts (set flags to simulate found/missed seeds). 
- Tests to include:
    - Acquire S22 via mid-boss -> verify `chronicle_entries` receives S22 and payoffs unlock. 
    - Attempt Memory Cost that would remove a protected seed -> blocked and message shown. 
    - Festival multi-romance path triggers S21 gag and applies the downgrade, journal note, and flags.

---

## Example: Chronicle mirror pseudocode (safe, simple)
```python
def pickup_seed(seed_id, player, save_state):
    seed = load_seed(seed_id)
    player.inventory.append(seed_id)
    save_state['flags'][f'flag_seed_{seed_id}_found'] = True
    if seed['essential_for_payoff'] or seed.get('mirror_on_pickup'):
        # mirror to chronicle
        if seed_id not in save_state['chronicle_entries']:
            save_state['chronicle_entries'].append(seed_id)
            save_state['flags'][f'flag_seed_{seed_id}_mirrored_to_chronicle'] = True
            print("[CHRONICLE] Protected in Chronicle — cannot be removed.")
```

This follows the doc directive: mirror essential seeds to Chronicle, `protected: true`, `write_once`.

---
## Learning / OOP progression plan (for the solo dev)
- Start Phase 0/1 to learn classes, objects, and serialization.
- When confident, add modules (Phase 2): relationships, event system (publish/subscribe), and tests.
- By Phase 3 you'll be using composition, dependency injection (pass managers into `Game`), and data modeling.
- Add unit tests for `seed` logic, `payoff_manager`, and `chronicle` protection.

---

## Final checklist before full content writing
- [ ] Pick Engine Heart canonical placement (Ch11 recommended) and set `game_config.json`. 
- [ ] Confirm which seeds must be `essential_for_payoff: true` (doc currently marks S22 & S23 essential). 
- [ ] Implement fallback enforcement for early seeds (ensure midpoints expose fallbacks). 
- [ ] Copy QA tests into a `QA/` folder as runnable scripts or checklists (so playtesters can reproduce edge cases).

---

## Appendix — Useful file / folder structure (suggested)

```
/stasis-hunters/
  README.md
  run_game.py
  game_config.json
  /src/
    game.py
    scene.py
    player.py
    seed.py
    chronicle.py
    payoff_manager.py
    monster.py
    save_manager.py
    ui_helpers.py
  /data/
    chapters.json
    seeds.json
    payoffs.json
    monsters.json
    scenes/
      festival.json
      recruitment.json
      ...
  /saves/
  /docs/
    QA_checklists.md
    design_notes.md
  /tools/
    seed_editor.py
    playtest_helpers.py
```