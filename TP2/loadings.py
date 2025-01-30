import json


# ---------------------- Load Stopwords ---------------------- #
def load_stopwords(filepath):
    """Loads stopwords from a given file and returns a set for filtering tokens."""
    with open(filepath, "r", encoding="utf-8") as f:
        return set(word.strip() for word in f.readlines())


# ---------------------- Load and Parse JSONL File ---------------------- #
def load_products(filepath):
    """Loads product data from a JSONL file where each line contains a JSON object."""
    products = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            products.append(json.loads(line.strip()))  # Parse each JSON line
    return products
