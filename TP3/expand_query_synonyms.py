def expand_query(query_tokens, synonyms):
    """
    Expands the query tokens with any synonyms.
    synonyms should be a dict like:
        {
            "france": ["french", "fr"],
            "spain": ["espagne", ...]
            ...
        }
    If a query token is found as a key in synonyms,
    add all synonyms to the set of tokens.

    Returns a list of expanded tokens.
    """
    expanded = set(query_tokens)
    for token in query_tokens:
        if token in synonyms:
            expanded.update(synonyms[token])
    return list(expanded)
