from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# --- helpers ---
def clean_price(price):
    if price:
        price = price.replace("грн.", "").replace(" ", "").replace(",", ".")
        try:
            return float(price)
        except:
            return None
    return None

def clean_area(area):
    if area:
        area = area.replace("м²", "").replace(",", ".")
        try:
            return float(area)
        except:
            return None
    return None


# --- setup driver ---
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

url = "https://www.olx.ua/uk/nedvizhimost/kvartiry/kiev/"
driver.get(url)

# --- знайти оголошення ---
ads = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-cy='l-card']"))
)

data = []

for ad in ads[:10]:  # для тесту беремо 10
    try:
        title = ad.find_element(By.CSS_SELECTOR, "a").text
    except:
        title = None

    try:
        price_raw = ad.find_element(By.CSS_SELECTOR, "[data-testid='ad-price']").text
        price = clean_price(price_raw)
    except:
        price = None

    try:
        location = ad.find_element(By.CSS_SELECTOR, "[data-testid='location-date']").text
        city = location.split(",")[0]
    except:
        location = None
        city = None

    try:
        link = ad.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    except:
        link = None

    # --- деталі ---
    area = None
    floor = None
    total_floors = None

    if link:
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])

        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)

            page_text = driver.find_element(By.TAG_NAME, "body").text

            # --- area ---
            if "м²" in page_text:
                try:
                    raw_area = page_text.split("м²")[0].split()[-1] + " м²"
                    area = clean_area(raw_area)
                except:
                    area = None

            # --- floor ---
            if "Поверх" in page_text:
                try:
                    floor = page_text.split("Поверх")[1].split("\n")[0].strip()
                except:
                    floor = None

            # --- total floors ---
            if "Поверхів" in page_text:
                try:
                    total_floors = page_text.split("Поверхів")[1].split("\n")[0].strip()
                except:
                    total_floors = None

        except:
            pass

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    data.append({
        "title": title,
        "price": price,
        "location": location,
        "city": city,
        "link": link,
        "area": area,
        "floor": floor,
        "total_floors": total_floors
    })


# --- збереження ---
df = pd.DataFrame(data)
df.to_csv("olx_data.csv", index=False, sep=";")

print(df.head())

driver.quit()