from parsel import Selector
import requests

url = "https://quotes.toscrape.com"
sel = Selector(requests.get(url, timeout=10).text)

def is_honeypot(node):
    style = node.attrib.get("style", "").lower()
    cls = " ".join(node.attrib.get("class", [])).lower()
    attrs = node.attrib
    # typowe czerwone lampki
    hints = [
        "display:none" in style,
        "visibility:hidden" in style,
        "opacity:0" in style,
        "aria-hidden" in attrs,
        "tabindex" in attrs and attrs["tabindex"] == "-1",
        "honeypot" in cls or "trap" in cls,
    ]
    return any(hints)

safe_links = []
for a in sel.css("a::attr(href), a"):
    node = a.root if hasattr(a, "root") else None
    if node is not None and is_honeypot(node):
        continue
    href = a.get() if isinstance(a.get(), str) else a.attrib.get("href")
    if href:
        safe_links.append(href)

print("Linki (oczyszczone z honeypotów):", safe_links[:7])
