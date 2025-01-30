import json
import os


def load_json(filepath):
    """
    Loads a JSON file and returns its content.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(filepath):
    """
    Loads a JSONL file and returns a list of its content.
    """
    data = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data


def load_indexes(index_folder):
    """
    Loads all JSON index files from the specified folder into a dictionary.

    Each file name (without extension) becomes the index key,
    and the loaded JSON becomes the value.

    Example:
        index_folder/
            title_index.json
            description_index.json
            reviews_index.json
            ...
        => {
            "title_index": {...},
            "description_index": {...},
            "reviews_index": {...}
        }
    """
    indexes = {}
    for filename in os.listdir(index_folder):
        if filename.endswith(".json"):
            index_name = filename.replace(".json", "")
            full_path = os.path.join(index_folder, filename)
            indexes[index_name] = load_json(full_path)
    return indexes
