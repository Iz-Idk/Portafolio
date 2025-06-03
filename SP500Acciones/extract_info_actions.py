import json
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Config
INPUT_FILENAME = "links_estados_unidos_acciones.json"
OUTPUT_FILENAME = "output_data_US.json"
FAILED_FILENAME = "failed_US.json"
WAIT_TIME = 10

# Load URLs
with open(INPUT_FILENAME, "r") as f:
    urls = json.load(f)

# Chrome options
options = uc.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

extracted_data = []
failed_links = []

def extract_text_safe(driver, by, value):
    """Safe element text extraction with fallback."""
    try:
        element = WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_element_located((by, value)))
        return element.text
    except (TimeoutException, NoSuchElementException):
        return ""

for url in urls:
    print(f"Processing: {url}")
    try:
        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
        options.add_argument("start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        driver = uc.Chrome(options=options)
        driver.get(url)
        wait = WebDriverWait(driver, WAIT_TIME)

        nombre = extract_text_safe(driver, By.CSS_SELECTOR, "div.mb-1 > h1")
        ticker = nombre.split("(")[1][:-1] if "(" in nombre and ")" in nombre else "N/A"

        industria = extract_text_safe(driver, By.XPATH, "//div[@class='pr-3' and text()='Industry']/following-sibling::a")
        sector = extract_text_safe(driver, By.XPATH, "//div[@class='pr-3' and text()='Sector']/following-sibling::a")

        data = {
            "URL": url,
            "Nombre": nombre,
            "Ticker": ticker,
            "Industria": industria,
            "Sector": sector
        }
        extracted_data.append(data)
        print(f"✅ Extracted: {nombre} | Ticker: {ticker} | Industria: {industria}")

    except WebDriverException as e:
        print(f"❌ Error processing {url}: {e}")
        failed_links.append(url)

    finally:
        try:
            driver.quit()
        except:
            pass
        time.sleep(random.uniform(10, 20))
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)

    with open(FAILED_FILENAME, "w", encoding="utf-8") as f:
        json.dump(failed_links, f, ensure_ascii=False, indent=4)
# Save results


print("\n✅ Scraping complete.")
print(f"✔️ Successful: {len(extracted_data)}")
print(f"❌ Failed: {len(failed_links)}")
