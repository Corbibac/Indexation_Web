import nltk
import re

nltk.download("stopwords")
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))


def tokenize(text):
    """
    Tokenizes text by:
    1. Converting to lowercase
    2. Removing punctuation (only keep alphanumeric)
    3. Splitting on word boundaries
    4. Removing stopwords
    """
    text = text.lower()
    tokens = re.findall(r"\b\w+\b", text)
    return [t for t in tokens if t not in STOPWORDS]
