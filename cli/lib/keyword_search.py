import os
import pickle
import string
from nltk.stem import PorterStemmer
from collections import defaultdict

from lib.utils import read_json

from config import (
    STOPWORDS_PATH,
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


def search_by_keyword(inverted_index: InvertedIndex, search_query: str, search_limit: int) -> list[dict]:
    """
    Search the inverted index for documents matching any token in the query.

    The query is tokenized the same way documents were tokenized when the
    index was built, ensuring consistent matching (e.g. lowercasing, stemming).
    For each token, matching document IDs are looked up directly in the
    inverted index rather than scanning every document.

    Documents that match multiple query tokens are only included once.
    Matching stops as soon as `search_limit` results have been collected.

    Args:
        inverted_index: A loaded InvertedIndex containing the token -> doc ID
            mapping and the doc ID -> document lookup (docmap).
        search_query: The raw search string provided by the user.
        search_limit: The maximum number of results to return.

    Returns:
        A list of document dicts, ordered by the order in which their
        matching tokens were found in the query and index lookups.
    """
    seen = set()       # tracks which doc_ids we've already added, fast lookup
    results = []       # the ordered list of actual dicts to return
    
    stop = False       # signals both loops to exit once we've hit search_limit
    query_tokens = tokenize_text(search_query) 

    for t in query_tokens:
        # Look up every document that contains this token
        doc_ids: list[int] = inverted_index.get_documents(t)
        
        for id in doc_ids:
            # Skip documents already matched by a previous token
            if id in seen:
                continue
            
            seen.add(id)
            results.append(inverted_index.docmap[id])

            # Truncate returned output
            if len(results) == search_limit:
                stop = True
                break

        if stop:
            break

    return results
    


def clean_text(text: str) -> str:
    # Case insensitivity
    text = text.lower()

    # Remove punctuation (may not work well with hyphenated words)
    return text.translate(str.maketrans("", "", string.punctuation))


def fetch_stopwords() -> set[str]:
    with open(STOPWORDS_PATH, "r") as file:
        content = file.read()

    return {clean_text(word) for word in content.splitlines()}


def tokenize_text(text: str) -> list[str]:
    text = clean_text(text)
    
    # Tokenize: split text into smaller pieces 
    tokens = text.split() 

    # Remove stopwords ('the', 'is', 'a', etc)
    filtered_tokens = [t for t in tokens if t not in STOPWORDS]

    # Stemming (running, runs → run)
    stemmed_tokens = [stemmer.stem(t) for t in filtered_tokens]

    return stemmed_tokens


STOPWORDS = fetch_stopwords()
stemmer = PorterStemmer()