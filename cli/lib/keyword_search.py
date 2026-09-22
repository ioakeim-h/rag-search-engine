import string
from nltk.stem import PorterStemmer

from config import STOPWORDS_PATH


def search_by_keyword(data: list[dict], search_query: str, search_target: str, search_limit: int) -> list[dict]:
    stemmer = PorterStemmer()

    stopwords = fetch_stopwords()
    stopword_tokens = clean_text(stopwords)

    results = []
    for idx, item in enumerate(data):

        # Truncate returned output
        if len(results) == search_limit:
            break

        query_tokens = clean_text(search_query)
        target_tokens = clean_text(data[idx][search_target])

        # Remove stopwords ('the', 'is', 'a', etc)
        filtered_query_tokens = [word for word in query_tokens if word not in stopword_tokens]
        filtered_target_tokens = [word for word in target_tokens if word not in stopword_tokens]

        # Stemming (running, runs → run)
        stemmed_query_tokens = [stemmer.stem(token) for token in filtered_query_tokens]
        stemmed_target_tokens = [stemmer.stem(token) for token in filtered_target_tokens]

        # Find word, or part of it, in target 
        # For example, "fast" matches "faster"
        if match_tokens(stemmed_query_tokens, stemmed_target_tokens):
            results.append(item)

    return results


def clean_text(text: str) -> list[str]:
    # Case insensitivity
    text = text.lower()

    # Remove punctuation (may not work well with hyphenated words)
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Tokenize: split text into smaller pieces 
    text = text.split() 

    return text


def fetch_stopwords() -> str:
    with open(STOPWORDS_PATH, "r") as file:
        content = file.read()
    
    stopwords = content.splitlines() 
    return " ".join(stopwords)


def match_tokens(query_tokens: list, target_tokens: list) -> bool:
        for q in query_tokens:
            for t in target_tokens:
                if q in t:
                    return True
        return False



