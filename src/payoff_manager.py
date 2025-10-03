# src/payoff_manager.py
import json
import os
from typing import Dict, List

class PayoffManager:
    """
    Loads payoffs from data/payoffs.json and can check a player's Chronicle
    for unlocked payoffs. Keeps track of triggered payoffs on player.flags['payoffs_triggered'].
    """
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.payoffs = self._load_payoffs()

    def _load_payoffs(self) -> Dict:
        pfile = os.path.join(self.data_dir, "payoffs.json")
        try:
            with open(pfile, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[PayoffManager] Failed to load payoffs.json: {e}")
            return {}

    def check_and_trigger(self, player) -> List[Dict]:
        """
        Check all payoffs; if requirements met and not yet triggered, trigger them
        and add to player.flags['payoffs_triggered'].
        Returns list of triggered payoff dicts.
        """
        if player is None:
            return []
        triggered = set(player.flags.get("payoffs_triggered", []))
        chronicle_ids = {e['id'] for e in getattr(player.chronicle, "entries", [])}
        newly_triggered = []
        for pid, payoff in (self.payoffs.items() if isinstance(self.payoffs, dict) else []):
            required = set(payoff.get("required_seeds", []))
            if required and required.issubset(chronicle_ids) and pid not in triggered:
                # trigger payoff
                triggered.add(pid)
                newly_triggered.append(payoff)
                print(f"[PayoffManager] Triggered payoff {pid}: {payoff.get('title')}")
        # persist back to player flags
        player.flags["payoffs_triggered"] = list(triggered)
        return newly_triggered
