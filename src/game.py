# src/game.py
"""
Richer-CLI Game runner for Stasis Hunters — Phase 2 integrated.

Features:
 - Breadcrumb header + status bar (player name, inventory/chronicle counts)
 - Toast messages (console boxed notices)
 - Confirm prompts for destructive actions
 - Improved pagination and menus with shortcuts
 - Defensive fallbacks so it runs if some modules are missing

Drop into stasis-hunters/src/game.py (overwrite) and run from project root:
    python -m src.game
"""
import os
import json
import glob
import time
from typing import Dict, Any
from datetime import datetime

# ANSI helpers (works in most terminals; harmless if terminal ignores)
CSI = "\x1b["
RESET = CSI + "0m"
BOLD = CSI + "1m"
DIM = CSI + "2m"
UNDER = CSI + "4m"
GREEN = CSI + "32m"
YELLOW = CSI + "33m"
RED = CSI + "31m"
BLUE = CSI + "34m"
CYAN = CSI + "36m"

# Defensive imports (handles missing modules more gracefully)
try:
    from .player import Player
except Exception:
    Player = None

try:
    from .scene import Scene
except Exception:
    Scene = None

try:
    from .payoff_manager import PayoffManager
except Exception:
    PayoffManager = None

try:
    from .relationship import RelationshipManager
except Exception:
    RelationshipManager = None

try:
    from .memory_cost import MemoryCostManager
except Exception:
    MemoryCostManager = None

try:
    from .chapter_manager import ChapterManager
except Exception:
    ChapterManager = None

try:
    from .boss_fight import BossFight
except Exception:
    BossFight = None


try:
    from .ui_helpers import paginate_lines as ui_paginate, choice_menu as ui_choice_menu
except Exception:
    ui_paginate = None
    ui_choice_menu = None


# -------------------- UI Utilities --------------------
def clear_screen():
    # Simple clear - works on Windows and *nix shells
    os.system('cls' if os.name == 'nt' else 'clear')


def toast(msg: str, title: str = "NOTICE", wait: float = 0.8):
    """Pretty boxed toast message. Non-blocking aside from short wait."""
    lines = msg.splitlines() or [msg]
    width = max(len(l) for l in lines) + 4
    border = "+" + "-" * width + "+"
    print(CYAN + border)
    print(f"| {title.center(width - 2)} |")
    print("|" + "-" * width + "|")
    for l in lines:
        print("| " + l.ljust(width - 2) + " |")
    print(border + RESET)
    # short pause to mimic ephemeral toast (tweakable)
    time.sleep(wait)


def status_bar(player) -> str:
    name = getattr(player, "name", "Player")
    inv_count = len(getattr(player, "inventory", []))
    chron = len(getattr(player.chronicle, "entries", [])) if hasattr(player, "chronicle") else 0

    pieces = [f"{BOLD}{name}{RESET}", f"Inv: {inv_count}", f"Chronicle: {chron}"]

    cs = getattr(player, "chronosense_uses_remaining", None)
    if cs is not None:
        pieces.append(f"Chronosense: {cs}")

    tp = getattr(player, "tech_pulse", None)
    if tp is not None:
        tp_max = getattr(player, "tech_pulse_max", tp)
        pieces.append(f"TechPulse: {tp}/{tp_max}")

    return "  |  ".join(pieces)



def heading(text: str):
    print(BOLD + text + RESET)


def confirm(prompt: str, default: bool = False) -> bool:
    yes = "Y" if default else "y"
    no = "n" if default else "N"
    s = f"{prompt} [{yes}/{no}]: "
    while True:
        r = input(s).strip().lower()
        if r == "" and default:
            return True
        if r == "" and not default:
            return False
        if r in ("y", "yes"):
            return True
        if r in ("n", "no"):
            return False
        print("Please answer y or n.")


def paginate_lines(lines, page_size=6):
    """Fallback paginator - prints a heading and pages through."""
    if not lines:
        print("(none)")
        return
    for i in range(0, len(lines), page_size):
        clear_screen()
        for l in lines[i:i + page_size]:
            print(l)
        if i + page_size < len(lines):
            inp = input("-- more -- (Enter to continue, q to quit) -- ").strip().lower()
            if inp == 'q':
                break


