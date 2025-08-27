import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ---- KONFIG ----
URL = "http://localhost:8000/sample.html"   # podmień na swoją stronę
BASE = "http://localhost:8000"
DB_ADMIN = "mysql+pymysql://root:abc123@localhost:3306/?charset=utf8mb4"
DB_NAME = "shopdb"
DB_URL = f"mysql+pymysql://root:abc123@localhost:3306/{DB_NAME}?charset=utf8mb4"

# ---- 1) Utwórz bazę (jeśli nie ma) ----
admin_engine = sqlalchemy.create_engine(DB_ADMIN, future=True, pool_pre_ping=True)
with admin_engine.connect() as c:
    c.execute(sqlalchemy.text(
        f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    ))
    c.commit()

# ---- 2) Model + tabela ----
engine = sqlalchemy.create_engine(DB_URL, echo=False, future=True, pool_pre_ping=True)

class Base(DeclarativeBase): pass

class Product(Base):
    __tablename__ = "products"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    sku = sqlalchemy.Column(sqlalchemy.String(32), unique=True, index=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String(500), nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, future=True)
session = Session()

# ---- 3) Scrap ----
resp = requests.get(URL, timeout=15)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "lxml")  # może być "html.parser" albo "html5lib"

items = []
for li in soup.select("ul.products > li.product"):
    sku = li.get("data-sku")
    name = li.select_one("a.name").get_text(strip=True)
    price_text = li.select_one("span.price").get_text(strip=True)
    # normalizacja ceny (zamień przecinek na kropkę jeśli trzeba)
    price = float(re.sub(r"[^\d,\.]", "", price_text).replace(",", "."))

    url = urljoin(BASE, li.select_one("a.name")["href"])
    items.append(Product(sku=sku, name=name, price=price, url=url))

# ---- 4) Zapis do MySQL (prosty upsert po SKU) ----
for p in items:
    # sprawdź czy już jest — minimalny dedup
    existing = session.query(Product).filter_by(sku=p.sku).one_or_none()
    if existing:
        existing.name = p.name
        existing.price = p.price
        existing.url = p.url
    else:
        session.add(p)

session.commit()
print(f"Zapisano/zmodyfikowano: {len(items)} rekordów.")

# Podgląd:
for row in session.query(Product).order_by(Product.id):
    print(row.id, row.sku, row.name, row.price, row.url)
