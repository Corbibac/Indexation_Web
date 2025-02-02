# # Clément Mounier


# ---------------------- TP1 ---------------------- #

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

###################################

# ---------------------- TP2 ---------------------- #


# import os
# from TP2.loadings import load_products, load_stopwords
# from TP2.indexes_creation import (
#     create_feature_index,
#     create_inverted_index,
#     create_positional_index,
#     create_reviews_index,
# )
# from TP2.save_indexes import save_index
# from TP2.extract_features import extract_unique_features


# ---------------------- Main Execution ---------------------- #
# if __name__ == "__main__":
#     INPUT_FILE = "TP2/products.jsonl"
#     OUTPUT_DIR = "TP2/indexes"
#     FEATURES_OUTPUT_DIR = f"{OUTPUT_DIR}/features"
#     INPUT_STOPWORDS = "TP2/stopwords-en.txt"
#     os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists
#     os.makedirs(FEATURES_OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists

#     # Load the stopwords from the provided file
#     print("Loading stopwords...")
#     stopwords = load_stopwords(INPUT_STOPWORDS)

#     print("Loading products...")
#     products = load_products(INPUT_FILE)

#     print("Creating indexes...")
#     title_index = create_inverted_index(products, "title", stopwords)
#     description_index = create_inverted_index(products, "description", stopwords)
#     title_pos_index = create_positional_index(products, "title", stopwords)
#     description_pos_index = create_positional_index(products, "description", stopwords)
#     reviews_index = create_reviews_index(products)

#     # Creating indexes for the features
#     list_features = extract_unique_features(INPUT_FILE)
#     print("Saving indexes...")

#     list_non_features_to_save = [
#         "title",
#         "description",
#         "title_pos",
#         "description_pos",
#         "reviews",
#     ]

#     for non_features in list_non_features_to_save:
#         save_index(
#             eval(f"{non_features}_index"),
#             os.path.join(OUTPUT_DIR, f"{non_features}_index.json"),
#             overwrite=True,
#         )

#     for feature in list_features:
#         feature_index = create_feature_index(products, feature, stopwords)
#         save_index(
#             feature_index,
#             os.path.join(FEATURES_OUTPUT_DIR, f"{feature}_index.json"),
#             overwrite=True,
#         )

#     print("Indexing completed successfully!")


# ---------------------- TP3 ---------------------- #

import os

from TP3.loadings import load_json, load_indexes
from TP3.search import search
from TP3.documents_length import build_doc_data, compute_avgdl_per_field
from TP3.save_query import save_query_results

if __name__ == "__main__":

    field_weights = {
        "title": 3.0,
        "description": 1.0,
        "brand": 2.0,  # brand not used right now
        "origin": 2.0,
        # you can add more fields if you have them
    }
    # Adjust these paths according to your local file structure
    DATA_FOLDER = "TP3/data"
    INDEX_FOLDER = os.path.join(DATA_FOLDER, "indexes")
    SYNONYMS_FILE = os.path.join(DATA_FOLDER, "synonyms/origin_synonyms.json")

    QUERY_RESULTS_FILE = "query_result.json"

    # 1) Build doc_data from your JSONL
    doc_data = build_doc_data("TP3/data/rearranged_products.jsonl")

    # 2) Compute average doc length per field
    fields = ["title", "description", "brand", "origin"]
    avgdl = compute_avgdl_per_field(doc_data, fields)

    print("Loading indexes...")
    indexes = load_indexes(INDEX_FOLDER)

    # To fully work with indexes instead of the "build_doc_data" dictionary, you can use this function:
    #    doc_data = build_doc_data_from_indexes(indexes)

    print("Loading synonyms...")
    synonyms = load_json(SYNONYMS_FILE)

    print("Ready to search.")
    query_input = input("Enter your search query: ")

    # Example usage:
    # Choose the filtering mode: "any" (OR) or "all" (AND)
    mode = "any"  # or "all"
    results_data = search(
        query_input,
        indexes,
        synonyms,
        doc_data,
        avgdl,
        field_weights,
        filter_mode=mode,
    )

    # Print top 10 results
    print("\n=== Search Results ===")
    print(f"Total documents in the corpus: {results_data['total_documents']}")
    print(f"Documents after filtering: {results_data['filtered_documents']}\n")

    for i, res in enumerate(results_data["results"][:10], 1):
        print(
            f"{i}. Title: {res['title']}\n"
            f"   URL: {res['url']}\n"
            f"   Score: {res['score']}\n"
            f"   Description: {res['description'][:100]}...\n"
        )

    # If you want a JSON dump of the final results:
    # import json
    # print(json.dumps(results_data, indent=2))

    # saving the queries
    save_query_results(query_input, results_data, QUERY_RESULTS_FILE)
