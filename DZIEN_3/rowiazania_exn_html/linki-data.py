from bs4 import BeautifulSoup

html = open("ex2.html").read()
soup = BeautifulSoup(html, "html.parser")

for a in soup.select("a"):
    print(a["href"],a["data-type"],a["data-year"])
