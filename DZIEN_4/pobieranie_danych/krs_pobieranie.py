#chcemy pobrac numery KRS 0000001 do 0000100
import requests
import time

BASE_URL = "https://example.com/api/krs/{num}"
START = 1
END = 100
RESULTS = []

for num in range(START,END+1):
    url = BASE_URL.format(num=str(num).zfill(7))
    try:
        resp = requests.get(url,timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            RESULTS.append(data)
            print(f"{num}: pobrano dane")
        else:
            print(f"{num}: brak danych (HTTP {resp.status_code})")
    except requests.RequestException as e:
        print(f"{num}: błąd: {e}")
    time.sleep(0.5)
    
print("suma rekordów:",len(RESULTS))
