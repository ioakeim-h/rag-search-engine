from keyword_search.text import tokenize_text
from keyword_search.inverted_index import InvertedIndex


def search_by_keyword(inverted_index: InvertedIndex, search_query: str, search_limit: int) -> list[dict]:
    """
    Search the inverted index for documents matching any token in the query.

    The query is tokenized the same way documents were tokenized when the
    index was built, ensuring consistent matching (e.g. lowercasing, stemming).
    For each token, matching document IDs are looked up directly in the
    inverted index rather than scanning every document.

    Documents that match multiple query tokens are only included once.
    Matching stops as soon as `search_limit` results have been collected.

    Args:
        inverted_index: A loaded InvertedIndex containing the token -> doc ID
            mapping and the doc ID -> document lookup (docmap).
        search_query: The raw search string provided by the user.
        search_limit: The maximum number of results to return.

    Returns:
        A list of document dicts, ordered by the order in which their
        matching tokens were found in the query and index lookups.
    """
    seen = set()       # tracks which doc_ids we've already added, fast lookup
    results = []       # the ordered list of actual dicts to return
    
    stop = False       # signals both loops to exit once we've hit search_limit
    query_tokens = tokenize_text(search_query) 

    for t in query_tokens:
        # Look up every document that contains this token
        doc_ids: list[int] = inverted_index.get_documents(t)
        
        for id in doc_ids:
            # Skip documents already matched by a previous token
            if id in seen:
                continue
            
            seen.add(id)
            results.append(inverted_index.docmap[id])

            # Truncate returned output
            if len(results) == search_limit:
                stop = True
                break

        if stop:
            break

    return results
    


