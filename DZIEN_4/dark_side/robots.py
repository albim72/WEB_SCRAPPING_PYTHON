import re, json, hashlib, time, sys

RAW = """
Kontakt: Anna Kowalska, mail: anna.kowalska@example.com, tel. +48 600-700-800.
Zgłoszenie dotyczy zamówienia #A123.
"""

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s-]{7,}\d")

def pseudonymize(text):
    def h(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]
    text = EMAIL_RE.sub(lambda m: f"email#{h(m.group(0))}", text)
    text = PHONE_RE.sub(lambda m: f"phone#{h(m.group(0))}", text)
    return text

record = {
    "ts": int(time.time()),
    "origin": "scraper:example",
    "payload": pseudonymize(RAW).strip()
}

# zapis w formacie NDJSON (1 rekord = 1 linia)
sys.stdout.write(json.dumps(record, ensure_ascii=False) + "\n")
