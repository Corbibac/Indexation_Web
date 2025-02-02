import collections
import nltk
from nltk.corpus import stopwords
from TP3.tokenize import tokenize
from TP3.loadings import load_jsonl

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))


# Should preferrably use the indexes instead of creating another dict.
# It's for sure repetitive and suboptimal.
# However it has its use to fully display the documents information (title/descritpion)
# Under I provide "build_doc_data_from_indexes" a function that only uses the indexes.
# We don't use it in the end cause it's not optimal user wise. The use wants to see the full description with all words.
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
    Can store additional fields if desired.
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


def build_doc_data_from_indexes(indexes):
    """
    Build a pseudo doc_data from the existing indexes.
    doc_data[doc_id] = {
      "title": (reconstructed from token positions in title_index),
      "description": (reconstructed from token positions in description_index),
      "brand": (detected brand token(s)),
      "origin": (detected origin token(s))
    }

    Note: This won't perfectly match original texts because we only
          have token->positions, not full raw strings.
    """

    # Collect all doc_ids we see in any index
    all_doc_ids = set()

    # We'll track tokens+positions for title and description
    # e.g. title_tokens_positions[doc_id] = [(pos, token), (pos2, token2), ...]
    title_tokens_positions = collections.defaultdict(list)
    desc_tokens_positions = collections.defaultdict(list)

    # brand_map[doc_id] = set of detected brand tokens
    brand_map = collections.defaultdict(set)
    # origin_map[doc_id] = set of detected origin tokens
    origin_map = collections.defaultdict(set)

    # 1) Reconstruct "title" from title_index
    if "title_index" in indexes:
        for token, doc_dict_or_list in indexes["title_index"].items():
            if isinstance(doc_dict_or_list, dict):
                # { doc_id: [positions], ... }
                for doc_id, positions in doc_dict_or_list.items():
                    all_doc_ids.add(doc_id)
                    if isinstance(positions, list):
                        # Add each position and the token
                        for pos in positions:
                            title_tokens_positions[doc_id].append((pos, token))
                    else:
                        # If it's an int or something else, treat freq or single pos
                        title_tokens_positions[doc_id].append((0, token))
            elif isinstance(doc_dict_or_list, list):
                # just a list of docs => no position data
                for doc_id in doc_dict_or_list:
                    all_doc_ids.add(doc_id)
                    # We'll store token with some default position 0
                    title_tokens_positions[doc_id].append((0, token))

    # 2) Reconstruct "description" from description_index
    if "description_index" in indexes:
        for token, doc_dict_or_list in indexes["description_index"].items():
            if isinstance(doc_dict_or_list, dict):
                for doc_id, positions in doc_dict_or_list.items():
                    all_doc_ids.add(doc_id)
                    if isinstance(positions, list):
                        for pos in positions:
                            desc_tokens_positions[doc_id].append((pos, token))
                    else:
                        desc_tokens_positions[doc_id].append((0, token))
            elif isinstance(doc_dict_or_list, list):
                for doc_id in doc_dict_or_list:
                    all_doc_ids.add(doc_id)
                    desc_tokens_positions[doc_id].append((0, token))

    # 3) Detect brand(s) from brand_index
    if "brand_index" in indexes:
        for brand_token, doc_list_or_dict in indexes["brand_index"].items():
            if isinstance(doc_list_or_dict, dict):
                # doc_list_or_dict => { doc_id: [positions], ... } or frequency
                for doc_id in doc_list_or_dict.keys():
                    all_doc_ids.add(doc_id)
                    brand_map[doc_id].add(brand_token)
            elif isinstance(doc_list_or_dict, list):
                # doc_list_or_dict => [doc_id, doc_id, ...]
                for doc_id in doc_list_or_dict:
                    all_doc_ids.add(doc_id)
                    brand_map[doc_id].add(brand_token)

    # 4) Detect origin(s) from origin_index
    if "origin_index" in indexes:
        for origin_token, doc_list_or_dict in indexes["origin_index"].items():
            if isinstance(doc_list_or_dict, dict):
                for doc_id in doc_list_or_dict.keys():
                    all_doc_ids.add(doc_id)
                    origin_map[doc_id].add(origin_token)
            elif isinstance(doc_list_or_dict, list):
                for doc_id in doc_list_or_dict:
                    all_doc_ids.add(doc_id)
                    origin_map[doc_id].add(origin_token)

    # Build final doc_data
    doc_data = {}
    for doc_id in all_doc_ids:
        # Reconstruct a minimal title
        t_positions = title_tokens_positions[doc_id]
        # sort by position
        t_positions.sort(key=lambda x: x[0])
        # join tokens
        reconstructed_title = (
            " ".join(token for pos, token in t_positions) if t_positions else ""
        )

        # Reconstruct a minimal description
        d_positions = desc_tokens_positions[doc_id]
        d_positions.sort(key=lambda x: x[0])
        reconstructed_desc = (
            " ".join(token for pos, token in d_positions) if d_positions else ""
        )

        # Combine brand tokens
        brand_str = ", ".join(sorted(brand_map[doc_id])) if brand_map[doc_id] else ""

        # Combine origin tokens
        origin_str = ", ".join(sorted(origin_map[doc_id])) if origin_map[doc_id] else ""

        doc_data[doc_id] = {
            "title": reconstructed_title if reconstructed_title else "Unknown Title",
            "description": (
                reconstructed_desc if reconstructed_desc else "No description"
            ),
            "brand": brand_str,
            "origin": origin_str,
        }

    return doc_data
