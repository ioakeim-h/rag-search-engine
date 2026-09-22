import os

PROJECT_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "rag-search-engine"
)

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")

DEFAULT_SEARCH_LIMIT = 5

