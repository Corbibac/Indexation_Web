from TP3.tokenize import tokenize
from TP3.expand_query import expand_query
from TP3.filters import filter_docs_any_token, filter_docs_all_tokens
from TP3.rank import rank_documents


def search(query, indexes, synonyms, doc_data, avgdl, field_weights, filter_mode="any"):
    """
    Execute the entire search process:
    1. Tokenize the query
    2. Expand it with synonyms
    3. Filter documents (either 'any' or 'all' modes)
    4. Rank them
    5. Format final results

    Return a dictionary with:
    {
      "total_documents": number of docs in the corpus (if known),
      "filtered_documents": number of docs passing the filter,
      "results": [
         {
           "url": doc_id,
           "title": ...,
           "description": ...,
           "score": ...
         },
         ...
      ]
    }
    """
    # 1) Tokenize
    query_tokens = tokenize(query)

    # 2) Expand with synonyms if available
    expanded_tokens = expand_query(query_tokens, synonyms)

    # 3) Filter documents based on 'any' or 'all' presence of tokens
    if filter_mode == "all":
        filtered_docs = filter_docs_all_tokens(expanded_tokens, indexes)
    else:
        filtered_docs = filter_docs_any_token(expanded_tokens, indexes)

    # 4) Rank documents (using multi-field BM25)
    #    rank_documents internally calls compute_bm25(..., doc_data, avgdl, field_weights)
    ranked = rank_documents(
        filtered_docs, expanded_tokens, indexes, doc_data, avgdl, field_weights
    )

    # 5) Format final results
    # If you store total doc count in indexes["total_docs"], use that;
    # otherwise, default to the size of doc_data (the raw dataset).
    total_docs = indexes.get("total_docs", len(doc_data))

    results_list = []
    for doc_id, score in ranked:
        # Retrieve fields from doc_data
        info = doc_data.get(doc_id, {})
        doc_title = info.get("title", "Unknown Title")
        doc_description = info.get("description", "No description available")

        results_list.append(
            {
                "url": doc_id,
                "title": doc_title,
                "description": doc_description,
                "score": round(score, 2),
            }
        )

    return {
        "total_documents": total_docs,
        "filtered_documents": len(ranked),
        "results": results_list,
    }
