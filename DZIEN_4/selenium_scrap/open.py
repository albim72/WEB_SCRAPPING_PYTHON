from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.python.org")

print(f'tytuł strony: {driver.title}')

elem = driver.find_element("id","about")
print(f'Nagłóek About: {elem.text}')
driver.quit()
