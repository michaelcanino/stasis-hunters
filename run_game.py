import json
import os

# ---------- Data loading helpers ----------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- Models ----------
class Seed:
    def __init__(self, data):
        self.id = data["id"]
        self.desc = data["desc"]
        self.essential = data["essential_for_payoff"]
        self.mirror_on_pickup = data.get("mirror_on_pickup", False)

class Chronicle:
    def __init__(self):
        self.entries = []

    def add(self, seed: Seed):
        if seed.id not in self.entries:
            self.entries.append(seed.id)
            print(f"[CHRONICLE] {seed.desc} (protected).")

class Player:
    def __init__(self, name="Aki"):
        self.name = name
        self.inventory = []
        self.relationships = {}
        self.chronicle = Chronicle()

    def pickup_seed(self, seed: Seed):
        print(f"You obtained: {seed.desc}")
        self.inventory.append(seed.id)
        if seed.essential or seed.mirror_on_pickup:
            self.chronicle.add(seed)

# ---------- Game runtime ----------
class Game:
    def __init__(self):
        self.seeds = load_json("data/seeds.json")
        self.scenes = {"festival": load_json("data/scenes/festival.json")}
        self.player = Player()
        self.save_path = "saves/save1.json"
        os.makedirs("saves", exist_ok=True)

    def run_scene(self, scene_id):
        scene = self.scenes[scene_id]
        print(f"\n== {scene['title']} ==")
        for line in scene["text"]:
            print(line)

        for idx, choice in enumerate(scene["choices"], start=1):
            print(f"{idx}. {choice['text']}")

        while True:
            try:
                sel = int(input("> "))
                if 1 <= sel <= len(scene["choices"]):
                    break
            except ValueError:
                pass
            print("Invalid input, try again.")

        chosen = scene["choices"][sel - 1]
        effects = chosen["effects"]

        # Apply effects
        if "add_seed" in effects:
            seed_id = effects["add_seed"]
            seed = Seed(self.seeds[seed_id])
            self.player.pickup_seed(seed)

        if "relationship" in effects:
            for char, delta in effects["relationship"].items():
                self.player.relationships[char] = (
                    self.player.relationships.get(char, 0) + delta
                )
                print(f"[REL] {char} affinity: {self.player.relationships[char]}")

        self.save_game()

    def save_game(self):
        save_state = {
            "player": {
                "name": self.player.name,
                "inventory": self.player.inventory,
                "relationships": self.player.relationships
            },
            "chronicle_entries": self.player.chronicle.entries
        }
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(save_state, f, indent=2)
        print(f"\n[Game Saved] -> {self.save_path}")

# ---------- Entrypoint ----------
if __name__ == "__main__":
    game = Game()
    game.run_scene("festival")
