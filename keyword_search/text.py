import string

from nltk.stem import PorterStemmer

from config import STOPWORDS_PATH


def clean_text(text: str) -> str:
    # Case insensitivity
    text = text.lower()

    # Remove punctuation (may not work well with hyphenated words)
    return text.translate(str.maketrans("", "", string.punctuation))


def fetch_stopwords() -> set[str]:
    with open(STOPWORDS_PATH, "r") as file:
        content = file.read()

    return {clean_text(word) for word in content.splitlines()}


def tokenize_text(text: str) -> list[str]:
    text = clean_text(text)
    
    # Tokenize: split text into smaller pieces 
    tokens = text.split() 

    # Remove stopwords ('the', 'is', 'a', etc)
    filtered_tokens = [t for t in tokens if t not in STOPWORDS]

    # Stemming (running, runs → run)
    stemmed_tokens = [stemmer.stem(t) for t in filtered_tokens]

    return stemmed_tokens


STOPWORDS = fetch_stopwords()
stemmer = PorterStemmer()