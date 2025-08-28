import json, time, random, requests
from pathlib import Path

BASE = "https://api-krs.ms.gov.pl/api/krs/odpisAktualny/{krs}"
INPUT = ["0000030897","0000028860","0000858820","0000886104"]  # przykładowe, pewne KRS (ORLEN grupy)
OUT = Path("krs.ndjson")

s = requests.Session()
s.headers.update({"Accept":"application/json","User-Agent":"Mozilla/5.0"})

saved = 0
with OUT.open("a", encoding="utf-8") as f:
    for krs in INPUT:
        try:
            r = s.get(BASE.format(krs=krs), timeout=(5,15))
            if r.status_code == 404:
                print(f"{krs}: 404 (brak)")
                continue
            r.raise_for_status()
            f.write(json.dumps({"krs": krs, "payload": r.json()}, ensure_ascii=False) + "\n")
            saved += 1
            print(f"{krs}: zapisano ({saved})")
        except requests.RequestException as e:
            print(f"{krs}: {e}")
        time.sleep(0.4 + random.uniform(0,0.4))
print("Gotowe:", saved)
