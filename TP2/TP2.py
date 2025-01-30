import json
import os
import re
from collections import defaultdict


# ---------------------- Load Stopwords ---------------------- #
def load_stopwords(filepath):
    """Loads stopwords from a given file and returns a set for filtering tokens."""
    with open(filepath, "r", encoding="utf-8") as f:
        return set(word.strip() for word in f.readlines())


# Load the stopwords from the provided file
STOPWORDS = load_stopwords("TP2/stopwords-en.txt")


# ---------------------- Load and Parse JSONL File ---------------------- #
def load_products(filepath):
    """Loads product data from a JSONL file where each line contains a JSON object."""
    products = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            products.append(json.loads(line.strip()))  # Parse each JSON line
    return products


# ---------------------- Extract Product ID and Variant ---------------------- #
def extract_product_id(url):
    """Extracts the product ID and variant from a product URL, if present."""
    match = re.search(r"/product/(\d+)(?:\?variant=(\w+))?", url)
    if match:
        return match.group(1), match.group(2) if match.group(2) else None
    return None, None


# ---------------------- Tokenization Function ---------------------- #
def tokenize(text):
    """Tokenizes text by removing punctuation, converting to lowercase, and filtering out stopwords."""
    tokens = re.findall(r"\b\w+\b", text.lower())  # Extract words
    return [token for token in tokens if token not in STOPWORDS]  # Remove stopwords


# ---------------------- Create Inverted Index ---------------------- #
def create_inverted_index(products, field):
    """Creates an inverted index mapping words in a given field (title, description) to product URLs."""
    index = defaultdict(list)
    for product in products:
        product_url = product.get("url", "")
        if product_url and field in product:
            tokens = tokenize(product[field])
            for token in tokens:
                index[token].append(product_url)
    return index


# ---------------------- Create Reviews Index ---------------------- #
def create_reviews_index(products):
    """Creates an index storing the total number of reviews, average rating, and latest rating per product."""
    index = {}
    for product in products:
        product_url = product.get("url", "")
        if product_url and "product_reviews" in product:
            reviews = product["product_reviews"]
            scores = [
                review.get("rating", 0) for review in reviews if "rating" in review
            ]
            if scores:
                index[product_url] = {
                    "total_reviews": len(scores),
                    "average_score": sum(scores) / len(scores),
                    "latest_score": scores[-1],  # Most recent review score
                }
    return index


# ---------------------- Create Feature Index ---------------------- #
def create_feature_index(products, feature):
    """Creates an inverted index mapping feature values (e.g., brand, made in) to product URLs."""
    index = defaultdict(list)
    for product in products:
        product_url = product.get("url", "")
        if (
            product_url
            and "product_features" in product
            and feature in product["product_features"]
        ):
            tokens = tokenize(product["product_features"][feature])
            for token in tokens:
                index[token].append(product_url)
    return index


# ---------------------- Create Positional Index ---------------------- #
def create_positional_index(products, field):
    """Creates an inverted index that stores word positions in the given field."""
    index = defaultdict(lambda: defaultdict(list))
    for product in products:
        product_url = product.get("url", "")
        if product_url and field in product:
            tokens = tokenize(product[field])
            for pos, token in enumerate(tokens):
                index[token][product_url].append(pos)
    return index


# ---------------------- Save Indexes to JSON ---------------------- #
def save_index(index, filename, overwrite=False):
    """Saves an index to a JSON file, ensuring it doesn't overwrite existing files unless specified."""
    if os.path.exists(filename) and not overwrite:
        raise FileExistsError(
            f"The file '{filename}' already exists. Use `overwrite=True` to overwrite it."
        )
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
    print(f"Index saved to {filename}")


# ---------------------- Main Execution ---------------------- #
if __name__ == "__main__":
    INPUT_FILE = "TP2/products.jsonl"
    OUTPUT_DIR = "TP2/indexes"
    FEATURES_OUTPUT_DIR = "TP2/indexes/features"
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists
    os.makedirs(FEATURES_OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists

    print("Loading products...")
    products = load_products(INPUT_FILE)

    print("Creating indexes...")
    title_index = create_inverted_index(products, "title")
    description_index = create_inverted_index(products, "description")
    title_pos_index = create_positional_index(products, "title")
    description_pos_index = create_positional_index(products, "description")
    reviews_index = create_reviews_index(products)

    # Creating indexes for the features
    list_features = [
        "brand",
        "made in",
        "flavor",
        "sugar_content",
        "material",
        "care instructions",
        "sizes",
        "design",
        "colors",
        "light",
        "closure",
        "comfort",
        "purpose",
        "versatility",
        "durability",
    ]
    print("Saving indexes...")

    save_index(
        title_index, os.path.join(OUTPUT_DIR, "title_index.json"), overwrite=True
    )
    save_index(
        description_index,
        os.path.join(OUTPUT_DIR, "description_index.json"),
        overwrite=True,
    )
    save_index(
        title_pos_index,
        os.path.join(OUTPUT_DIR, "title_pos_index.json"),
        overwrite=True,
    )
    save_index(
        description_pos_index,
        os.path.join(OUTPUT_DIR, "description_pos_index.json"),
        overwrite=True,
    )
    save_index(
        reviews_index, os.path.join(OUTPUT_DIR, "reviews_index.json"), overwrite=True
    )

    for feature in list_features:
        feature_index = create_feature_index(products, feature)
        save_index(
            feature_index,
            os.path.join(FEATURES_OUTPUT_DIR, f"{feature}_index.json"),
            overwrite=True,
        )

    print("Indexing completed successfully!")
