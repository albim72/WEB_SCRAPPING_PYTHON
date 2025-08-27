from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import pathlib

BASE = "https://example.com"  # do urljoin
HTML = pathlib.Path("sample.html").read_text(encoding="utf-8")

ATTACH = {
    "targets": {
        "items": "ul.products > li",
        "name": "a.name",
        "price": "span.price"
    }
}

def parse_and_extract(parser: str):
    t0 = time.perf_counter()
    soup = BeautifulSoup(HTML, parser)
    dt = time.perf_counter() - t0

    items = []
    for li in soup.select(ATTACH["targets"]["items"]):
        a = li.select_one(ATTACH["targets"]["name"])
        price_el = li.select_one(ATTACH["targets"]["price"])
        if not a or not price_el:
            continue
        row = {
            "sku": li.get("data-sku"),
            "name": a.get_text(strip=True),
            "url": urljoin(BASE, a.get("href", "")),
            "featured": "featured" in (li.get("class") or []),
            "price_text": price_el.get_text(strip=True),
        }
        items.append(row)

    return {"parser": parser, "time_ms": round(dt*1000, 2), "items": items}

for parser in ("html.parser", "lxml", "html5lib"):
    result = parse_and_extract(parser)
    print(f"\n--- {result['parser']} ({result['time_ms']} ms) ---")
    for it in result["items"]:
        print(it)
