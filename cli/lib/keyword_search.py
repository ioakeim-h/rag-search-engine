import json


def search_movies(path: str, query: str, search_limit: int) -> list[dict]:
    movies = read_json(path)["movies"]
    return search_by_keyword(movies, query, "title", search_limit)
    

def read_json(path: str) -> dict:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f"Data at {path} is not valid JSON")


def search_by_keyword(data: dict, query: str, key: str, limit: int) -> list[dict]:
    results = []
    for idx, item in enumerate(data):
        
        if len(results) == limit:
            break
        
        if query in data[idx][key]:
            results.append(item)

    return results

