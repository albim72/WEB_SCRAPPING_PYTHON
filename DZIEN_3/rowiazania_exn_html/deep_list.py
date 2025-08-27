from bs4 import BeautifulSoup

html = open("ex4.html").read()
soup = BeautifulSoup(html, "html.parser")

def parse_ul(ul):
    out=[]
    for li in ul.find_all("li"):
        text = li.contents[0].strip()
        children = li.find("ul")
        out.append({"name":text, "children":parse_ul(children) if children else []})
    return out

print(parse_ul(soup.select_one("#cats")))
