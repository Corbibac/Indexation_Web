import re


# ---------------------- Extract Product ID and Variant ---------------------- #
def extract_product_id(url):
    """Extracts the product ID and variant from a product URL, if present."""
    match = re.search(r"/product/(\d+)(?:\?variant=(\w+))?", url)
    if match:
        return match.group(1), match.group(2) if match.group(2) else None
    return None, None
