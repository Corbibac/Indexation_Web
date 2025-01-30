import re


# ---------------------- Tokenization Function ---------------------- #
def my_tokenizer(text, stopwords):
    """Tokenizes text by removing punctuation, converting to lowercase, and filtering out stopwords."""
    tokens = re.findall(r"\b\w+\b", text.lower())  # Extract words
    return [token for token in tokens if token not in stopwords]  # Remove stopwords
