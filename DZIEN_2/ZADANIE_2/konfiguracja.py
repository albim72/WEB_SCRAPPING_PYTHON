from dataclasses import dataclass
from typing import Optional, List, Dict

# --- KONFIG ---
@dataclass
class Config:
    name: str
    item_selector: str
    title_selector: str
    price_selector: Optional[str] = None

# dwa różne serwisy
BOOKS_CFG = Config(
    name="Books",
    item_selector="article.product",
    title_selector=".title",
    price_selector=".price"
)

MOVIES_CFG = Config(
    name="Movies",
    item_selector="div.movie",
    title_selector="h2",
    price_selector="span.cost"
)

# --- MASZYNA ---
def fake_extract(html: str, cfg: Config) -> List[Dict]:
    """
    Symulacja ekstrakcji:
    zamiast BeautifulSoup zwracamy "udawane" rekordy,
    pokazując, że logika nie zależy od konkretnego serwisu.
    """
    return [
        {"title": f"Sample 1 from {cfg.name}", "price": 10.0},
        {"title": f"Sample 2 from {cfg.name}", "price": 20.0},
    ]

# --- DEMO ---
for cfg in [BOOKS_CFG, MOVIES_CFG]:
    print(f"\n== Używam konfiguracji: {cfg.name} ==")
    results = fake_extract("<html> ... </html>", cfg)
    for r in results:
        print(r)
