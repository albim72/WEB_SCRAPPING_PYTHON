from bs4 import BeautifulSoup

html = open("ex7.html",encoding="utf-8").read()
soup = BeautifulSoup(html, "lxml")

books = []
for div in soup.select("div.book"):
    title = div.select_one("h2").get_text(strip=True)
    author = div.select_one(".author").get_text(strip=True)
    year = int(div.select_one(".year").get_text(strip=True))
    books.append({"tytuł":title, "autor":author, "rok":year})

print(books)
