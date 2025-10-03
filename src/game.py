# src/game.py
import json
import os
from .player import Player
from .scene import Scene
from .save_manager import SaveManager

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_DIR = os.path.normpath(DATA_DIR)

class Game:
    def __init__(self):
        self.player = Player()
        self.save_manager = SaveManager(save_path="saves/save.json")
        # load seeds and scenes
        self.seeds = self._load_json("seeds.json")
        self.scenes = self._load_json("scenes.json")
        # index seeds by id
        self.seeds_index = {s['id']: s for s in self.seeds}
        # index scenes by id
        self.scenes_index = {sc['id']: sc for sc in self.scenes}
        # Here we can add chapters mapping (simple)
        self.chapters = [{"id": "chap1", "title": "Chapter 1: Festival", "scenes": ["festival", "relic_cave"]}]

    def _load_json(self, filename):
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            print(f"[Game] Missing data file: {path}")
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def main_menu(self):
        while True:
            print("\n=== Main Menu ===")
            print("1. Chapters")
            print("2. Inventory")
            print("3. Chronicle")
            print("4. Save")
            print("5. Load")
            print("6. Quit")
            c = input("> ").strip()
            if c == "1":
                self.chapter_menu()
            elif c == "2":
                self.player.show_inventory()
            elif c == "3":
                self.player.chronicle.list_entries()
            elif c == "4":
                self.save_manager.save(self.player)
            elif c == "5":
                self._load_game_into_player()
            elif c == "6":
                print("Bye.")
                break
            else:
                print("Unknown option.")

    def chapter_menu(self):
        print("\n=== Chapters ===")
        for i, ch in enumerate(self.chapters, 1):
            print(f"{i}. {ch['title']}")
        print(f"{len(self.chapters)+1}. Back")
        c = input("> ").strip()
        try:
            ci = int(c)
        except:
            return
        if ci < 1 or ci > len(self.chapters):
            return
        chapter = self.chapters[ci-1]
        self.scene_menu(chapter)

    def scene_menu(self, chapter):
        while True:
            print(f"\n=== {chapter['title']} ===")
            for i, sid in enumerate(chapter['scenes'], 1):
                sc = self.scenes_index.get(sid, {"title": sid})
                print(f"{i}. {sc.get('title','(untitled)')}")
            print(f"{len(chapter['scenes'])+1}. Back")
            c = input("> ").strip()
            try:
                ci = int(c)
            except:
                continue
            if ci == len(chapter['scenes']) + 1:
                break
            if 1 <= ci <= len(chapter['scenes']):
                sid = chapter['scenes'][ci-1]
                sc_data = self.scenes_index.get(sid)
                if not sc_data:
                    print("[Game] Scene missing.")
                    continue
                scene = Scene(sc_data, self.seeds_index)
                self.run_scene(scene)

    def run_scene(self, scene):
        while True:
            scene.show()
            try:
                pick = int(input("> ").strip())
            except:
                print("Enter a number.")
                continue
            if pick == len(scene.choices) + 1:
                break
            scene.perform_choice(pick, self.player)

    def _load_game_into_player(self):
        state = self.save_manager.load()
        if not state:
            return
        p = state.get("player", {})
        self.player.name = p.get("name", self.player.name)
        inv = p.get("inventory", [])
        # map inventory entries back to seed objects if possible (best-effort)
        self.player.inventory.clear()
        for entry in inv:
            sid = entry.get("id")
            seed = self.seeds_index.get(sid, {"id": sid, "desc": entry.get("desc","")})
            self.player.inventory.append(seed)
        # chronicle
        self.player.chronicle.entries = state.get("chronicle_entries", [])
        print("[Game] Save loaded into player.")

def run():
    g = Game()
    g.main_menu()

if __name__ == "__main__":
    run()
