import json
import os


def save_query_results(query_str, results_data, QUERY_RESULTS_FILE):
    """
    Save the search results to query_result.json, assigning an auto-incremented ID.
    """

    # 1) Load existing data from file, or create empty list if the file doesn't exist
    if os.path.exists(QUERY_RESULTS_FILE):
        with open(QUERY_RESULTS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    if not isinstance(data, list):
        # If file structure isn't a list, reset to an empty list
        data = []

    # 2) Determine the next ID
    next_id = len(data) + 1

    # 3) Build the record to store
    # You can store any fields you want (the entire results_data, the query, etc.)
    record = {
        "id": next_id,
        "query": query_str,
        "results_data": results_data,  # this includes total_docs, filtered_docs, results...
    }

    # 4) Append and save back to file
    data.append(record)
    with open(QUERY_RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved query #{next_id} to {QUERY_RESULTS_FILE}")
