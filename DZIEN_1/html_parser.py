print("analiza struktur Pythona potrzebych do parsowania danych!")
#wstęp język Python
"""
analiza tekstu: regex
parsing html  moduły
szybkie filtorwanie - list comprehension
czytanie formatu json
łączenie technik
"""

import re
import json
from html.parser import HTMLParser

import requests


print("__________ Regex ___________")
html = """
<h1>Python Scripting</h1>
<p>Cena 145 zł</p>
<a href="https://www.python.org">Kup teraz</a>
"""
#wyciągnięcie nagłówka
title = re.search("<h1>(.*?)</h1>", html).group(1)
print(f"tytuł: {title}")

#cena (cyfry + zł)
price = re.search("<p>Cena (.*?)</p>", html).group(1)
print(f"cena: {price}")

#link
link = re.search('<a href="(.*?)">', html).group(1)
print(f"link: {link}")

print("\n__________ html.Parser ___________")
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print(f"Start tag: {tag}")
    def handle_data(self,data):
        print(f"Data: {data.strip()}")

parser = MyHTMLParser()
parser.feed(html)

print("\n__________ szybkie filtrowanie ___________")
links = [
    "https://quotes.toscrape.com/page/1/",
    "https://quotes.toscrape.com/page/2/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/login",
]

#filtrujemy tylko linki do paginacji
page_links = [link for link in links if "/page/" in link]
print(page_links)


print("\n__________ JSON scrapping ___________")
data = '{"name":"Laptop","price":3510,"in_stock":true}'
product = json.loads(data)
print(f"nazwa: {product['name']}")
print(f"cena: {product['price']}")

#mini-scraper
url = "https://python.org/"
reponse = requests.get(url)

#regex nagłówka H1
title = re.search(r"<h1>(.*?)</h1>", reponse.text).group(1)
print(f"nałgówek strony: {title}")
