# search.py
from config import DATA_FILE

class StringSearcher:
    def __init__(self):
        self.strings = set()

    def load_data(self):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            self.strings = set(line.strip() for line in f)

    def __contains__(self, item):
        return item in self.strings
