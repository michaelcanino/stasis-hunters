# src/scene.py
import random
import time
from typing import Dict

class Scene:
    def __init__(self, scene_data, seeds_index):
        """
        scene_data: dict describing scene (id, title, desc, choices)
        seeds_index: mapping seed_id -> seed dict
        """
        self.id = scene_data['id']
        self.title = scene_data.get('title', '')
        self.desc = scene_data.get('desc', '')
        self.choices = scene_data.get('choices', [])
        self.seeds_index = seeds_index

    def show(self):
        print(f"\n=== Scene: {self.title} ({self.id}) ===")
        print(self.desc)
        print("\nChoices:")
        for i, c in enumerate(self.choices, 1):
            print(f"{i}. {c.get('label')}")
        print(f"{len(self.choices)+1}. Back to Chapter menu")

    def perform_choice(self, idx, player):
        # idx is 1-based index of choice in self.choices
        if idx < 1 or idx > len(self.choices):
            return
        choice = self.choices[idx-1]
        action = choice.get('action')
        if action == "pickup_seed":
            seed_id = choice.get('seed_id')
            seed = self.seeds_index.get(seed_id)
            if not seed:
                print("[Scene] No such seed.")
                return
            player.add_seed(seed)
        elif action == "anchor_minigame":
            self.anchor_minigame(player)
        elif action == "text":
            print("\n" + choice.get('text', '(no text)'))
        else:
            print("\n[Scene] Unhandled action:", action)

    def anchor_minigame(self, player):
        """
        Simple timed quick-choice mini-game:
        - shows a small puzzle (e.g., compute a+b)
        - measure response time and correctness
        Outcome: Perfect (fast+correct), Partial (correct+slow), Fail (incorrect)
        """
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        correct = a + b
        print("\n[Anchor Mini-game] Solve quickly!")
        print(f"What is {a} + {b}?")
        start = time.time()
        answer = input("> ").strip()
        elapsed = time.time() - start
        try:
            ans_i = int(answer)
            if ans_i == correct and elapsed < 3.0:
                print(f"[Mini-game] PERFECT! ({elapsed:.2f}s)")
            elif ans_i == correct:
                print(f"[Mini-game] Partial success. ({elapsed:.2f}s)")
            else:
                print(f"[Mini-game] Fail — wrong answer. ({elapsed:.2f}s)")
        except:
            print(f"[Mini-game] Fail — invalid input. ({elapsed:.2f}s)")

    def apply_effects(self, effects: dict, player, payoff_manager=None, relationship_manager=None, memory_manager=None, monsters_index=None):
        """
        Apply declarative 'effects' from scene JSON.
        Supported keys (minimal Phase2): add_seed, relationship, encounter_monster, memory_cost_preview
        """
        if not effects:
            return

        # add seed (expects seed_id string)
        sid = effects.get("add_seed")
        if sid:
            seed = self.seeds_index.get(sid)
            if seed:
                player.add_seed(seed)
                # check payoffs if manager present
                if payoff_manager:
                    payoff_manager.check_and_trigger(player)

        # relationship adjustments: {"Hana": 1}
        rel = effects.get("relationship")
        if rel and relationship_manager:
            for name, delta in rel.items():
                relationship_manager.change_affinity(name, delta)
                # also persist to player.relationships for compatibility
                player.relationships[name] = relationship_manager.affinities.get(name, 0)

        # encounter monster: expects monster id string
        mid = effects.get("encounter_monster")
        if mid and monsters_index:
            mdata = monsters_index.get(mid)
            if mdata:
                from .monster import Monster
                m = Monster(mdata)
                drops = m.fight(player)
                # apply drops to player inventory
                for d in drops:
                    s = self.seeds_index.get(d)
                    if s:
                        player.add_seed(s)
                        if payoff_manager:
                            payoff_manager.check_and_trigger(player)

        # Memory cost preview/apply (very simple toggle)
        if effects.get("memory_cost_preview") and memory_manager:
            memory_manager.preview_removable()
