import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


# Configuration initiale
def is_allowed_to_crawl(url, robots_txt_url):
    """Vérifie si le crawler est autorisé à accéder à une page via robots.txt."""
    try:
        robots_txt = requests.get(robots_txt_url).text
        if "Disallow" in robots_txt:
            disallowed_paths = [
                line.split(":")[1].strip()
                for line in robots_txt.split("\n")
                if line.startswith("Disallow")
            ]
            for path in disallowed_paths:
                if urlparse(url).path.startswith(path):
                    return False
        return True
    except Exception as e:
        print(f"Erreur en vérifiant robots.txt : {e}")
        return False


def polite_request(url, delay=1):
    """Effectue une requête HTTP avec un délai pour respecter la politesse."""
    time.sleep(delay)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")
        return None


# Extraction du contenu
def parse_html(content):
    """Parse le contenu HTML et retourne un objet BeautifulSoup."""
    return BeautifulSoup(content, "html.parser")


def extract_page_info(soup, base_url):
    """Extrait le titre, le premier paragraphe et les liens pertinents d'une page, en priorisant les pages 'product'."""
    title = soup.title.string.strip() if soup.title else "Titre non disponible"
    paragraph = soup.find("p").text.strip() if soup.find("p") else ""

    # Priorité aux liens contenant 'product'
    links = [urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True)]
    product_links = [link for link in links if "product" in link]
    other_links = [link for link in links if "product" not in link]

    # Retourne d'abord les liens 'product', puis les autres
    prioritized_links = product_links + other_links

    return {
        "title": title,
        "first_paragraph": paragraph,
        "links": prioritized_links,  # Les liens sont triés avec priorité
    }


# Gestion des URLs
def add_url_to_queue(url, visited, priority_queue, normal_queue):
    """Ajoute une URL à la file d'attente appropriée (prioritaire ou normale) si elle n'a pas été visitée."""
    if url not in visited and url not in priority_queue and url not in normal_queue:
        if "product" in url:  # Les liens avec 'product' vont dans la pile prioritaire
            priority_queue.append(url)
        else:  # Les autres liens vont dans la pile normale
            normal_queue.append(url)
