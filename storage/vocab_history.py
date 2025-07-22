# storage/vocab_history.py

import json
from pathlib import Path


class VocabHistory:
    def __init__(self, history_path="data/histories/vocab_history.json", max_length=60):
        # Resolve path relative to project root
        project_root = Path(__file__).resolve().parent.parent
        self.history_path = (project_root / history_path).resolve()
        self.max_length = max_length
        self.history = []  # ✅ always initialized
        self._load_history()

    def _load_history(self):
        if self.history_path.exists():
            try:
                with open(self.history_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.history = data[-self.max_length:]
            except (json.JSONDecodeError, IOError):
                print(f"⚠️ Warning: could not load history from {self.history_path}. Starting fresh.")
                self.history = []

    def _save_history(self):
        # Make sure the parent dir exists
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(self.history[-self.max_length:], f, indent=2, ensure_ascii=False)

    def add_category(self, category: str):
        if category in self.history:
            self.history.remove(category)
        self.history.append(category)
        self._save_history()

    def was_used_recently(self, category: str) -> bool:
        return category in self.history

    def get_recent(self) -> list:
        return self.history[-self.max_length:]

    def get_unused(self, all_categories: list) -> list:
        return [cat for cat in all_categories if cat not in self.history]

    def clear(self):
        self.history = []
        self._save_history()
