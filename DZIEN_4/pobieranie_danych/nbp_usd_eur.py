import requests, sqlite3
from datetime import date

# Baza
con = sqlite3.connect("kursy.db")
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    currency TEXT,
    rate REAL,
    day TEXT
)
""")

# Funkcja pobierająca kurs dla wybranej waluty
def get_rate(code: str) -> float:
    url = f"https://api.nbp.pl/api/exchangerates/rates/A/{code}/?format=json"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data["rates"][0]["mid"]

# Pobranie kursów EUR i USD
today = str(date.today())
for code in ["EUR", "USD"]:
    rate = get_rate(code)
    cur.execute("INSERT INTO rates(currency, rate, day) VALUES (?, ?, ?)", (code, rate, today))
    print(f"✅ Zapisano {code}: {rate}")

con.commit()
con.close()
