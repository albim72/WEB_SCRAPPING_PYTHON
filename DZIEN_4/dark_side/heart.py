import time, random, requests

FAILS = 0
OPEN = False
OPEN_UNTIL = 0

def smart_get(url, max_retries=4, base=0.7):
    global FAILS, OPEN, OPEN_UNTIL
    now = time.time()
    if OPEN and now < OPEN_UNTIL:
        raise RuntimeError("🔌 Circuit OPEN — odpoczynek po porażkach.")
    if OPEN and now >= OPEN_UNTIL:
        OPEN = False; FAILS = 0

    for attempt in range(1, max_retries+1):
        try:
            r = requests.get(url, timeout=15)
            if r.status_code in (429, 503):
                retry_after = int(r.headers.get("Retry-After", "0") or 0)
                sleep = retry_after or base * (2 ** (attempt-1)) + random.random()
                time.sleep(sleep); continue
            r.raise_for_status()
            FAILS = 0
            return r
        except requests.RequestException:
            sleep = base * (2 ** (attempt-1)) + random.random()
            time.sleep(sleep)

    FAILS += 1
    if FAILS >= 3:
        OPEN, OPEN_UNTIL = True, time.time() + 60  # minuta ciszy
    raise RuntimeError("💔 Zbyt wiele błędów — breaker otwarty.")

print(smart_get("https://quotes.toscrape.com").status_code)
