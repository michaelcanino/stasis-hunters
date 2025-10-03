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
