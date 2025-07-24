# helper_functions/topic_selector.py

import random

from storage.history import History

class TopicSelector:
    def __init__(self, all_categories: list[str], history: History):
        self.all_categories = all_categories
        self.history = history

    def get_unused_topic(self):
        unused = self.history.get_unused(self.all_categories)
        if not unused:
            raise ValueError("No unused vocabulary topics available.")
        return random.choice(unused)
