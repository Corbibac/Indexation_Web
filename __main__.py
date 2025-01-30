# # Clément Mounier

# # TP1
# from TP1.crawler import crawl
# from TP1.save_json import save_results_to_json

# # Exécution du script du TP1
# if __name__ == "__main__":
#     start_url = "https://web-scraping.dev/products"
#     max_pages = 50
#     output_file = "crawler_results.json"

#     results = crawl(start_url, max_pages)
#     save_results_to_json(results, output_file, overwrite=True)
# # Testé avec web-scraping.dev/products et ensai.fr sans problème.

# TP2

import os
from TP2.loadings import load_products, load_stopwords
from TP2.indexes_creation import (
    create_feature_index,
    create_inverted_index,
    create_positional_index,
    create_reviews_index,
)
from TP2.save_indexes import save_index

# Load the stopwords from the provided file
stopwords = load_stopwords("TP2/stopwords-en.txt")

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
    title_index = create_inverted_index(products, "title", stopwords)
    description_index = create_inverted_index(products, "description", stopwords)
    title_pos_index = create_positional_index(products, "title", stopwords)
    description_pos_index = create_positional_index(products, "description", stopwords)
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

    list_non_features_to_save = [
        "title",
        "description",
        "title_pos",
        "description_pos",
        "reviews",
    ]

    for non_features in list_non_features_to_save:
        save_index(
            eval(f"{non_features}_index"),
            os.path.join(OUTPUT_DIR, f"{non_features}_index.json"),
            overwrite=True,
        )

    for feature in list_features:
        feature_index = create_feature_index(products, feature, stopwords)
        save_index(
            feature_index,
            os.path.join(FEATURES_OUTPUT_DIR, f"{feature}_index.json"),
            overwrite=True,
        )

    print("Indexing completed successfully!")
