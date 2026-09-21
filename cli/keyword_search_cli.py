import argparse

from lib.keyword_search import search_movies

from lib.search_utils import (
    DATA_PATH,
    DEFAULT_SEARCH_LIMIT
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            results = search_movies(DATA_PATH, args.query, search_limit=DEFAULT_SEARCH_LIMIT)

            for i, item in enumerate(results):
                print(f"{i+1}. {item}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()