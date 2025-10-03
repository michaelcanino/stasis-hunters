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
        """
        Print inventory with removable/protected marking and return removable list.
        """
        chronicle_ids = {e['id'] for e in self.player.chronicle.entries}
        print("\n[MemoryCost] Inventory preview (protected items are tagged):")
        lines = []
        removable = []
        for s in self.player.inventory:
            sid = s.get("id")
            tag = "[PROTECTED]" if sid in chronicle_ids else ""
            lines.append(f"{sid}: {s.get('desc','(no desc)')} {tag}")
            if sid not in chronicle_ids:
                removable.append(s)
        for l in lines:
            print(l)
        if not removable:
            print("[MemoryCost] No removable fragments (all protected or none present).")
        else:
            print(f"[MemoryCost] Removable fragments: {', '.join([r['id'] for r in removable])}")
        return removable

    def apply_removal(self, remove_ids: List[str]) -> Dict:
        """
        Attempt to remove items by id. Protected items (mirrored to Chronicle) will be blocked.
        Returns dict: removed, blocked, remaining_count
        """
        chronicle_ids = {e['id'] for e in self.player.chronicle.entries}
        removed = []
        blocked = []
        new_inventory = []
        remove_set = set(remove_ids or [])
        for s in self.player.inventory:
            sid = s.get("id")
            if sid in remove_set:
                if sid in chronicle_ids:
                    blocked.append(sid)
                    new_inventory.append(s)  # keep it
                else:
                    removed.append(sid)
                    # skip adding -> removed
            else:
                new_inventory.append(s)
        self.player.inventory = new_inventory
        print(f"[MemoryCost] Removed: {removed}; Blocked (protected): {blocked}")
        return {"removed": removed, "blocked": blocked, "remaining_count": len(self.player.inventory)}
