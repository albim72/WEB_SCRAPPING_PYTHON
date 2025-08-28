from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.python.org")

#scroll do dołu strony
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#zapis zrzutu
driver.save_screenshot("screenpython.png")
driver.quit()
