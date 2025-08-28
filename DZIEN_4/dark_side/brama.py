import urllib.robotparser as rp, requests, sys

BASE = "https://books.toscrape.com"
AGENT = "MyBot/1.0"
robots = rp.RobotFileParser(f"{BASE}/robots.txt")
robots.read()

# twardy stop, jeśli strona jest zabroniona
TARGET = f"{BASE}/catalogue/page-1.html"
if not robots.can_fetch(AGENT, TARGET):
    sys.exit(f"ZABRONIONE przez robots.txt: {TARGET}")

# miękka sonda (HEAD) przed GET
h = requests.head(TARGET, timeout=10)
if h.status_code >= 400:
    sys.exit(f"Ryzyko (status {h.status_code}), przerwanie.")

print("Przejście przez Strażnika Bram — można kontynuować.")
