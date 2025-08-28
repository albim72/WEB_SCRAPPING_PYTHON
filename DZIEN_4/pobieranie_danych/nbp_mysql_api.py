import os
from datetime import date
from decimal import Decimal
import requests
import pymysql

# ==== KONFIG (ustaw zmienne środowiskowe lub wpisz na sztywno) ====
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "password")
DB_NAME = os.getenv("DB_NAME", "kursy")

# ==== POBRANIE DANYCH z NBP ====
url = "https://api.nbp.pl/api/exchangerates/rates/A/EUR/?format=json"
resp = requests.get(url, timeout=15)
resp.raise_for_status()
data = resp.json()
kurs = Decimal(str(data["rates"][0]["mid"]))  # Decimal dla dokładności
dzis = date.today()

# ==== POŁĄCZENIE Z MySQL ====
conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    charset="utf8mb4",
    autocommit=False,
    cursorclass=pymysql.cursors.Cursor,
)

try:
    with conn.cursor() as cur:
        # 1) Tabela (klucz unikalny na (currency, day))
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                currency VARCHAR(8) NOT NULL,
                rate DECIMAL(12,6) NOT NULL,
                day DATE NOT NULL,
                UNIQUE KEY uniq_currency_day (currency, day)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # 2) INSERT z UPSERT-em (bez duplikatów tego samego dnia)
        # Używamy aliasu NEW zgodnie z zaleceniami MySQL 8 (zamiast VALUES()).
        cur.execute("""
            INSERT INTO rates (currency, rate, day)
            VALUES (%s, %s, %s)
            AS new
            ON DUPLICATE KEY UPDATE
                rate = new.rate
        """, ("EUR", kurs, dzis))

    conn.commit()
    print(f"Zapisano kurs EUR na {dzis}: {kurs}")

except Exception as e:
    conn.rollback()
    raise
finally:
    conn.close()
