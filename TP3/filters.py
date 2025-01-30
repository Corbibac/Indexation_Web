from collections import defaultdict


def filter_docs_any_token(query_tokens, indexes):
    """
    Filter documents: keep those that have AT LEAST ONE of the query_tokens
    (OR-based filtering).

    indexes is expected to have the typical structure, e.g.:
        {
            "title_index": { token: { doc_id: ... }, ... },
            "description_index": { token: { doc_id: ... }, ... },
            ...
        }
    Returns a dict: { doc_id: matched_token_count }
    """
    relevant_docs = defaultdict(int)

    # We look in multiple fields (title, description, possibly origin, etc.)
    # You can adapt the fields in which you want to check tokens
    fields_to_check = [
        "title_index",
        "description_index",
        "origin_index",
        "brand_index",
    ]

    for token in query_tokens:
        for field in fields_to_check:
            if field in indexes and token in indexes[field]:
                docs_for_token = indexes[field][token]
                for doc_id in docs_for_token:
                    # Increase count to reflect how many tokens matched
                    # (not mandatory, but can be useful)
                    relevant_docs[doc_id] += 1

    return relevant_docs


def filter_docs_all_tokens(query_tokens, indexes):
    """
    Filter documents: keep those that contain ALL tokens in query_tokens
    (AND-based filtering), ignoring stopwords.

    Returns a dict: { doc_id: matched_token_count } for those that match all tokens.
    """
    # Remove stopwords from query_tokens (optional, but often recommended)
    query_tokens = [t for t in query_tokens if t not in STOPWORDS]
    if not query_tokens:
        return {}

    # We'll do an intersection across sets of docs for each token
    fields_to_check = ["title_index", "description_index", "origin_index", "brand"]
    # For each token, we build a set of doc_ids
    docs_for_each_token = []

    for token in query_tokens:
        doc_ids_for_token = set()
        for field in fields_to_check:
            if field in indexes and token in indexes[field]:
                doc_ids_for_token.update(indexes[field][token].keys())

        if not doc_ids_for_token:
            # If no docs for a particular token, no doc can match all tokens
            return {}
        docs_for_each_token.append(doc_ids_for_token)

    # Intersect them all to get docs that have all tokens
    docs_with_all_tokens = set.intersection(*docs_for_each_token)

    # We also keep a count of how many tokens matched (which should be the length of query_tokens)
    result = {}
    for doc_id in docs_with_all_tokens:
        result[doc_id] = len(query_tokens)
    return result
