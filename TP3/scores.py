import math

from TP3.tokenize import tokenize

FIELD_INDEX_MAP = {
    "title": "title_index",
    "description": "description_index",
    "brand": "brand_index",
    "origin": "origin_index",
}


def compute_bm25(
    query_tokens, doc_id, indexes, doc_data, avgdl, field_weights, k1=1.5, b=0.75
):
    """
    Compute BM25 across multiple fields, each with its own weight.

    :param query_tokens: list of query terms.
    :param doc_id: the document identifier (e.g. the URL).
    :param indexes: a dict containing your different field indexes:
                    {
                      "title_index": {... or ...},
                      "description_index": {... or ...},
                      "brand_index": {... or ...},
                      "origin_index": {... or ...},
                      ...
                    }
    :param doc_data: dictionary with doc_id -> {field -> raw text}
    :param avgdl: dict with average doc length per field: avgdl[field] = float
    :param field_weights: dict with the weight for each field. E.g. {"title":1.0, "description":1.0, "brand":0.0, ...}
    :param k1, b: BM25 parameters
    :return: float BM25 score.
    """
    # Use total_docs if stored; otherwise compute from one of the indexes
    if "total_docs" not in indexes:
        if "title_index" in indexes and indexes["title_index"]:
            all_doc_ids = set()
            for token_dict in indexes["title_index"].values():
                # token_dict might be a dict or a list
                if isinstance(token_dict, dict):
                    all_doc_ids.update(token_dict.keys())
                elif isinstance(token_dict, list):
                    all_doc_ids.update(token_dict)
            total_docs = len(all_doc_ids)
        else:
            total_docs = 1
    else:
        total_docs = indexes["total_docs"]

    score = 0.0

    # Go through each field
    for field, weight in field_weights.items():
        if weight <= 0.0:
            continue

        # Get the index name for this field (e.g. "title_index")
        index_name = FIELD_INDEX_MAP.get(field)
        if not index_name or index_name not in indexes:
            continue

        # doc_length for this doc's field
        field_text = doc_data.get(doc_id, {}).get(field, "")
        doc_length = len(tokenize(field_text))
        if doc_length == 0:
            doc_length = 1  # avoid zero in the denominator

        # average length for this field
        avgdl_field = avgdl.get(field, 1.0)

        # For each token in the query
        for token in query_tokens:
            # If token doesn't exist in the field index, skip
            if token not in indexes[index_name]:
                continue

            # docs_with_token might be either:
            # a) dict {doc_id: positions/freq, ...}  or
            # b) list of doc_ids
            docs_with_token = indexes[index_name][token]

            if isinstance(docs_with_token, dict):
                # Data structure: token -> { doc_id -> [positions] or freq }
                df = len(docs_with_token)  # how many docs have this token
                freq_object = docs_with_token.get(doc_id, [])
                if isinstance(freq_object, list):
                    tf = len(freq_object)  # number of positions
                elif isinstance(freq_object, (int, float)):
                    tf = float(freq_object)
                else:
                    tf = 0.0
            elif isinstance(docs_with_token, list):
                # Data structure: token -> [doc_id, doc_id, ...]
                # => presence means tf=1, absence means tf=0
                df = len(docs_with_token)  # doc frequency
                tf = 1.0 if doc_id in docs_with_token else 0.0
            else:
                # Unexpected structure => skip scoring
                continue

            # Compute IDF
            idf = math.log((total_docs - df + 0.5) / (df + 0.5) + 1)

            # BM25 partial
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (doc_length / avgdl_field))
            bm25_partial = idf * (numerator / denominator) if denominator != 0 else 0.0

            # Multiply by field weight
            score += weight * bm25_partial

    return score


def compute_linear_score(doc_id, query_tokens, indexes):
    """
    Example of a simpler linear combination of signals:
     - presence in title
     - presence in description
     - average review score
     - exact match in product origin (if relevant)
     - etc.

    Adjust the weights, signals, and logic as you see fit.
    """
    score = 0.0

    # 1) Count how many query tokens appear in the title
    title_hits = 0
    if "title_index" in indexes:
        for token in query_tokens:
            if (
                token in indexes["title_index"]
                and doc_id in indexes["title_index"][token]
            ):
                title_hits += 1
    score += 2.0 * title_hits  # Weighted, for example

    # 2) Count how many query tokens appear in the description
    desc_hits = 0
    if "description_index" in indexes:
        for token in query_tokens:
            if (
                token in indexes["description_index"]
                and doc_id in indexes["description_index"][token]
            ):
                desc_hits += 1
    score += 1.0 * desc_hits

    # 3) Average review score (if available in "reviews_index")
    avg_review = 0
    if "reviews_index" in indexes and doc_id in indexes["reviews_index"]:
        # Suppose indexes["reviews_index"][doc_id] = {"average_score": 4.5, "count": 100}
        avg_review = float(indexes["reviews_index"][doc_id].get("average_score", 0.0))
    score += avg_review  # direct addition, or maybe apply a factor

    # 4) Exact origin match (if your synonyms or query mention something about origin)
    # For demonstration, if there's an "origin_index" or if the doc has a known origin
    # you'd do something like:
    origin_boost = 0
    # If the doc has "france" in origin, and the query also has "france", give a boost
    # This depends heavily on how your origin is indexed.
    # Example:
    if "origin_index" in indexes:
        for token in query_tokens:
            if (
                token in indexes["origin_index"]
                and doc_id in indexes["origin_index"][token]
            ):
                origin_boost += 3.0  # arbitrary
    score += origin_boost

    return score
