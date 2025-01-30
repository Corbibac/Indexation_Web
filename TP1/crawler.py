from TP1.extraction import (
    is_allowed_to_crawl,
    polite_request,
    parse_html,
    extract_page_info,
    add_url_to_queue,
)
from urllib.parse import urljoin


def crawl_url(url, visited, priority_queue, normal_queue, robots_txt_url):
    """Gère le crawling d'une URL et l'ajoute aux files d'attente selon sa priorité."""
    if not is_allowed_to_crawl(url, robots_txt_url):
        print(f"L'accès à {url} est interdit par robots.txt.")
        return None
    response = polite_request(url)
    if response:
        soup = parse_html(response.text)
        page_info = extract_page_info(soup, url)
        visited.add(url)  # Marquer l'URL comme visitée
        for link in page_info["links"]:
            add_url_to_queue(
                link, visited, priority_queue, normal_queue
            )  # Ajout des liens dans la bonne file
        return page_info
    return None


# Logique principale du crawler
def crawl(start_url, max_pages):
    """Exécute le crawler en respectant la priorité des liens 'product'."""
    robots_txt_url = urljoin(start_url, "/robots.txt")
    visited = set()
    priority_queue = [start_url]  # Pile des liens prioritaires (product)
    normal_queue = []  # Pile des autres liens
    results = []

    while (priority_queue or normal_queue) and len(visited) < max_pages:
        # On explore d'abord la pile prioritaire, puis la pile normale
        if priority_queue:
            current_url = priority_queue.pop(0)
        else:
            current_url = normal_queue.pop(0)

        print(f"Crawling : {current_url}")
        page_info = crawl_url(
            current_url, visited, priority_queue, normal_queue, robots_txt_url
        )

        if page_info:
            results.append(
                {
                    "title": page_info["title"],
                    "url": current_url,
                    "first_paragraph": page_info["first_paragraph"],
                    "links": page_info["links"],
                }
            )
    print("Crawling terminé")
    return results
