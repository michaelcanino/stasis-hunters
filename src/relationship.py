# src/relationship.py
from typing import Dict, List

class RelationshipManager:
    """
    Affinity/romance manager.
    - affinities: name -> int
    - romance_flags: name -> bool
    Behavior:
    - change_affinity updates current affinity and auto-sets romance flag
      when affinity >= ROMANCE_THRESHOLD, and clears it when affinity drops.
    Note: more complex rebuild/lock rules should be enforced by Game using
    player.flags (e.g. romance_rebuild_cost, flag_romance_locked_until_rebuild).
    """
    ROMANCE_THRESHOLD = 5

    def __init__(self, affinities: Dict[str, int] = None, romance_flags: Dict[str, bool] = None):
        self.affinities = affinities if affinities is not None else {}
        self.romance_flags = romance_flags if romance_flags is not None else {}

    def change_affinity(self, npc_name: str, delta: int, player_flags: Dict = None) -> int:
        """
        Adjust affinity by delta and manage romance flags.

        :param npc_name: str
        :param delta: int
        :param player_flags: optional dict (player.flags) so special constraints
                             (like 'flag_romance_locked_until_rebuild') can be checked.
        :returns: new affinity value
        """
        cur = self.affinities.get(npc_name, 0) + delta
        self.affinities[npc_name] = cur

        # Check any external lock (Game may set this flag)
        locked = False
        if isinstance(player_flags, dict):
            locked = player_flags.get("flag_romance_locked_until_rebuild", False)

        # If affinity crosses threshold, set romance (unless locked)
        if cur >= self.ROMANCE_THRESHOLD and not locked:
            if not self.romance_flags.get(npc_name, False):
                self.romance_flags[npc_name] = True
                print(f"[Relationship] {npc_name} reached romance threshold (affinity={cur}). Romance flag set.")
        else:
            # falling below threshold clears romance flag (keep simple)
            if self.romance_flags.get(npc_name, False) and cur < self.ROMANCE_THRESHOLD:
                self.romance_flags[npc_name] = False
                print(f"[Relationship] {npc_name} romance cleared (affinity={cur}).")

        return cur

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
