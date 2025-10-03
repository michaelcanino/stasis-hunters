# src/chronicle.py
from typing import List, Dict

class Chronicle:
    """Stores mirrored lore entries (seeds that matter)."""
    def __init__(self):
        self.entries: List[Dict] = []

    def add_entry(self, seed):
        # seed is a dict-like with id and desc
        existing = any(e['id'] == seed['id'] for e in self.entries)
        if not existing:
            self.entries.append({"id": seed['id'], "desc": seed.get('desc', '')})
            print(f"\n[Chronicle] Mirrored seed {seed['id']}: added to Chronicle.")
        else:
            print(f"\n[Chronicle] {seed['id']} already in Chronicle.")

    def list_entries(self):
        if not self.entries:
            print("\n[Chronicle] No entries yet.")
            return
        print("\n--- Chronicle ---")
        for e in self.entries:
            print(f"{e['id']}: {e['desc']}")
        print("-----------------")
