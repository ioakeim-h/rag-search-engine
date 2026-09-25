import os

PROJECT_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "rag-search-engine"
)

MOVIES_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, "data", "stopwords.txt")

CACHE_PATH = os.path.join(PROJECT_ROOT, "cache")
CACHE_INDEX = os.path.join(CACHE_PATH, "index.pkl")
CACHE_DOCMAP = os.path.join(CACHE_PATH, "docmap.pkl")

DEFAULT_SEARCH_LIMIT = 5

