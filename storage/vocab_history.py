from storage.history import History


class VocabHistory(History):
    def __init__(self):
        super().__init__(history_path="data/histories/vocab_history.json", max_length=60)