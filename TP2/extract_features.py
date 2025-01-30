import json


def extract_unique_features(jsonl_file):
    """Extracts all unique feature keys from product_features in a JSONL file."""
    unique_features = set()

    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            product = json.loads(line.strip())
            if "product_features" in product:
                unique_features.update(product["product_features"].keys())

    return sorted(unique_features)
