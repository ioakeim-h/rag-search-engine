# Run: uv run python -m keyword_search.cli <command> <args>

import argparse

from keyword_search.text import tokenize_term
from keyword_search.search import search_by_keyword
from keyword_search.inverted_index import build_index, InvertedIndex

from config import (
    CACHE_PATH,
    DEFAULT_SEARCH_LIMIT,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("build", help="Build the inverted index")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    tf_parser = subparsers.add_parser("tf", help="Get term frequency")
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Term")
    
    args = parser.parse_args()

    match args.command:

        case "build":
            # As long as the data doesn't change, 
            # we don't need to rebuild the index before every search
            print("Building inverted index...")
            build_index()
            print("Inverted index built successfully.")

        case "search":
            idx = load_index()

            print(f"Searching for: {args.query}")
            results = search_by_keyword(
                inverted_index = idx,
                search_query = args.query,
                search_limit = DEFAULT_SEARCH_LIMIT
            )

            for i, item in enumerate(results):
                print(f"{i+1}. {item}")

        case "tf":
            idx = load_index()
            token = tokenize_term(args.term)

            freq = idx.get_term_freq(args.doc_id, token)
            print(f"Document ID: {args.doc_id}")
            print(f"Term: {args.term}")
            print(f"Term frequency: {freq}")

        case _:
            parser.print_help()


def load_index():
    print("Loading inverted index...")
    idx = InvertedIndex()
    
    try: 
        idx.load()
        return idx 
    except FileNotFoundError:
        raise FileNotFoundError(f"Index files missing from: {CACHE_PATH}")

    
if __name__ == "__main__":
    main()