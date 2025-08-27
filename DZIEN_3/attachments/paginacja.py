import os, re, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

START = "http://localhost:8000/page1.html"
OUT = "out2"
os.makedirs(OUT, exist_ok=True)
ATTACH_EXTS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv"}

def safe_filename(name): return re.sub(r"[^\w\.-]+", "_", name)[:180] or "file"

url = START
visited = set()
downloaded = []

while url and url not in visited:
    visited.add(url)
    r = requests.get(url, timeout=10); r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Zbierz i pobierz załączniki na tej stronie
    for a in soup.select("a[href]"):
        link = urljoin(url, a["href"])
        ext = os.path.splitext(urlparse(link).path)[1].lower()
        if ext in ATTACH_EXTS:
            resp = requests.get(link, timeout=20); resp.raise_for_status()
            fname = safe_filename(os.path.basename(urlparse(link).path))
            with open(os.path.join(OUT, fname), "wb") as f: f.write(resp.content)
            downloaded.append(fname)

    # Szukaj rel=next
    nxt = soup.select_one('a[rel="next"]')
    url = urljoin(url, nxt["href"]) if nxt else None

print("Pobrano:", downloaded)

for name in ['specyfikacja.docx', 'cennik.xlsx', 'instrukcja.pdf', 'zestawienie.csv']:
    assert os.path.exists(os.path.join("out2", name))
print("Wszystko OK!")
