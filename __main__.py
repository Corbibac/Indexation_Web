# Clément Mounier

# TP1
from TP1.crawler import crawl
from TP1.save_json import save_results_to_json

# Exécution du script du TP1
if __name__ == "__main__":
    start_url = "https://web-scraping.dev/products"
    max_pages = 50
    output_file = "crawler_results.json"

    results = crawl(start_url, max_pages)
    save_results_to_json(results, output_file, overwrite=True)
# Testé avec web-scraping.dev/products et ensai.fr sans problème.

# TP2
