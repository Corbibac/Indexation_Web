from TP3.scores import compute_bm25, compute_linear_score


def rank_documents(
    filtered_docs, query_tokens, indexes, doc_data, avgdl, field_weights
):
    """
    :param filtered_docs: dict { doc_id: matched_token_count } from a filter step
    :param query_tokens: list of tokens (expanded + tokenized)
    :param indexes: the dictionary containing your multiple indexes
    :param doc_data: dict of doc_id -> field texts (from rearranged_products.jsonl)
    :param avgdl: dict of average doc length per field
    :param field_weights: dict, e.g. {"title":1.0, "description":1.0, "brand":0.5, "origin":1.0}
    :return: list of (doc_id, final_score) sorted desc
    """
    results = []
    for doc_id in filtered_docs:
        # BM25 across multiple fields
        bm25_score = compute_bm25(
            query_tokens=query_tokens,
            doc_id=doc_id,
            indexes=indexes,
            doc_data=doc_data,
            avgdl=avgdl,
            field_weights=field_weights,
        )

        # We could add more signals here, just didn't have the time to think of many interesting ones.
        # Maybe a signal based on the number of query tokens that appear in the title?
        # Or based on the number of tokens in the query, making smaller queries more relevant?
        linear_score = compute_linear_score(doc_id, query_tokens, indexes)

        final_score = bm25_score * 1.5 + linear_score

        results.append((doc_id, final_score))

    # Sort descending by score
    results.sort(key=lambda x: x[1], reverse=True)
    return results
