import json


def read_json(path: str) -> dict:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f"Data at {path} is not valid JSON")