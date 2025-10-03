# src/save_manager.py
import json
import os
from typing import Dict

class SaveManager:
    def __init__(self, save_path="saves/save.json"):
        self.save_path = save_path
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

    def save(self, player, extra=None):
        state = {
            "player": {
                "name": player.name,
                "inventory": [{"id": s['id'], "desc": s.get('desc','')} for s in player.inventory],
                "relationships": player.relationships
            },
            "chronicle_entries": player.chronicle.entries
        }
        if extra:
            state.update(extra)
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        print(f"\n[SaveManager] Game saved to {self.save_path}")

    def load(self):
        if not os.path.exists(self.save_path):
            print("[SaveManager] No save found.")
            return None
        with open(self.save_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        print(f"[SaveManager] Loaded save from {self.save_path}")
        return state
