import os
import pickle
from collections import Counter, defaultdict

from utils import read_json
from keyword_search.text import tokenize_text

from config import (
    MOVIES_PATH,
    CACHE_PATH,
    CACHE_INDEX,
    CACHE_DOCMAP,
    CACHE_TERM_FREQ
)


class InvertedIndex:
    """
    An inverted index is what makes keyword search fast
    Instead of scanning every document on every search, we build a lookup table ahead of time

    A "forward index" maps location → value
    An "inverted index" maps value → location
    """
    def __init__(self):
        # Maps tokens to sets of document IDs
        # set() excludes duplicates during __add_document method
        self.index: defaultdict[str, set[int]] = defaultdict(set)

        # Maps document IDs to their full document objects (movie dicts)
        self.docmap: dict[int, dict] = {}

        # Maps document IDs to their term frequencies
        # measures how often a word occurs in a document
        self.term_frequencies: defaultdict[int, Counter[str]] = defaultdict(Counter)


    def __add_document(self, doc_id: int, text: str):
        tokens = tokenize_text(text)

        # Add each token and doc_id to the index
        for t in tokens:
            self.index[t].add(doc_id)

        # Count how many times a term appears in the doc 
        self.term_frequencies[doc_id].update(tokens)


    def get_documents(self, term: str) -> list[int]:
        """
        Get the document IDs for a single tokenized word 
        Return them as a sorted list in ascending order
        """
        ids = self.index.get(term, set())
        return sorted(ids)


    def get_term_freq(self, doc_id: int, term: str) -> int:
        count = self.term_frequencies[doc_id][term]
        return count


    def build(self):
        movies: list[dict] = read_json(MOVIES_PATH)["movies"]

        for m in movies:
            doc_id = m["id"]
            text = f"{m['title']} {m['description']}"

            # Populate index
            self.__add_document(doc_id, text)

            # Populate docmap
            self.docmap[doc_id] = m


    def save(self):
        # Create cache dir if not exists
        os.makedirs(CACHE_PATH, exist_ok=True)

        # Save attributes to disk
        with open(CACHE_INDEX, "wb") as file:
            pickle.dump(self.index, file)

        with open(CACHE_DOCMAP, "wb") as file:
            pickle.dump(self.docmap, file)

        with open(CACHE_TERM_FREQ, "wb") as file:
            pickle.dump(self.term_frequencies, file)


    def load(self):
        if not os.path.exists(CACHE_INDEX):
            raise FileNotFoundError(f"Path not found: {CACHE_INDEX}")

        if not os.path.exists(CACHE_DOCMAP):
            raise FileNotFoundError(f"Path not found: {CACHE_DOCMAP}")

        if not os.path.exists(CACHE_TERM_FREQ):
            raise FileNotFoundError(f"Path not found: {CACHE_TERM_FREQ}")

        # Load from disk
        with open(CACHE_INDEX, "rb") as file:
            self.index = pickle.load(file)

        with open(CACHE_DOCMAP, "rb") as file:
            self.docmap = pickle.load(file)

        with open(CACHE_TERM_FREQ, "rb") as file:
            self.term_frequencies = pickle.load(file)


def build_index():
    idx = InvertedIndex()
    idx.build()
    idx.save()