def choice_menu(options):
    """Fallback choice menu. options = list of (key, text). returns chosen key or control codes."""
    for idx, (key, text) in enumerate(options, start=1):
        print(f"{idx}) {text}")
    print("q) quit  s) save  m) main menu")
    while True:
        c = input("> ").strip().lower()
        if c in ("q", "s", "m"):
            return c
        try:
            i = int(c)
            if 1 <= i <= len(options):
                return options[i - 1][0]
        except Exception:
            pass
        print("Invalid choice.")


# Choose which helpers to use (prefer project's ui_helpers if available)
paginate = ui_paginate if ui_paginate else paginate_lines
menu_choice = ui_choice_menu if ui_choice_menu else choice_menu


# -------------------- Minimal Player Fallback --------------------
class MinimalPlayer:
    """Fallback player if src/player.py is missing. Lightweight and JSON serializable."""
    def __init__(self, name="Player"):
        self.name = name
        self.inventory = []     # list of seed dicts
        self.chronicle = type('C', (), {'entries': []})()
        self.relationships = {}
        self.flags = {}

    def add_seed(self, seed_dict: Dict[str, Any]):
        self.inventory.append(seed_dict)
        # Mirror if seed declares mirror_on_pickup
        if seed_dict.get('mirror_on_pickup'):
            self.chronicle.entries.append({'id': seed_dict.get('id'), 'desc': seed_dict.get('desc')})

    def to_dict(self):
        return {
            'name': getattr(self, 'name', 'Player'),
            'inventory': self.inventory,
            'chronicle': getattr(self.chronicle, 'entries', []),
            'relationships': self.relationships,
            'flags': self.flags,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        p = cls(name=data.get('name', 'Player'))
        p.inventory = data.get('inventory', [])
        p.chronicle.entries = data.get('chronicle', [])
        p.relationships = data.get('relationships', {})
        p.flags = data.get('flags', {})
        return p


# -------------------- Game --------------------
class Game:
    def __init__(self):
        self.root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
        self.data_dir = os.path.join(self.root, 'data')
        self.saves_dir = os.path.join(self.root, 'saves')
        os.makedirs(self.saves_dir, exist_ok=True)

        # content indexes
        self.seeds_index = self._load_json_index('seeds.json', key_field='id')
        self.scenes_index = self._load_scenes(os.path.join(self.data_dir, 'scenes'))
        self.monsters_index = self._load_json_index('monsters.json', key_field='id')

        # Managers
        self.payoff_manager = PayoffManager(self.data_dir) if PayoffManager else None
        self.relationship_manager = RelationshipManager() if RelationshipManager else None
        self.memory_manager = None  # created after player exists

        # Player
        if Player:
            try:
                self.player = Player()
            except Exception:
                self.player = MinimalPlayer()
        else:
            self.player = MinimalPlayer()

        # Chapter manager (Phase 3)
        self.chapter_manager = ChapterManager(self.data_dir, player=self.player) if ChapterManager else None
        # Optional boss helper
        self.boss_fight_helper = BossFight if BossFight else None

        # ensure flags container exists
        if not hasattr(self.player, 'flags'):
            self.player.flags = {}

        # memory manager requires player
        self.memory_manager = MemoryCostManager(self.player) if MemoryCostManager else None

        # wire seeds_index into scene objects
        for sid, scene in self.scenes_index.items():
            if hasattr(scene, 'seeds_index'):
                scene.seeds_index = self.seeds_index

        # UI state
        self.breadcrumb = ["Main Menu"]
        # small welcome toast
        toast("Phase 2 systems active (payoffs, relationships, memory cost, monsters).", "Welcome", wait=0.6)

    # --------------------- Loading helpers ---------------------
    def _load_json_index(self, filename, key_field='id'):
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                arr = json.load(f)
                if isinstance(arr, dict):
                    return arr
                idx = {}
                for item in arr:
                    key = item.get(key_field)
                    if key:
                        idx[key] = item
                return idx
        except Exception as e:
            print(f"[Game] Failed to load {filename}: {e}")
            return {}

    def _load_scenes(self, scenes_dir):
        scenes = {}
        if not os.path.isdir(scenes_dir):
            return scenes
        for fpath in glob.glob(os.path.join(scenes_dir, '*.json')):
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sid = data.get('id') or os.path.splitext(os.path.basename(fpath))[0]
                    if Scene:
                        try:
                            scene_obj = Scene(data)
                            setattr(scene_obj, 'seeds_index', self.seeds_index)
                            scenes[sid] = scene_obj
                        except Exception:
                            scenes[sid] = data
                    else:
                        scenes[sid] = data
            except Exception as e:
                print(f"[Game] Failed to load scene {fpath}: {e}")
        return scenes

    # --------------------- Save / Load ---------------------
    def _save_payload(self):
        if hasattr(self.player, 'to_dict'):
            payload = self.player.to_dict()
        else:
            payload = {
                'name': getattr(self.player, 'name', 'Player'),
                'inventory': getattr(self.player, 'inventory', []),
                'chronicle': getattr(self.player.chronicle, 'entries', []),
                'relationships': getattr(self.player, 'relationships', {}),
                'flags': getattr(self.player, 'flags', {}),
                'saved_at': datetime.utcnow().isoformat()
            }
        return payload

    def save_game(self, filename=None):
        filename = filename or f"save_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json"
        path = os.path.join(self.saves_dir, filename)
        if os.path.exists(path):
            if not confirm(f"Overwrite existing save {filename}?", default=False):
                toast("Save canceled.", "Save")
                return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self._save_payload(), f, ensure_ascii=False, indent=2)
            toast(f"Saved to {filename}", "Save", wait=0.9)
        except Exception as e:
            print(f"[Save] Failed to save: {e}")

    def load_game(self, filename):
        path = os.path.join(self.saves_dir, filename)
        if not os.path.exists(path):
            toast("Save file not found.", "Load", wait=0.8)
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if Player and hasattr(Player, 'from_dict'):
                try:
                    self.player = Player.from_dict(data)
                except Exception:
                    self.player = MinimalPlayer.from_dict(data)
            else:
                self.player = MinimalPlayer.from_dict(data)
            # rewire managers
            if self.memory_manager:
                self.memory_manager.player = self.player
            if self.relationship_manager and hasattr(RelationshipManager, 'from_player_data'):
                self.relationship_manager = RelationshipManager.from_player_data({'relationships': getattr(self.player, 'relationships', {})})
            toast("Load successful.", "Load", wait=0.6)
        except Exception as e:
            print(f"[Load] Failed to load save: {e}")

    def list_saves(self):
        files = sorted(glob.glob(os.path.join(self.saves_dir, '*.json')))
        return [os.path.basename(p) for p in files]

    # --------------------- Gameplay helpers ---------------------
    def _render_header(self):
        clear_screen()
        print(BOLD + "Stasis Hunters".center(70) + RESET)
        print(self._breadcrumb_line())
        print("-" * 70)
        print(status_bar(self.player))
        print("-" * 70)

    def _breadcrumb_line(self):
        return " > ".join(self.breadcrumb)

    def list_scenes(self):
        lines = []
        for sid, scene in sorted(self.scenes_index.items()):
            title = getattr(scene, 'title', scene.get('title') if isinstance(scene, dict) else sid)
            lines.append(f"{sid}: {title}")
        heading("Available Scenes")
        paginate(lines)

    def show_inventory(self):
        inv = getattr(self.player, 'inventory', [])
        if not inv:
            print("[Inventory] (empty)")
            return
        lines = [f"{i+1}) {s.get('id','?')} - {s.get('desc','') or s.get('name','')}" for i, s in enumerate(inv)]
        heading("Inventory")
        paginate(lines)

    def show_chronicle(self):
        entries = getattr(self.player.chronicle, 'entries', [])
        if not entries:
            print("[Chronicle] (no mirrored fragments)")
            return
        lines = [f"{i+1}) {e.get('id')} - {e.get('desc','')}" for i, e in enumerate(entries)]
        heading("Chronicle")
        paginate(lines)

    def show_relationships(self):
        rels = getattr(self.player, 'relationships', {})
        if not rels:
            print('[Relationships] (none)')
            return
        lines = [f"{name}: {val}" for name, val in rels.items()]
        heading("Relationships")
        paginate(lines)

    def memory_preview(self):
        if not self.memory_manager:
            toast("Memory manager not available.", "Memory")
            return
        self.memory_manager.preview_removable()

    def memory_apply(self):
        if not self.memory_manager:
            toast("Memory manager not available.", "Memory")
            return
        removable = self.memory_manager.preview_removable()
        if not removable:
            toast("Nothing removable.", "Memory")
            return
        print("Enter comma-separated IDs to remove (or blank to cancel):")
        val = input("> ").strip()
        if not val:
            toast("Cancelled.", "Memory")
            return
        ids = [s.strip() for s in val.split(",") if s.strip()]
        result = self.memory_manager.apply_removal(ids)
        if result.get("blocked"):
            toast(f"Some items were protected and not removed: {', '.join(result['blocked'])}", "Memory")
        else:
            toast(f"Removed: {', '.join(result['removed'])}", "Memory")


    def check_payoffs(self):
        if not self.payoff_manager:
            toast("Payoff manager not available.", "Payoff")
            return
        newly = self.payoff_manager.check_and_trigger(self.player)
        if not newly:
            toast("No new payoffs unlocked.", "Payoff", wait=0.6)
            return
        for p in newly:
            title = p.get('title')
            desc = p.get('desc', '')
            toast(f"{title}\n{desc}", "Payoff Unlocked", wait=1.0)

    def enter_scene(self, sid):
        scene = self.scenes_index.get(sid)
        if not scene:
            toast("Scene not found.", "Scene")
            return
        # bracket UI state for breadcrumbs
        self.breadcrumb.append(getattr(scene, 'title', sid))
        self._render_header()
        # description
        desc = getattr(scene, 'description', scene.get('description') if isinstance(scene, dict) else '')
        if desc:
            paginate(desc.splitlines())
        # choices
        choices = getattr(scene, 'choices', scene.get('choices') if isinstance(scene, dict) else [])
        if not choices:
            toast("No choices available in this scene.", "Scene")
            self.breadcrumb.pop()
            return
        # present choices with shortcuts
        opts = []
        for idx, ch in enumerate(choices, start=1):
            opts.append((idx, ch.get('text', f'Choice {idx}')))
        while True:
            print("\nChoices:")
            for idx, ch in enumerate(choices, start=1):
                print(f"{idx}) {ch.get('text')}")
            print("b) back    m) main menu")
            sel = input('> ').strip().lower()
            if sel in ('b', 'm'):
                break
            try:
                i = int(sel) - 1
                if not (0 <= i < len(choices)):
                    toast("Invalid choice.", "Input")
                    continue
                choice = choices[i]
                effects = choice.get('effects')
                if hasattr(scene, 'apply_effects'):
                    scene.apply_effects(effects or {}, self.player,
                                         payoff_manager=self.payoff_manager,
                                         relationship_manager=self.relationship_manager,
                                         memory_manager=self.memory_manager,
                                         monsters_index=self.monsters_index)
                else:
                    self._apply_effects_minimal(effects or {})
                # persist relationship manager affinities back to player, if present
                if self.relationship_manager and hasattr(self.relationship_manager, 'affinities'):
                    self.player.relationships = self.relationship_manager.affinities
                # run payoff check defensively
                if self.payoff_manager:
                    self.payoff_manager.check_and_trigger(self.player)
                toast("Choice applied.", "Scene")
            except ValueError:
                toast("Please enter a number for choices.", "Input")
        # exit breadcrumbs
        self.breadcrumb.pop()

    def _apply_effects_minimal(self, effects: Dict[str, Any]):
        sid = effects.get('add_seed')
        if sid and sid in self.seeds_index:
            seed = self.seeds_index[sid]
            if hasattr(self.player, 'add_seed'):
                self.player.add_seed(seed)
            else:
                self.player.inventory.append(seed)
            toast(f"Added seed {sid}", "Effect")
        rel = effects.get('relationship')
        if rel and self.relationship_manager:
            for name, delta in rel.items():
                self.relationship_manager.change_affinity(name, delta)
                self.player.relationships[name] = self.relationship_manager.affinities.get(name, 0)
            toast("Relationship updated.", "Effect")
        mid = effects.get('encounter_monster')
        if mid and self.monsters_index and mid in self.monsters_index:
            try:
                from .monster import Monster as _Monster
                m = _Monster(self.monsters_index[mid])
                drops = m.fight(self.player)
                for d in drops:
                    s = self.seeds_index.get(d)
                    if s:
                        if hasattr(self.player, 'add_seed'):
                            self.player.add_seed(s)
                        else:
                            self.player.inventory.append(s)
                toast(f"Encounter resolved. Drops: {drops}", "Combat")
            except Exception as e:
                print(f"[Encounter] Error: {e}")

    # --------------------- Main menu ---------------------
    def main_menu(self):
        while True:
            self._render_header()
            print("1) New game")
            print("2) Load game")
            print("3) Save game")
            print("4) List scenes")
            print("5) Enter scene")
            print("6) Inventory")
            print("7) Chronicle")
            print("8) Relationships")
            print("9) Memory cost preview")
            print("10) Memory cost apply")
            print("11) Check payoffs")
            print("q) Quit")
            choice = input("> ").strip().lower()
            if choice == '1':
                if confirm("Start a new game (current progress will be lost in RAM)?", default=False):
                    self.player = Player() if Player else MinimalPlayer()
                    # rewire managers
                    if self.memory_manager:
                        self.memory_manager.player = self.player
                    if self.relationship_manager and hasattr(RelationshipManager, 'from_player_data'):
                        self.relationship_manager = RelationshipManager.from_player_data({'relationships': getattr(self.player, 'relationships', {})})
                    toast("New game started.", "Game")
            elif choice == '2':
                saves = self.list_saves()
                if not saves:
                    toast("No saves available.", "Load")
                    continue
                for i, s in enumerate(saves, start=1):
                    print(f"{i}) {s}")
                sel = input('> ').strip()
                try:
                    idx = int(sel) - 1
                    if not (0 <= idx < len(saves)):
                        toast("Invalid save selection.", "Load")
                        continue
                    self.load_game(saves[idx])
                except Exception:
                    toast("Invalid selection.", "Load")
            elif choice == '3':
                # allow providing filename
                print("Enter filename to save as (blank -> auto name):")
                fn = input("> ").strip()
                self.save_game(fn or None)
            elif choice == '4':
                self.breadcrumb.append("Scenes")
                self._render_header()
                self.list_scenes()
                input("Press Enter to return.")
                self.breadcrumb.pop()
            elif choice == '5':
                print("Enter scene id:")
                sid = input('> ').strip()
                if sid:
                    self.enter_scene(sid)
            elif choice == '6':
                self.breadcrumb.append("Inventory")
                self._render_header()
                self.show_inventory()
                input("Press Enter to return.")
                self.breadcrumb.pop()
            elif choice == '7':
                self.breadcrumb.append("Chronicle")
                self._render_header()
                self.show_chronicle()
                input("Press Enter to return.")
                self.breadcrumb.pop()
            elif choice == '8':
                self.breadcrumb.append("Relationships")
                self._render_header()
                self.show_relationships()
                input("Press Enter to return.")
                self.breadcrumb.pop()
            elif choice == '9':
                self.memory_preview()
                input("Press Enter to return.")
            elif choice == '10':
                self.memory_apply()
                input("Press Enter to return.")
            elif choice == '11':
                self.check_payoffs()
                input("Press Enter to return.")
            elif choice == 'q':
                if confirm("Quit game? (progress not saved automatically)", default=False):
                    toast("Goodbye — may your seeds find payoffs.", "Exit", wait=0.5)
                    break
            else:
                toast("Invalid choice.", "Input")

    def run(self):
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print("\nInterrupted — exiting")


if __name__ == '__main__':
    Game().run()
