# src/boss_fight.py
import random
from typing import Dict, List

class BossFight:
    """
    Lightweight multi-phase boss engine.
    Input: boss_data dict (id, name, phases, drops)
    Returns: list of seed_ids dropped
    """

    def __init__(self, boss_data: Dict):
        self.id = boss_data.get("id")
        self.name = boss_data.get("name", "Boss")
        self.phases = boss_data.get("phases", [{"hp": 60}, {"hp": 80}])
        self.drops = boss_data.get("drops", [])

    def fight(self, player) -> List[str]:
        print(f"\n[BossFight] Confronting boss: {self.name}\n")
        for phase_i, phase in enumerate(self.phases, start=1):
            hp = int(phase.get("hp", 50))
            print(f"[BossFight] Phase {phase_i} begins. Boss HP: {hp}")
            while hp > 0:
                print("1) Attack  2) Guard  3) Use Tech Pulse  4) Try to Retreat")
                choice = input("> ").strip()
                if choice == "1":
                    dmg = random.randint(8, 18)
                    print(f"[Action] You attack for {dmg} damage.")
                    hp -= dmg
                    if hp <= 0:
                        print("[BossFight] Phase cleared.")
                        break
                elif choice == "2":
                    print("[Action] You guard. Boss attack less effective.")
                    # slight effect simulated by extending loop (no player HP model here)
                elif choice == "3":
                    # attempt to use tech pulse if available
                    tp = getattr(player, "tech_pulse", 0)
                    if tp > 0:
                        player.tech_pulse = tp - 1
                        effect = random.randint(20, 35)
                        print(f"[TechPulse] Powerful strike! deals {effect} hp.")
                        hp -= effect
                        if hp <= 0:
                            print("[BossFight] Phase cleared.")
                            break
                    else:
                        print("[TechPulse] No Tech Pulse charges available.")
                elif choice == "4":
                    if random.random() < 0.4:
                        print("[BossFight] You escaped.")
                        return []
                    else:
                        print("[BossFight] Failed to escape.")
                else:
                    print("Invalid choice.")
            # small pause between phases
            print(f"[BossFight] Phase {phase_i} complete.\n")
        if self.drops:
            print(f"[BossFight] Boss defeated! Drops: {self.drops}")
        else:
            print("[BossFight] Boss defeated! No drops.")
        return list(self.drops)
