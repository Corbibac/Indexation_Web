import os
import json


# ---------------------- Save Indexes to JSON ---------------------- #
def save_index(index, filename, overwrite=False):
    """Saves an index to a JSON file, ensuring it doesn't overwrite existing files unless specified."""
    if os.path.exists(filename) and not overwrite:
        raise FileExistsError(
            f"The file '{filename}' already exists. Use `overwrite=True` to overwrite it."
        )
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
    print(f"Index saved to {filename}")
