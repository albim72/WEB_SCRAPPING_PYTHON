# demo_login_quotes_requests.py
import csv
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://quotes.toscrape.com"
LOGIN = urljoin(BASE, "/login")

def get_csrf_and_cookies(session: requests.Session):
    r = session.get(LOGIN, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.select_one("input[name=csrf_token]")["value"]
    return token

def login(session: requests.Session, username: str, password: str):
    token = get_csrf_and_cookies(session)
    payload = {
        "csrf_token": token,
        "username": username,
        "password": password,
    }
    r = session.post(LOGIN, data=payload, timeout=15)
    r.raise_for_status()
    return r

def scrape_all_quotes(session: requests.Session):
    url = BASE  # start od strony głównej po zalogowaniu
    data = []
    while True:
        r = session.get(url, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for q in soup.select(".quote"):
            text = q.select_one(".text").get_text(strip=True).strip('“”"')
            author = q.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in q.select(".tags a.tag")]
            data.append({"text": text, "author": author, "tags": ", ".join(tags)})

        next_a = soup.select_one("li.next > a")
        if not next_a:
            break
        url = urljoin(url, next_a["href"])
        time.sleep(0.2)  # grzecznościowy throttling
    return data

def main():
    with requests.Session() as s:
        login(s, "demo_user", "demo_pass")
        rows = scrape_all_quotes(s)

    df = pd.DataFrame(rows)
    df.to_csv("quotes.csv", index=False, encoding="utf-8")
    df.to_excel("quotes.xlsx", index=False)
    df.to_html("quotes.html", index=False)
    print(f"✅ Zapisano {len(df)} cytatów → quotes.csv / quotes.xlsx / quotes.html")

if __name__ == "__main__":
    main()
