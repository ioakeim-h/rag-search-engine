import argparse

from lib.utils import read_json
from lib.keyword_search import search_by_keyword

from config import (
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
            movies = read_json(DATA_PATH)["movies"]
         
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