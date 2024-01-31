import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# domains 
# add any new urls you want to scrape here and also to NO_PROXY_DOMAINS below
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
    

def _get_chrome_options(headless):
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")  # suppresses browser aria warnings
    return chrome_options


def create_driver_and_navigate_to_domain(domain: str, headless: bool = False) -> webdriver.Chrome:
    """
    Create a WebDriver instance and navigate to the specified domain,
    Return the Webdriver instance
    """
    chromedriver_path = _get_chromedriver_path()
    chrome_options = _get_chrome_options(headless)
    
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(f"https://{domain}")
    return driver

def accept_cookies(driver):
    try:
        accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
    )
        accept_button.click()
    except Exception as e:
        print("Error accepting cookies:", e)

def scrape_bank_england_base_rate():
    driver = create_driver_and_navigate_to_domain(BANK_OF_ENGLAND_DOMAIN)
    accept_cookies(driver)

    try:
        # Locate the element containing the bank rate and extract its text
        bank_rate_element = driver.find_element(By.CLASS_NAME, "home-stat-number")
        bank_rate = bank_rate_element.text.strip()

        # Locate the element containing the next due date and extract its text
        next_due_element = driver.find_element(By.CLASS_NAME, "home-stat-caption")
        next_due = next_due_element.text.strip()

        print(f"Current Bank Rate: {bank_rate}")
        print(f"Next Due: {next_due}")

    except Exception as e:
        print("Error while scraping the data:", e)

    # Wait or close the browser based on your requirement
    input("Press Enter to close the browser...")
    driver.quit()

scrape_bank_england_base_rate()





