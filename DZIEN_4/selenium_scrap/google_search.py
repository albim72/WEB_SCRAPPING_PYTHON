from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# (opcjonalnie) start z większym oknem, bo czasem overlay się skaluje dziwnie
opts = webdriver.ChromeOptions()
opts.add_argument("--start-maximized")
# opts.add_argument("--headless=new")  # jeśli chcesz bez okna

driver = webdriver.Chrome(options=opts)

try:
    driver.get("https://www.google.com/ncr")  # /ncr = no country redirect; często stabilniejsze

    wait = WebDriverWait(driver, 30)

    # 1) Spróbuj zaakceptować cookies, jeśli overlay jest
    try:
        # Najczęstsze selektory w UE (zmieniają się, więc daję kilka prób)
        possible_selectors = [
            "button#L2AGLb",                              # klasyczne: 'Zgadzam się'
            "button[aria-label^='Zaakceptuj']",           # PL wariant
            "button:has(div:contains('Zgadzam się'))",    # :has i :contains nie zawsze wspierane — pomijane przez Selenium
        ]

        # Bezpieczniej: kilka XPathów na tekst/aria-label
        possible_xpaths = [
            "//button[@id='L2AGLb']",
            "//button[contains(@aria-label,'Akceptuj')]",
            "//button[.//div[contains(translate(., 'Z', 'z'),'zgadzam')]]",
            "//button[.//span[contains(translate(., 'A', 'a'),'accept')]]",
        ]

        clicked = False

        # Najpierw szybka próba po CSS
        for css in possible_selectors:
            try:
                btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
                btn.click()
                clicked = True
                break
            except TimeoutException:
                pass

        # Jeśli CSS-y nie zadziałały, spróbuj XPath
        if not clicked:
            for xp in possible_xpaths:
                try:
                    btn = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
                    btn.click()
                    clicked = True
                    break
                except TimeoutException:
                    pass
        # jeśli nic nie znaleziono, trudno — może overlayu nie było
    except Exception:
        pass

    # 2) Poczekaj aż pole wyszukiwania będzie widoczne i klikalne
    box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
    # U niektórych użytkowników Google używa <textarea name="q"> — NAME jest ten sam

    box.clear()
    box.send_keys("Selenium Python")
    box.send_keys(Keys.RETURN)  # szybciej i stabilniej niż submit()

    # 3) Poczekaj aż tytuł się zmieni lub pojawią się wyniki
    wait.until(EC.title_contains("Selenium Python"))
    print(f"tytuł po wyszukaniu: {driver.title}")

finally:
    driver.quit()
