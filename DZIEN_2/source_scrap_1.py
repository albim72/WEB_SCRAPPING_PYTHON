from bs4 import BeautifulSoup

html = """
<div id="main">
  <h1>Sklep</h1>
  <ul class="products">
    <li class="product" data-sku="A1">
      <a class="name" href="/p/a1">Kubek</a>
      <span class="price">£9.99</span>
    </li>
    <li class="product featured" data-sku="B2">
      <a class="name" href="/p/b2">Notes</a>
      <span class="price promo">£4.50</span>
    </li>
    <li class="product" data-sku="C3">
      <a class="name" href="/p/c3">Długopis</a>
      <span class="price">£2.49</span>
    </li>
  </ul>
  <p class="footer">Kontakt: <a href="/contact">napisz</a></p>
</div>
"""
soup = BeautifulSoup(html, "html.parser")
