# src/player.py
from typing import List, Dict
from .chronicle import Chronicle

class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.inventory: List[Dict] = []      # list of seed dicts (id, desc, ...)
        self.relationships = {}
        self.chronicle = Chronicle()

    def add_seed(self, seed):
        # seed: dict with id, desc, essential_for_payoff, mirror_on_pickup
        if any(s['id'] == seed['id'] for s in self.inventory):
            print(f"[Inventory] {seed['id']} already collected.")
            return False
        self.inventory.append(seed)
        print(f"[Inventory] Picked up seed {seed['id']}.")
        if seed.get("mirror_on_pickup") or seed.get("essential_for_payoff"):
            # mirror essential or flagged seeds
            self.chronicle.add_entry(seed)
        return True

    def show_inventory(self):
        if not self.inventory:
            print("\n[Inventory] Empty.")
            return
        print("\n--- Inventory ---")
        for s in self.inventory:
            print(f"{s['id']}: {s.get('desc','(no desc)')}")
        print("-----------------")
