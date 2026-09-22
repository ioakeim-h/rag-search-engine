import string


def search_by_keyword(data: list[dict], search_query: str, search_target: str, search_limit: int) -> list[dict]:
    results = []
    for idx, item in enumerate(data):

        # Truncate returned output
        if len(results) == search_limit:
            break

        query_tokens = clean_text(search_query)
        target_tokens = clean_text(data[idx][search_target])

        # Find word, or part of it, in target 
        # For example, "fast" matches "faster"
        if match_tokens(query_tokens, target_tokens):
            results.append(item)

    return results


def clean_text(text: str) -> list[str]:
    # Case insensitivity
    text = text.lower()

    # Remove punctuation (may not work well with hyphenated words)
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Tokenize: split text into smaller pieces
    # split with no arg splits on all whitespace
    text = text.split() 

    return text


def match_tokens(query_tokens: list, target_tokens: list) -> bool:
        for q in query_tokens:
            for t in target_tokens:
                if q in t:
                    return True
        return False
