from keyword_search.text import tokenize_text


def search_by_keyword(data: list[dict], search_query: str, search_target: str, search_limit: int) -> list[dict]:
    results = []
    query_tokens = tokenize_text(search_query) 
    
    for item in data:

        # Truncate returned output
        if len(results) == search_limit:
            break

        target_tokens = tokenize_text(item[search_target])  

        # Find query words in target 
        for q in query_tokens:
            if q in target_tokens:
                results.append(item) 
                break

    return results
