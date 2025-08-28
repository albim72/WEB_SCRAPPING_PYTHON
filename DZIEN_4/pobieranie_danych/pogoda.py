import requests, pandas as pd

# Endpoint GUS BDL API (średnia temperatura powietrza, wskaźnik 42702)
url = "https://api-dbw.stat.gov.pl/api/variable/42702/data/by-unit/000000000000?lang=pl&format=json"

r = requests.get(url, timeout=15)
r.raise_for_status()
data = r.json()

# Ekstrakcja: lista słowników {rok, wartosc}
rows = []
for entry in data["results"]:
    rows.append({
        "rok": entry["year"],
        "miesiac": entry["month"],
        "temperatura": entry["val"]
    })

# Do DataFrame i zapis do CSV
df = pd.DataFrame(rows)
df.to_csv("temperatura.csv", index=False, encoding="utf-8")
print("✅ Zapisano dane do temperatura.csv")
print(df.head())
