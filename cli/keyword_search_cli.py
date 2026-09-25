import argparse

from lib.utils import read_json
from lib.keyword_search import search_by_keyword, build_index, InvertedIndex

from config import (
    CACHE_PATH,
    DEFAULT_SEARCH_LIMIT
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    subparsers.add_parser("build", help="Build the inverted index")
    
    args = parser.parse_args()

    match args.command:

        case "build":
            # As long as the data doesn't change, 
            # we don't need to rebuild the index before every search
            print("Building inverted index...")
            build_index()
            print("Inverted index built successfully.")

        case "search":
            print("Loading inverted index...")
            idx = InvertedIndex()
            
            try: 
                idx.load()
            except FileNotFoundError:
                raise(f"Index files missing from: {CACHE_PATH}")

            print(f"Searching for: {args.query}")
            results = search_by_keyword(
                inverted_index = idx,
                search_query = args.query,
                search_limit = DEFAULT_SEARCH_LIMIT
            )

            for i, item in enumerate(results):
                print(f"{i+1}. {item}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()