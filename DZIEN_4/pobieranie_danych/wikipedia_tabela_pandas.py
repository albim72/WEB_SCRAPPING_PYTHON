import requests
import pandas as pd

url = "https://pl.wikipedia.org/wiki/Pa%C5%84stwa_Europy"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
}

# 1) Pobierz HTML z nagłówkami (ominie 403)
resp = requests.get(url, headers=headers, timeout=20)
resp.raise_for_status()
html = resp.text

# 2) Wyciągnij tabelki z pobranego HTML
tables = pd.read_html(html)  # nie podawaj encoding – pandas sam wykryje

# 3) Spróbuj znaleźć tabelę z kolumną „Państwo” (lub podobną)
def pick_table(ts):
    for t in ts:
        cols = [str(c).lower() for c in t.columns]
        if any("państwo" in c or "państwo/terytorium" in c for c in cols):
            return t
    return ts[0]  # fallback

df = pick_table(tables)

print(df.head())

# 4) Zapis (UTF-8-SIG lepiej otwiera się w Excelu)
df.to_csv("panstwa.csv", index=False, encoding="utf-8-sig")
print("✅ Zapisano do panstwa.csv")
