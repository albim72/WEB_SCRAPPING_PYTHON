import requests
import sqlite3
from datetime import date


#Baza SQLIte
con = sqlite3.connect('kursy.db')
cur = con.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS rates (
                                                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                 currency TEXT,
                                                 rate REAL,
                                                 day TEXT
            )
            ''')

#pobieranie danych z API NBP
url = 'http://api.nbp.pl/api/exchangerates/rates/A/EUR/?format=json'
resp = requests.get(url)
data = resp.json()
kurs = data['rates'][0]['mid']

#zapis do bazy
cur.execute("INSERT INTO rates(currency,rate,day) VALUES (?, ?, ?)",
            ("EUR",kurs, str(date.today())))
con.commit()
con.close()
print("zapisano do bazy:kurs EUR")
print(f"Kurs euro: {kurs}")
