# Run: uv run python -m keyword_search.cli <command> <args>

import argparse

from utils import read_json
from keyword_search.search import search_by_keyword
from keyword_search.inverted_index import build_index

from config import (
    DEFAULT_SEARCH_LIMIT,
    MOVIES_PATH,
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
            print(f"Searching for: {args.query}")
            movies = read_json(MOVIES_PATH)["movies"]
         
            results = search_by_keyword(
                data = movies,
                search_query = args.query,
                search_target = "title",
                search_limit = DEFAULT_SEARCH_LIMIT,
            )

            for i, item in enumerate(results):
                print(f"{i+1}. {item}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()