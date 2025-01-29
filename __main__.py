# TP1
from TP1.crawler import crawl
from TP1.save_json import save_results_to_json

# Exécution du script du TP1
if __name__ == "__main__":
    START_URL = "https://web-scraping.dev/products"
    MAX_PAGES = 50
    OUTPUT_FILE = "crawler_results.json"

    results = crawl(START_URL, MAX_PAGES)
    save_results_to_json(results, OUTPUT_FILE, overwrite=True)
