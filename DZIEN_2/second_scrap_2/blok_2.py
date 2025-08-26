page_title = select_one_text(soup, "#page-title")
crumbs = [a.get_text(strip=True) for a in soup.select(".breadcrumbs a")]
print(page_title, " | ", " > ".join(crumbs))


cards = soup.select("ul.product-list > li.product")
print("Ile produktów:", len(cards))  # 3

def extract_image(li):
    img = li.select_one("img.thumb")
    return attr_or_none(img, "data-src") or attr_or_none(img, "src")

for li in cards:
    print(li["data-sku"], "img:", extract_image(li))

def extract_price(li):
    promo = select_one_text(li, ".prices .price.promo")
    base  = select_one_text(li, ".prices .price:not(.promo):not(.old)")
    raw = promo or base or select_one_text(li, ".prices .price")
    return parse_price_to_float(raw), raw

for li in cards:
    p_float, p_raw = extract_price(li)
    print(li["data-sku"], p_raw, "→", p_float)

def extract_rating(li):
    el = li.select_one(".star-rating")
    mapping = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
    for c in (el.get("class", []) if el else []):
        if c in mapping: return mapping[c]
    return None

for li in cards:
    print(li["data-sku"], "rating:", extract_rating(li))


def extract_stock(li):
    txt = select_one_text(li, ".availability")
    m = re.search(r"\((\d+)\)", txt or "")
    if m: return int(m.group(1))
    # fallback: jeśli jest klasa 'out' albo tekst „niedostępne”
    if li.select_one(".availability.out") or (txt and "niedostępne" in txt.lower()):
        return 0
    return None

# przykład :has (znajdź wszystkie produkty z promo ceną)
promo_products = soup.select("li.product:has(.price.promo)")
print("Promo:", [li["data-sku"] for li in promo_products])

for li in cards:
    print(li["data-sku"], "stock:", extract_stock(li))


def extract_variants(li):
    out = []
    for v in li.select(".variants > li"):
        out.append({
            "label": text_or_none(v),
            "code": v.get("data-variant"),
            "ean": v.get("data-ean")
        })
    return out

print("H100 variants:", extract_variants(cards[0]))


def extract_specs(li):
    specs = {}
    for tr in li.select(".specs tr"):
        k = select_one_text(tr, "th")
        v = select_one_text(tr, "td")
        if k: specs[k] = v
    return specs

print("H100 specs:", extract_specs(cards[0]))


def extract_inline_json(li):
    data_tag = li.select_one('script.type["application/json"], script.data') or li.select_one("script.data")
    if not data_tag: return None
    try:
        return json.loads(data_tag.string)
    except Exception:
        return None

print("H300 json:", extract_inline_json(cards[2]))


def product_url(li):
    a = li.select_one(".name a")
    return urljoin(BASE, attr_or_none(a, "href"))

for li in cards:
    print(li["data-sku"], "url:", product_url(li))


# wszystkie opisy, które wspominają o ANC
anc_desc = soup.select('p.desc:-soup-contains("ANC")')
print("Ile opisów z ANC:", len(anc_desc))


next_url = urljoin(BASE, attr_or_none(soup.select_one(".pagination .next"), "href"))
print("next:", next_url)
