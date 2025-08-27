from bs4 import BeautifulSoup
import pandas as pd

html = open("ex6.html").read()
soup = BeautifulSoup(html, "html.parser")

data = []
for tr in soup.select("table.results tr")[1:]:
    name,time = [td.text.strip() for td in tr.find_all("td")]
    data.append((name,time))
    
df = pd.DataFrame(data, columns=["zawodnik", "czas"])
print(df)
