import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL = "https://www.python.org"
URL = "https://www.comarch.pl/szkolenia/ai/?gad_source=1&gad_campaignid=21160349516&gclid=Cj0KCQjw_L_FBhDmARIsAItqgt72c14TIK9SVGX3vn_8IFa6uAZqaT8N6TD128k8wkJugmskocxPHKYaAtT8EALw_wcB"
OUT = "images"
os.makedirs(OUT, exist_ok=True)

resp = requests.get(URL)
soup = BeautifulSoup(resp.text, "html.parser")

for img in soup.select("img"):
    src = img.get("src")
    if not src:
        continue
    img_url = urljoin(URL, src)
    filename = os.path.join(OUT, os.path.basename(img_url))
    r = requests.get(img_url)
    with open(filename, "wb") as f:
        f.write(r.content)
    print(f"pobrano {filename}")
