from storage.mongodb_handler import MongoDBHandler

class History:
    def __init__(self, post_type: str, max_length: int = 60):
        self.post_type = post_type
        self.max_length = max_length
        self.db = MongoDBHandler(collection_name="post_histories")
        self.history = self._load_history()

    def _load_history(self) -> list:
        doc = self.db.find_post({"type": self.post_type})
        if doc and "history" in doc:
            return doc["history"][-self.max_length:]
        return []

    def _save_history(self):
        trimmed = self.history[-self.max_length:]
        self.db.collection.update_one(
            {"type": self.post_type},
            {"$set": {"history": trimmed}},
            upsert=True
        )

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
