from bs4 import BeautifulSoup
import re

html = open("ex5.html").read()
soup = BeautifulSoup(html, "html.parser")

btn = soup.select_one("button[onclick]")
m = re.search(r"downloadFile\('(.+?)',(\d+)\)", btn["onclick"])
print(m.group(1), int(m.group(2)))
