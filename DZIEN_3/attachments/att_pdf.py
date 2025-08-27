import os, re, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE = "http://localhost:8000/task1.html"
OUT = "out1"
os.makedirs(OUT, exist_ok=True)

ATTACH_EXTS = {".pdf", ".csv",".txt",".dat"}

def safe_filename(name: str) -> str:
    return re.sub(r"[^\w\.-]+", "_", name)[:180] or "file"

r = requests.get(BASE, timeout=10)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

downloaded = []
for a in soup.select("a[href]"):
    href = a["href"]
    if href.startswith(("mailto:", "javascript:")):
        continue
    url = urljoin(BASE, href)
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    if ext in ATTACH_EXTS:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        fname = safe_filename(os.path.basename(urlparse(url).path))
        path = os.path.join(OUT, fname)
        with open(path, "wb") as f:
            f.write(resp.content)
        downloaded.append(path)

print("Pobrane pliki:", downloaded)
