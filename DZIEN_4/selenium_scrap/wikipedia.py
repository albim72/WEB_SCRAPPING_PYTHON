from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

opts = webdriver.ChromeOptions()
opts.add_argument("--start-maximized")
# opts.add_argument("--headless=new")  # w razie potrzeby

driver = webdriver.Chrome(options=opts)

try:
    driver.get("https://pl.wikipedia.org")
    wait = WebDriverWait(driver, 30)

    # 1) Spróbuj zamknąć/zaakceptować baner cookies (różne warianty)
    try:
        # Wikimedia używa różnych implementacji w zależności od regionu/AB-testów
        cookie_locators = [
            (By.ID, "wm-cc-accept-all"),
            (By.CSS_SELECTOR, "button[aria-label*='Zgadzam']"),
            (By.CSS_SELECTOR, "button[aria-label*='Akceptuj']"),
            (By.XPATH, "//button[contains(., 'Zgadzam') or contains(., 'Akceptuj')]"),
        ]
        for how, what in cookie_locators:
            try:
                btn = wait.until(EC.element_to_be_clickable((how, what)))
                btn.click()
                break
            except TimeoutException:
                pass
    except Exception:
        pass  # jeśli nie ma banera, idziemy dalej

    # 2) Stabilniejszy selektor do linku językowego
    #    (Wikipedia oznacza link do wersji EN atrybutem lang="en")
    link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[lang='en']")))
    link.click()

    # 3) Poczekaj aż przeładuje się strona EN (tytuł lub domena)
    wait.until(EC.url_contains("en.wikipedia.org"))
    print(f"aktualny url: {driver.current_url}")

finally:
    driver.quit()
