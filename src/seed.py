# src/seed.py
from typing import Dict

class Seed:
    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.desc = data.get("desc", "")
        self.essential_for_payoff = data.get("essential_for_payoff", False)
        self.mirror_on_pickup = data.get("mirror_on_pickup", False)

    def to_dict(self) -> Dict:
        return {"id": self.id, "desc": self.desc,
                "essential_for_payoff": self.essential_for_payoff,
                "mirror_on_pickup": self.mirror_on_pickup}
