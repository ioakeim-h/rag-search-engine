import os
import pickle
import string
from nltk.stem import PorterStemmer
from collections import defaultdict

from lib.utils import read_json

from config import (
    STOPWORDS_PATH,
    MOVIES_PATH,
    CACHE_PATH
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
        index_path = os.path.join(CACHE_PATH, "index.pkl")
        docmap_path = os.path.join(CACHE_PATH, "docmap.pkl")

        with open(index_path, "wb") as file:
            pickle.dump(self.index, file)

        with open(docmap_path, "wb") as file:
            pickle.dump(self.docmap, file)


def build_command():
    idx = InvertedIndex()
    idx.build()
    idx.save()

    # Test
    docs = idx.get_documents("merida")
    print(f"First document for token 'merida' = {docs[0]}")


def search_by_keyword(data: list[dict], search_query: str, search_target: str, search_limit: int) -> list[dict]:
    results = []
    query_tokens = tokenize_text(search_query) 
    
    for item in data:

        # Truncate returned output
        if len(results) == search_limit:
            break

        target_tokens = tokenize_text(item[search_target])  

        # Find query words in target 
        for q in query_tokens:
            if q in target_tokens:
                results.append(item) 
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