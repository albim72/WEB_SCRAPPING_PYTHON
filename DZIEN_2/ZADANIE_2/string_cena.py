import re
smaples = [
    "Cena: PLN 39.99",
    "Tylko 59,00 zł",
    "USD 12",
    "Brak ceny"
]

#Regex: liczba całkowita lub zmienno przecinkowa(kropka lub przecinek)
pattern = re.compile(r"([0-9]+(?:[.,][0-9]+)?)")

def parse_price(text: str):
    m = pattern.search(text)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))

for s in smaples:
    print(f"{s}: {parse_price(s)}")
