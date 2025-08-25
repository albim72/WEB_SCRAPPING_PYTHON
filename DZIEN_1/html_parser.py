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
