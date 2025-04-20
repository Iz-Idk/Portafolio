import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import undetected_chromedriver as uc

# Load URLs from JSON file
input_filename = "links_completo.json"  # Your input JSON file
output_filename = "output_data3.json"  # Output JSON file
failed_filename = "failed.json"
with open(input_filename, "r") as f:
    urls = json.load(f)

options = uc.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
#options.add_argument("--headless")  # Run in headless mode
#options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
#options.add_argument("--disable-extensions")
#options.add_argument("--disable-gpu")


# List to store extracted data
extracted_data = []
links = []
for url in urls:
    options = uc.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    driver = uc.Chrome(options=options)

    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)  # Wait for elements to load

        # Extract company name (h1)
        nombre_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mb-1 > h1")))
        nombre = nombre_element.text

        # Extract ticker from the name
        ticker = nombre.split("(")[1][:-1] if "(" in nombre and ")" in nombre else "N/A"

        # Locate "Industria" div
        industria_div = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='pr-3' and text()='Industria']")))

        # Find the corresponding industry link
        servicios_a = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='pr-3' and text()='Industria']/following-sibling::a")))
        servicios_text = servicios_a.text

        sector_div = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='pr-3' and text()='Sector']")))
        sector_a = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='pr-3' and text()='Sector']/following-sibling::a")))
        sector_text = sector_a.text

        # Store data
        extracted_data.append({
            "URL": url,
            "Nombre": nombre,
            "Ticker": ticker,
            "Industria": servicios_text,
            "Sector": sector_text
        })

        print(f"Extracted: {nombre} | Ticker: {ticker} | Industria: {servicios_text}")
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error extracting data from {url}: {e}")
        links.append(url)
        with open(failed_filename, "w", encoding="utf-8") as f:
            json.dump(links, f, ensure_ascii=False, indent=4)

    time.sleep(random.uniform(10, 20))
    driver.quit()
    
    # Save to JSON after each iteration
    
# Close the browser

