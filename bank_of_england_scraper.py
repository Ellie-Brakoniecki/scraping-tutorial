import pandas as pd
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


BANK_OF_ENGLAND_DOMAIN = "www.bankofengland.co.uk"

# proxy settings
NO_PROXY_DOMAINS = "localhost, BANK_OF_ENGLAND_DOMAIN"
os.environ["no_proxy"] = NO_PROXY_DOMAINS


def _get_chromedriver_path():
    project_root_path = os.path.abspath(os.path.dirname(__file__))
    chromedriver_path = os.path.join(
        project_root_path,
        "chromedriver",
        "chromedriver.exe"
    )
    return chromedriver_path
    
    
def setup_webdriver():
    service = Service(executable_path=_get_chromedriver_path())
    return webdriver.Chrome(service=service)


def navigate_to_page(driver, url):
    driver.get(url)
    

def accept_cookies(driver):
    try:
        accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
    )
        accept_button.click()
    except Exception as e:
        print("Error accepting cookies:", e)


def scrape_bank_england_base_rate(driver):

    try:
        # Locate the elements and extract text
        bank_rate_element = driver.find_element(By.CLASS_NAME, "home-stat-number")
        bank_rate = bank_rate_element.text.strip()

        next_due_element = driver.find_element(By.CLASS_NAME, "home-stat-caption")
        next_due = next_due_element.text.strip()

        # Print the scraped data
        print(f"Current Bank Rate: {bank_rate}")
        print(f"Next Due: {next_due}")

        # Save to CSV
        current_date = datetime.now().strftime("%Y-%m-%d")
        data = {
            "Scrape Date": [current_date],
            "Base Rate": [bank_rate],
            "Next Due Date": [next_due]
        }
        df = pd.DataFrame(data)
        
        # Define the CSV file path
        csv_file_path = "data/bank_of_england_base_rates.csv"
        # Append data to the CSV file, creating it if it doesn't exist
        df.to_csv(csv_file_path, mode='a', header=not os.path.exists(csv_file_path), index=False)

    except Exception as e:
        print("Error while scraping the data:", e)
                

if __name__ == "__main__":
    
    driver = setup_webdriver()

    navigate_to_page(driver, f"https://{BANK_OF_ENGLAND_DOMAIN}")
    accept_cookies(driver)
    
    scrape_bank_england_base_rate(driver)
    
    input("Press Enter to close the browser...")
    driver.quit()



