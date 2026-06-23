from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, Tag

def normalize_url(url: str) -> str:
    o = urlsplit(url)
    return o.netloc + o.path.rstrip("/")
"""
def normalize_url(url):
    if url.startswith("http://"):
        url = url[len("http://"):]
    elif url.startswith("https://"):
        url = url[len("https://"):]
    if url.endswith("/"):
        url = url[:-1]
    return url

def get_heading_from_html(html: str) -> list:
    text = BeautifulSoup(html, "html.parser")
    if text.h1 != None and text.h1 != "":
        return [text.h1.get_text()]
    elif text.h2 != None and text.h2 != "":
        return [text.h2.get_text()]
    else:
        return [""]
"""
def get_heading_from_html(html: str) -> list:
    text = BeautifulSoup(html, "html.parser")
    return text.h1.get_text(strip=True) if isinstance(text.h1, Tag) else text.h2.get_text(strip=True) if isinstance(text.h2, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    text = BeautifulSoup(html, "html.parser")
    return text.main.p.get_text(strip=True) if isinstance(text.main, Tag) else text.p.get_text(strip=True) if isinstance(text.p, Tag) else ""

def get_urls_from_html(html: str, base_url: str = "") -> list:
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for link in soup.find_all("a", href=True):
        url = link["href"]
        if url.startswith("/"):
            url = urljoin(base_url, url)
        urls.append(url)
    return urls

def get_images_from_html(html: str, base_url: str = "") -> list:
    soup = BeautifulSoup(html, "html.parser")
    images = []
    for img in soup.find_all("img", src=True):
        src = img["src"]
        if src.startswith("/"):
            src = base_url + src
        images.append(src)
    return images

def extract_page_data(html: str, base_url: str) -> dict:
    return {
        "url": base_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, base_url),
        "image_urls": get_images_from_html(html, base_url)
    }