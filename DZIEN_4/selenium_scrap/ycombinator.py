#scrapowanie wielu elementów
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://news.ycombinator.com/")

items = driver.find_elements(By.CLASS_NAME, "titleline")

for i, item in enumerate(items[:5],start=1):
    print(i,item.text)
driver.quit()
