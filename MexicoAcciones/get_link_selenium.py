import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class InvestingScraper:
    def __init__(self, driver_path):
        options = Options()
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def close(self):
        self.driver.quit()
    
    def scrape(self, url, output_file="links.json"):
        self.driver.get(url)
        time.sleep(10)
        
        try:
            self.driver.find_element(By.CSS_SELECTOR, "#index-select > .dropdown_dropdownInput__i8rbg .select_option__C4QA5").click()
            print("Dropdown opened")
        except Exception as e:
            print(f"Error opening dropdown: {e}")
        
        mexico_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'México - Acciones')]")
        ))
        mexico_option.click()
        time.sleep(5)
        
        for _ in range(7):
            try:
                load_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'load-more_loadMoreContainer__')]"))
                )
                load_more_button.click()
                time.sleep(3)
            except Exception as e:
                print(f"Error clicking 'Load More': {e}")
                break
        
        time.sleep(5)
        
        links = [
            elem.get_attribute("href") 
            for elem in WebDriverWait(self.driver, 20).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='datatable-v2_cell__wrapper__7O0wk dynamic-table-v2_desktopFreezeColumnWidth__BKzCe'] > a[href]"))
            )
        ]
        
        with open(output_file, "w") as f:
            json.dump(links, f, indent=4)
        
        print(f"Extracted {len(links)} links saved to {output_file}")

if __name__ == "__main__":
    CHROMEDRIVER_PATH = r"C:\webdriver\chromedriver.exe"
    scraper = InvestingScraper(CHROMEDRIVER_PATH)
    try:
        scraper.scrape("https://mx.investing.com/equities/mexico")
    finally:
        scraper.close()
