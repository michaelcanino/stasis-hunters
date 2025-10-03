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
        triggered = player.flags.get("payoffs_triggered", [])
        chronicle_ids = {e['id'] for e in player.chronicle.entries}
        newly_triggered = []
        for pid, pdata in self.payoffs.items():
            if pid in triggered:
                continue
            reqs = set(pdata.get("required_seeds", []))
            if reqs.issubset(chronicle_ids):
                print(f"[Payoff] Payoff unlocked: {pdata.get('title')} ({pid})")
                triggered.append(pid)
                newly_triggered.append(pdata)
        player.flags["payoffs_triggered"] = triggered
        return newly_triggered

    def list_locked(self, player) -> List[Dict]:
        chronicle_ids = {e['id'] for e in player.chronicle.entries}
        locked = []
        for pid, pdata in self.payoffs.items():
            reqs = set(pdata.get("required_seeds", []))
            if not reqs.issubset(chronicle_ids):
                locked.append({"id": pid, "title": pdata.get("title"), "missing": list(reqs - chronicle_ids)})
        return locked
