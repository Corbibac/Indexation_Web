from TP2.my_tokenizer import my_tokenizer
from collections import defaultdict


# ---------------------- Create Inverted Index ---------------------- #
def create_inverted_index(products, field, stopwords):
    """Creates an inverted index mapping words in a given field (title, description) to product URLs."""
    index = defaultdict(list)
    for product in products:
        product_url = product.get("url", "")
        if product_url and field in product:
            tokens = my_tokenizer(product[field], stopwords)
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
def create_feature_index(products, feature, stopwords):
    """Creates an inverted index mapping feature values (e.g., brand, made in) to product URLs."""
    index = defaultdict(list)
    for product in products:
        product_url = product.get("url", "")
        if (
            product_url
            and "product_features" in product
            and feature in product["product_features"]
        ):
            tokens = my_tokenizer(product["product_features"][feature], stopwords)
            for token in tokens:
                index[token].append(product_url)
    return index


# ---------------------- Create Positional Index ---------------------- #
def create_positional_index(products, field, stopwords):
    """Creates an inverted index that stores word positions in the given field."""
    index = defaultdict(lambda: defaultdict(list))
    for product in products:
        product_url = product.get("url", "")
        if product_url and field in product:
            tokens = my_tokenizer(product[field], stopwords)
            for pos, token in enumerate(tokens):
                index[token][product_url].append(pos)
    return index
