# src/relationship.py
from typing import Dict, List

class RelationshipManager:
    """
    Simple affinity manager. Stores affinities and romance flags.
    Thresholds are intentionally small for easier testing; tweak as needed.
    """
    ROMANCE_THRESHOLD = 5

    def __init__(self, affinities: Dict[str, int]=None, romance_flags: Dict[str, bool]=None):
        self.affinities = affinities if affinities is not None else {}
        self.romance_flags = romance_flags if romance_flags is not None else {}

    def change_affinity(self, npc_name: str, delta: int):
        cur = self.affinities.get(npc_name, 0) + delta
        self.affinities[npc_name] = cur
        print(f"[Relation] {npc_name} affinity -> {cur}")
        if cur >= self.ROMANCE_THRESHOLD and not self.romance_flags.get(npc_name, False):
            self.romance_flags[npc_name] = True
            print(f"[Relation] {npc_name} romance flag SET.")

    def get_affinity(self, npc_name: str) -> int:
        return self.affinities.get(npc_name, 0)

    def get_romances(self) -> List[str]:
        return [n for n, v in self.romance_flags.items() if v]

    def to_dict(self) -> Dict:
        return {"affinities": self.affinities, "romance_flags": self.romance_flags}

    @classmethod
    def from_player_data(cls, player_data: Dict):
        affin = player_data.get("relationships", {})
        romance = player_data.get("romance_flags", {})
        return cls(affinities=affin, romance_flags=romance)
