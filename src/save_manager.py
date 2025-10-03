# src/save_manager.py
import json
import os
import hashlib
from typing import Dict, Tuple

class SaveManager:
    """
    Saves player state to JSON and appends a SHA-256 signature over the
    canonical JSON payload (player + chronicle_entries) to help detect tampering.
    """
    def __init__(self, save_path="saves/save.json"):
        self.save_path = save_path
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

    def _compute_signature(self, payload_obj: Dict) -> str:
        """
        Compute SHA-256 hex signature for a JSON-serializable object.
        We canonicalize by dumping with sort_keys=True and separators to stabilize representation.
        """
        payload_bytes = json.dumps(payload_obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(payload_bytes).hexdigest()

    def save(self, player, extra=None):
        """
        Save the canonical payload (what we consider protected), then attach a signature.
        The saved file has keys:
          - protected_payload: { player: {...}, chronicle_entries: [...] }
          - signature: "<hex>"
          - extra: optional developer extras
        """
        protected = {
            "player": {
                "name": player.name,
                "inventory": [{"id": s['id'], "desc": s.get('desc','')} for s in player.inventory],
                "relationships": player.relationships
            },
            "chronicle_entries": player.chronicle.entries
        }
        signature = self._compute_signature(protected)
        to_write = {
            "protected_payload": protected,
            "signature": signature
        }
        if extra:
            to_write["extra"] = extra
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(to_write, f, indent=2, ensure_ascii=False)
        print(f"\n[SaveManager] Game saved to {self.save_path}")
        print(f"[SaveManager] Signature: {signature}")

    def load_raw(self):
        """
        Load the save file (no verification). Returns dict or None.
        """
        if not os.path.exists(self.save_path):
            print("[SaveManager] No save found.")
            return None
        with open(self.save_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        print(f"[SaveManager] Loaded save from {self.save_path}")
        return state

    def load_and_verify(self) -> Tuple[bool, Dict]:
        """
        Load and verify the signature. Returns (is_valid, protected_payload_or_None).
        """
        state = self.load_raw()
        if not state:
            return False, None
        protected = state.get("protected_payload")
        signature = state.get("signature")
        if protected is None or signature is None:
            print("[SaveManager] Save missing protected payload or signature.")
            return False, None
        expected = self._compute_signature(protected)
        ok = (expected == signature)
        if ok:
            print("[SaveManager] Signature verification OK.")
        else:
            print("[SaveManager] Signature mismatch! Save may be tampered with.")
            print(f"Expected: {expected}")
            print(f"Found:    {signature}")
        return ok, protected
