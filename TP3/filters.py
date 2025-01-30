from collections import defaultdict

from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))


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
    # Can adapt the fields in which we want to check tokens
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
    """
    query_tokens = [t for t in query_tokens if t not in STOPWORDS]
    if not query_tokens:
        return {}

    fields_to_check = ["title_index", "description_index", "origin_index", "brand"]
    docs_for_each_token = []

    for token in query_tokens:
        doc_ids_for_token = set()
        for field in fields_to_check:
            if field in indexes and token in indexes[field]:
                doc_list_or_dict = indexes[field][token]

                # Check if it’s a dict or a list
                if isinstance(doc_list_or_dict, dict):
                    # Old approach
                    doc_ids_for_token.update(doc_list_or_dict.keys())
                elif isinstance(doc_list_or_dict, list):
                    # Just add them directly
                    doc_ids_for_token.update(doc_list_or_dict)
                else:
                    # Unexpected structure -> skip or handle differently
                    pass

        if not doc_ids_for_token:
            # If no docs for a particular token, no doc can match all
            return {}
        docs_for_each_token.append(doc_ids_for_token)

    # Intersect them all
    docs_with_all_tokens = set.intersection(*docs_for_each_token)

    # Build your result
    return {doc_id: len(query_tokens) for doc_id in docs_with_all_tokens}
