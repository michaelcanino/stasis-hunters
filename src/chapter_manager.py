# src/chapter_manager.py
import os
import json
from typing import Dict, Optional

class ChapterManager:
    """
    Simple chapter manager for Phase 3.
    Responsibilities:
      - load chapters.json
      - track current chapter id / meta
      - reset per-chapter chronosense uses on enter
      - recharge Tech Pulse on enter
    """

    def __init__(self, data_dir: str, player=None):
        self.data_dir = data_dir
        self.player = player
        self.chapters = self._load_chapters()
        self.current_id: Optional[str] = None

    def _load_chapters(self) -> Dict:
        path = os.path.join(self.data_dir, "chapters.json")
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as fh:
                arr = json.load(fh)
                return {c.get("id"): c for c in arr}
        except Exception:
            return {}

    def enter_chapter(self, chapter_id: str) -> bool:
        """Set current chapter, reset uses and recharge as defined in chapters.json."""
        if chapter_id not in self.chapters:
            return False
        ch = self.chapters[chapter_id]
        self.current_id = chapter_id

        # Chronosense uses per chapter
        uses = int(ch.get("chronosense_uses", 2))
        if self.player is not None:
            setattr(self.player, "chronosense_uses_remaining", uses)

            # Tech pulse max / recharge
            tp_max = int(ch.get("tech_pulse_max", getattr(self.player, "tech_pulse_max", 3)))
            self.player.tech_pulse_max = tp_max

            # Starting / recharge behaviour — add 'tech_pulse_recharge' to chapter to control increment
            recharge = int(ch.get("tech_pulse_recharge", 1))
            # if player has no tech_pulse, set to either configured start or max
            if not hasattr(self.player, "tech_pulse"):
                start = int(ch.get("tech_pulse_start", tp_max))
                self.player.tech_pulse = min(start, tp_max)
            else:
                self.player.tech_pulse = min(self.player.tech_pulse + recharge, tp_max)
        return True

    def get_current(self):
        return self.chapters.get(self.current_id) if self.current_id else None

    def use_chronosense(self, amount=1) -> bool:
        if not self.player:
            return False
        cur = getattr(self.player, "chronosense_uses_remaining", 0)
        if cur >= amount:
            self.player.chronosense_uses_remaining = cur - amount
            return True
        return False
