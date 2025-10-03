# src/player.py
from typing import List, Dict
from .chronicle import Chronicle

class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.inventory: List[Dict] = []      # list of seed dicts (id, desc, ...)
        self.relationships = {}
        self.chronicle = Chronicle()
        self.flags = {}   # storage for arbitrary flags (e.g. triggered payoffs)

        # Phase 3 additions:
        self.chronosense_uses_remaining = 0
        self.tech_pulse = 0
        self.tech_pulse_max = 3

    def add_seed(self, seed):
        # seed: dict with id, desc, essential_for_payoff, mirror_on_pickup
        if any(s['id'] == seed['id'] for s in self.inventory):
            print(f"[Inventory] Seed {seed['id']} already in inventory.")
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

    def to_dict(self):
        return {
            'name': self.name,
            'inventory': self.inventory,
            'chronicle': getattr(self.chronicle, 'entries', []),
            'relationships': self.relationships,
            'flags': self.flags,
            'chronosense_uses_remaining': self.chronosense_uses_remaining,
            'tech_pulse': self.tech_pulse,
            'tech_pulse_max': self.tech_pulse_max
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(name=data.get('name','Player'))
        p.inventory = data.get('inventory', [])
        p.chronicle.entries = data.get('chronicle', [])
        p.relationships = data.get('relationships', {})
        p.flags = data.get('flags', {})
        p.chronosense_uses_remaining = data.get('chronosense_uses_remaining', 0)
        p.tech_pulse = data.get('tech_pulse', 0)
        p.tech_pulse_max = data.get('tech_pulse_max', 3)
        return p
