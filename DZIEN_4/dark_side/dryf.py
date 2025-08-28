import requests, hashlib
from lxml import html

URL = "https://books.toscrape.com/catalogue/page-1.html"
r = requests.get(URL, timeout=15)
tree = html.fromstring(r.content)

# z kluczowych pól budujemy „odcisk palca” struktury
titles = [t.strip() for t in tree.xpath('//article//h3/a/@title')]
prices = [p.strip() for p in tree.xpath('//article//p[@class="price_color"]/text()')]

schema_fingerprint = hashlib.sha256(
    ("|".join([str(len(titles)), str(len(prices))]) + "|" +
     "|".join([t.split()[0] for t in titles[:5]])).encode("utf-8")
).hexdigest()

# baseline z poprzedniego przebiegu (tu: symulacja)
baseline = "d41d8cd98f00b204e9800998ecf8427e"  # <- w praktyce: wczytaj z pliku/DB
if baseline != schema_fingerprint:
    raise RuntimeError(f"🛑 DRIFT SCHEMATU DOM! Fingerprint: {schema_fingerprint}")

print("✅ Schema OK:", schema_fingerprint)
