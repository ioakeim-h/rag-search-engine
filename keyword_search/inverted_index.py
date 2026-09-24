import os
import pickle
from collections import defaultdict

from utils import read_json
from keyword_search.text import tokenize_text

from config import (
    MOVIES_PATH,
    CACHE_PATH,
    CACHE_INDEX,
    CACHE_DOCMAP
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
        self.index = defaultdict(set)

        # Maps document IDs to their full document objects (movie dicts)
        self.docmap = {}


    def __add_document(self, doc_id: int, text: str):
        tokens = tokenize_text(text)

        # Add each token and doc_id to the index
        for t in tokens:
            self.index[t].add(doc_id)


    def get_documents(self, term: str) -> list[int]:
        """
        Get the document IDs for a single tokenized word 
        Return them as a sorted list in ascending order
        """
        ids = self.index.get(term, set())
        return sorted(ids)


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

        # Save index and docmap attributes to disk
        # index_path = os.path.join(CACHE_PATH, "index.pkl")
        # docmap_path = os.path.join(CACHE_PATH, "docmap.pkl")

        with open(CACHE_INDEX, "wb") as file:
            pickle.dump(self.index, file)

        with open(CACHE_DOCMAP, "wb") as file:
            pickle.dump(self.docmap, file)


    def load(self):
        if not os.path.exists(CACHE_INDEX):
            raise FileNotFoundError(f"Path not found: {CACHE_INDEX}")

        if not os.path.exists(CACHE_DOCMAP):
            raise FileNotFoundError(f"Path not found: {CACHE_DOCMAP}")

        # Load index and docmap from disk
        with open(CACHE_INDEX, "rb") as file:
            self.index = pickle.load(file)

        with open(CACHE_DOCMAP, "rb") as file:
            self.docmap = pickle.load(file)


def build_index():
    idx = InvertedIndex()
    idx.build()
    idx.save()

