import requests, pandas as pd

url = "https://bdl.stat.gov.pl/api/v1/variables"
params = {
    "search": "temperatura", 
    "format": "json", 
    "lang": "pl", 
    "page-size": 50
}
r = requests.get(url, params=params, timeout=15)
r.raise_for_status()
data = r.json()

for v in data["results"]:
    print(v["id"], v["name"])

import requests, pandas as pd

unit_id = "000000000000"   # Polska
var_id = 259864            # przykładowy ID zmiennej

url = f"https://bdl.stat.gov.pl/api/v1/data/by-unit/{unit_id}"
params = {
    "var-id": var_id,
    "year": "2015-2022",   # można podać zakres jako string
    "format": "json",
    "lang": "pl"
}

r = requests.get(url, params=params, timeout=15)
r.raise_for_status()
data = r.json()

rows = []
for series in data["results"]:
    for e in series["values"]:   # <-- tu poprawka
        rows.append({
            "rok": e["year"],
            "wartosc": e["val"]
        })

df = pd.DataFrame(rows)
print(df.head())
df.to_csv("temperatura.csv", index=False, encoding="utf-8")
print("✅ Zapisano do temperatura.csv")

