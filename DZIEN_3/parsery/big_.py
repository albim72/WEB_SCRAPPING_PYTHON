from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin
import pathlib, time, re

BASE = "https://example.com/"
HTML = pathlib.Path("sample2.html").read_text(encoding="utf-8")

# aby przyspieszyć: parsujemy tylko sekcję #wrap (pokaz: SoupStrainer)
only_wrap = SoupStrainer(id="wrap")

def clean_number(txt: str) -> int:
    # "120 000" -> 120000
    return int(re.sub(r"\D+", "", txt))

def parse_with(parser: str):
    t0 = time.perf_counter()
    soup = BeautifulSoup(HTML, parser, parse_only=only_wrap)
    dt = round((time.perf_counter() - t0)*1000, 2)

    # --- 1) Tabela (może być niezamknięta) ---
    rows = []
    table = soup.select_one("table.raporty")
    if table:
        # Pomijamy pierwszy wiersz z nagłówkami; tolerujemy brak </tr>
        trs = table.find_all("tr")
        for tr in trs[1:]:
            tds = tr.find_all(["td", "th"])
            if len(tds) >= 3:
                rok = tds[0].get_text(strip=True)
                kwartal = tds[1].get_text(strip=True)
                przychod_txt = tds[2].get_text(" ", strip=True)
                rows.append({
                    "rok": int(re.sub(r"\D", "", rok) or 0),
                    "kwartal": kwartal,
                    "przychod": clean_number(przychod_txt),
                    "data_id": tr.get("data-id")
                })

    # --- 2) Linki do plików (atrybuty bez cudzysłowów) ---
    files = []
    for a in soup.select("a.file"):
        files.append({
            "href": urljoin(BASE, a.get("href", "")),
            "type": a.get("data-type"),
            "text": a.get_text(strip=True)
        })

    return {"parser": parser, "ms": dt, "rows": rows, "files": files}

for parser in ("html.parser", "lxml", "html5lib"):
    out = parse_with(parser)
    print(f"\n=== {out['parser']} ({out['ms']} ms) ===")
    print("Tabela:")
    for r in out["rows"]:
        print(" ", r)
    print("Pliki:")
    for f in out["files"]:
        print(" ", f)
