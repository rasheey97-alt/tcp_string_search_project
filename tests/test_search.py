# test_search.py
import unittest
from search import StringSearcher

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.searcher = StringSearcher()
        self.searcher.strings = {"apple", "banana", "carrot"}

    def test_search_found(self):
        self.assertIn("apple", self.searcher)

    def test_search_not_found(self):
        self.assertNotIn("mango", self.searcher)

if __name__ == "__main__":
    unittest.main()
