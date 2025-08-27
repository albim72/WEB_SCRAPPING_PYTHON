from bs4 import BeautifulSoup
from urllib.parse import urljoin

html = open("ex3.html").read()
soup = BeautifulSoup(html, "html.parser")

BASE = "http://example_scrap.com/dir/page.html"

for a in soup.select(".files a"):
    print(urljoin(BASE, a["href"]))
