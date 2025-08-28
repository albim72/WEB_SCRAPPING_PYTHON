unit_id = "000000000000"   # Polska
var_id = 12345             # poprawny ID z wyszukiwania

url = f"https://bdl.stat.gov.pl/api/v1/data/by-unit/{unit_id}"
params = {
    "var-id": var_id,
    "year": 2020,          # lub zakres, np. 2015&year=2016&year=2017
    "format": "json",
    "lang": "pl"
}

r = requests.get(url, params=params, timeout=15)
r.raise_for_status()
data = r.json()

rows = []
for e in data["results"]:
    rows.append({
        "rok": e["year"],
        "wartosc": e["val"]
    })

df = pd.DataFrame(rows)
print(df.head())
df.to_csv("temperatura.csv", index=False, encoding="utf-8")unit_id = "000000000000"   # Polska
var_id = 12345             # poprawny ID z wyszukiwania

url = f"https://bdl.stat.gov.pl/api/v1/data/by-unit/{unit_id}"
params = {
    "var-id": var_id,
    "year": 2020,          # lub zakres, np. 2015&year=2016&year=2017
    "format": "json",
    "lang": "pl"
}

r = requests.get(url, params=params, timeout=15)
r.raise_for_status()
data = r.json()

rows = []
for e in data["results"]:
    rows.append({
        "rok": e["year"],
        "wartosc": e["val"]
    })

df = pd.DataFrame(rows)
print(df.head())
df.to_csv("temperatura.csv", index=False, encoding="utf-8")
