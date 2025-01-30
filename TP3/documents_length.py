import json
import re
import nltk
from nltk.corpus import stopwords
from TP3.tokenize import tokenize
from TP3.loadings import load_jsonl

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))


def build_doc_data(jsonl_filepath):
    """
    Reads `rearranged_products.jsonl` and returns a dictionary:
      doc_data[doc_url] = {
          "title": <str>,
          "description": <str>,
          "brand": <str> or None,
          "origin": <str> or None,
          ...
      }
    You can store additional fields if desired.
    """
    raw_data = load_jsonl(jsonl_filepath)
    doc_data = {}

    for entry in raw_data:
        url = entry.get("url", "")

        # Extract fields safely
        title = entry.get("title", "")
        description = entry.get("description", "")
        product_features = entry.get("product_features", {})

        # brand and origin might be found in product_features
        brand = product_features.get("brand", "")
        origin = product_features.get(
            "made in", ""
        )  # or "origin" if your data uses that key

        doc_data[url] = {
            "title": title,
            "description": description,
            "brand": brand,
            "origin": origin,
        }

    return doc_data


def compute_avgdl_per_field(doc_data, fields):
    """
    For each field, compute the average document length across all docs.
    Returns a dict: avgdl[field] = average_length.

    doc_data[doc_id][field] is the raw text. We'll tokenize to find length.
    """
    # Initialize counters
    total_length_per_field = {field: 0 for field in fields}
    doc_count = 0

    for doc_id, content in doc_data.items():
        doc_count += 1
        for field in fields:
            text = content.get(field, "")
            tokens = tokenize(text)
            total_length_per_field[field] += len(tokens)

    avgdl = {}
    for field in fields:
        if doc_count > 0:
            avgdl[field] = total_length_per_field[field] / doc_count
        else:
            avgdl[field] = 1  # fallback
    return avgdl
