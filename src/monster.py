# src/monster.py
import random
from typing import Dict, List

class Monster:
    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.name = data.get("name", "Monster")
        self.max_hp = data.get("hp", 30)
        self.hp = self.max_hp
        self.attack_pattern = data.get("attack_pattern", ["bash"])
        self.drops = data.get("drops", [])

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)
        print(f"[Combat] {self.name} takes {amount} dmg (HP: {self.hp}/{self.max_hp})")

    def enemy_attack(self, player):
        # simple damage roll (flavor only—player HP system can be added later)
        dmg = random.randint(3, 8)
        print(f"[Combat] {self.name} attacks for {dmg} (flavor only).")

    def fight(self, player):
        """
        Very small deterministic loop for console testing.
        Returns list of drop ids if monster defeated.
        """
        print(f"[Encounter] You engage {self.name} (HP {self.max_hp}).")
        while self.is_alive():
            print("1) Attack  2) Try to Run")
            choice = input("> ").strip()
            if choice == "1":
                dmg = random.randint(6, 12)
                self.take_damage(dmg)
                if not self.is_alive():
                    print(f"[Combat] You defeated {self.name}!")
                    return list(self.drops)
                self.enemy_attack(player)
            elif choice == "2":
                # small chance to flee
                if random.random() < 0.5:
                    print("[Combat] You successfully fled.")
                    return []
                else:
                    print("[Combat] Failed to flee.")
                    self.enemy_attack(player)
            else:
                print("[Combat] Invalid choice.")
        return list(self.drops)
