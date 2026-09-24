import os


PROJECT_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "workspace",
    "rag-search-engine"
)

MOVIES_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, "data", "stopwords.txt")

CACHE_PATH = os.path.join(PROJECT_ROOT, "cache")

DEFAULT_SEARCH_LIMIT = 5

