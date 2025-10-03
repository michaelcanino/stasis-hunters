# tools/auto_playtest.py
"""
Auto playtest script to ensure milestone:
- Run through at least 3 scenes
- Pick up one optional seed (S05) and one essential seed (S22)
- Save the game
- Confirm chronicle entries are present and that the save's signature verifies
"""

import os
import sys
import json
import pathlib

# Ensure repo root is on path so we can import src modules
HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
sys.path.insert(0, str(REPO_ROOT))

# Import the project modules
from src.game import Game
from src.scene import Scene

def run_playtest():
    print("== Auto Playtest: Start ==")
    g = Game()

    # Scenes to visit (3 scenes)
    scenes_to_visit = ["festival", "relic_cave", "abandoned_lab"]

    # Actions to take per scene: map scene_id -> list of 1-based choice indices to perform
    # We'll pick:
    # - festival: choice 1 -> pickup S05 (optional)
    # - relic_cave: choice 1 -> pickup S22 (essential)
    # - abandoned_lab: choice 1 -> pickup S99 (optional)
    actions = {
        "festival": [1],
        "relic_cave": [1],
        "abandoned_lab": [1]
    }

    for sid in scenes_to_visit:
        sc_data = g.scenes_index.get(sid)
        if not sc_data:
            print(f"[Test] Scene '{sid}' missing in data. FAIL")
            return False
        scene = Scene(sc_data, g.seeds_index)
        print(f"\n[Test] Visiting scene: {scene.title} ({scene.id})")
        # perform requested choices
        picks = actions.get(sid, [])
        for pick in picks:
            print(f"[Test] Performing choice {pick} in scene {sid}")
            scene.perform_choice(pick, g.player)

    # After interactions, check player inventory and chronicle
    inv_ids = [s['id'] for s in g.player.inventory]
    chr_ids = [e['id'] for e in g.player.chronicle.entries]

    print("\n[Test] Inventory contains:", inv_ids)
    print("[Test] Chronicle entries:", chr_ids)

    # Basic assertions:
    have_optional = "S05" in inv_ids
    have_essential = "S22" in inv_ids
    chronicle_has_essential = "S22" in chr_ids or any(e.get("id") == "S22" for e in g.player.chronicle.entries)

    if not have_optional:
        print("[Test] Missing optional seed S05 in inventory. FAIL")
        return False
    if not have_essential:
        print("[Test] Missing essential seed S22 in inventory. FAIL")
        return False
    if not chronicle_has_essential:
        print("[Test] Chronicle does not include essential seed S22. FAIL")
        return False

    # Save the game using SaveManager (the Game instance contains save_manager)
    g.save_manager.save(g.player, extra={"test_run": True})

    # Now load and verify via load_and_verify (which returns (ok, protected_payload))
    ok, protected = g.save_manager.load_and_verify()
    if not ok:
        print("[Test] Save signature verification failed. FAIL")
        return False

    # Confirm chronicle_entries preserved in protected payload
    saved_chron = protected.get("chronicle_entries", [])
    saved_inv = [s.get("id") for s in protected.get("player", {}).get("inventory", [])]

    print("[Test] Saved chronicle entries:", [e.get("id") for e in saved_chron])
    print("[Test] Saved inventory ids:", saved_inv)

    # Check expected entries in saved file
    if "S22" not in [e.get("id") for e in saved_chron]:
        print("[Test] Essential seed S22 not present in saved chronicle_entries. FAIL")
        return False
    if "S05" not in saved_inv:
        print("[Test] Optional seed S05 not present in saved inventory. FAIL")
        return False

    print("\n== Auto Playtest: PASS ==")
    return True

if __name__ == "__main__":
    ok = run_playtest()
    if not ok:
        sys.exit(2)
    else:
        sys.exit(0)
