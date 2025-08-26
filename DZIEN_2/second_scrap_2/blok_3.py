def extract_product(li):
    price_float, price_raw = extract_price(li)
    data = {
        "sku": li.get("data-sku"),
        "category": li.get("data-cat"),
        "name": select_one_text(li, ".name a"),
        "url": product_url(li),
        "rating": extract_rating(li),
        "price": price_float,
        "price_raw": price_raw,
        "stock": extract_stock(li),
        "image": urljoin(BASE, extract_image(li) or ""),
        "featured": "featured" in li.get("class", []),
        "desc": select_one_text(li, ".desc"),
        "variants": extract_variants(li),
        "specs": extract_specs(li),
        "meta_json": extract_inline_json(li),
    }
    return data

products = [extract_product(li) for li in cards]
for p in products:
    print(p["sku"], p["name"], p["price"], p["stock"], p["featured"])
