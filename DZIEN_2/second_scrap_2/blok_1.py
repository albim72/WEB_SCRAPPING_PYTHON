import re, json
from urllib.parse import urljoin

BASE = "https://demo.example.com/"

def text_or_none(node, default=None):
    return node.get_text(" ", strip=True) if node else default

def select_one_text(root, css, default=None):
    el = root.select_one(css)
    return text_or_none(el, default)

def attr_or_none(el, name, default=None):
    return el.get(name, default) if el else default

def parse_price_to_float(txt):
    # obsługa PLN, spacji i przecinków
    if not txt: return None
    m = re.search(r'([0-9]+(?:[.,][0-9]{2})?)', txt)
    if not m: return None
    return float(m.group(1).replace(",", "."))
