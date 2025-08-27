import os, re, hashlib, requests, pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE = "http://localhost:8000/task3.html"
OUT = "out3"; os.makedirs(OUT, exist_ok=True)
ATTACH_EXTS = {".jpg", ".jpeg", ".zip", ".txt", ".png"}

def safe_filename(name: str) -> str:
    # usuń query i znormalizuj
    name = name.split("?")[0]
    return re.sub(r"[^\w\.-]+", "_", name, flags=re.UNICODE)[:180] or "file"

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

r = requests.get(BASE, timeout=10); r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

rows = []
seen_hashes = set()

for a in soup.select("a[href]"):
    link = urljoin(BASE, a["href"])
    path = urlparse(link).path
    ext = os.path.splitext(path)[1].lower()
    if ext not in ATTACH_EXTS:
        continue

    resp = requests.get(link, timeout=20); resp.raise_for_status()
    digest = sha256_bytes(resp.content)
    if digest in seen_hashes:
        # duplikat treści — pomijamy zapis pliku, ale rejestrujemy metadane
        rows.append({"url": link, "saved": False, "sha256": digest})
        continue

    seen_hashes.add(digest)
    fname = safe_filename(os.path.basename(path))
    out_path = os.path.join(OUT, fname)
    with open(out_path, "wb") as f: f.write(resp.content)

    rows.append({
        "url": link,
        "saved": True,
        "local_path": os.path.abspath(out_path),
        "ext": ext,
        "bytes": len(resp.content),
        "sha256": digest
    })

df = pd.DataFrame(rows)
print(df)
# np. zapis do CSV/Parquet:
# df.to_csv("out3_index.csv", index=False)
