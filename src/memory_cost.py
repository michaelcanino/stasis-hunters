# src/memory_cost.py
from typing import List, Dict

class MemoryCostManager:
    """
    Presents a preview of removable fragments and applies removals.
    Protected seeds (mirrored to Chronicle) cannot be removed.
    """

    def __init__(self, player):
        self.player = player

    def preview_removable(self) -> List[Dict]:
        chronicle_ids = {e['id'] for e in self.player.chronicle.entries}
        removable = [s for s in self.player.inventory if s.get("id") not in chronicle_ids]
        print("[MemoryCost] Preview removable fragments:")
        for s in removable:
            print(f" - {s.get('id')}: {s.get('desc','')}")
        return removable

    def apply_removal(self, remove_ids: List[str]) -> Dict:
        chronicle_ids = {e['id'] for e in self.player.chronicle.entries}
        removed = []
        blocked = []
        new_inventory = []
        for s in self.player.inventory:
            sid = s.get("id")
            if sid in remove_ids:
                if sid in chronicle_ids:
                    blocked.append(sid)
                else:
                    removed.append(sid)
                    continue
            new_inventory.append(s)
        self.player.inventory = new_inventory
        print(f"[MemoryCost] Removed: {removed}; Blocked: {blocked}")
        return {"removed": removed, "blocked": blocked, "remaining_count": len(self.player.inventory)}
