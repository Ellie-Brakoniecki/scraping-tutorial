import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def download_image(image_url, file_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)

bbc_recipe_domain = "www.bbc.co.uk/food/collections/weekend_cakes" 

# proxy settings
NO_PROXY_DOMAINS = "localhost, bbc_recipe_domain"
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
        agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "bbccookies-continue-button")))
        agree_button.click()
    except NoSuchElementException:
        print("Cookie acceptance element not found on page.")

def extract_recipes(driver):
    recipes_data = []
    recipe_elements = driver.find_elements(By.CSS_SELECTOR, "a.promo.promo__cakes_and_baking")
    for recipe_element in recipe_elements:
        try:
            title_element = recipe_element.find_element(By.CSS_SELECTOR, "h3.promo__title")
            recipe_name = title_element.text.strip()

            try:
                subtitle_element = recipe_element.find_element(By.CSS_SELECTOR, "span.promo__subtitle")
                creator_name = subtitle_element.text.strip()
            except NoSuchElementException:
                creator_name = "Unknown"

            recipe_link = recipe_element.get_attribute('href')

            image_element = recipe_element.find_element(By.CSS_SELECTOR, "img")
            image_url = image_element.get_attribute('src') or image_element.get_attribute('data-src')

            image_file_name = f"cake_images/{recipe_name.replace(' ', '_')}.jpg"
            download_image(image_url, image_file_name)

            recipe_data = {
                'name': recipe_name,
                'creator': creator_name,
                'link': recipe_link,
                'image_file_name': image_file_name
            }
            recipes_data.append(recipe_data)
        except Exception as e:
            print(f"Error extracting recipe data for {recipe_name}: {e}")
    
    return recipes_data

def scrape_recipe_details(driver, recipe_data):
    driver.get(recipe_data["link"])
    try:
        description_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.recipe-description__text"))
        )
        recipe_data['description'] = description_element.text.strip()
    except NoSuchElementException:
        recipe_data['description'] = "No description found."

if __name__ == "__main__":
    
    driver = setup_webdriver()

    navigate_to_page(driver, "https://www.bbc.co.uk/food/collections/weekend_cakes")
    accept_cookies(driver)
    recipes_data = extract_recipes(driver)

    for recipe in recipes_data:
        scrape_recipe_details(driver, recipe)

    print(recipes_data)
    input("Press Enter to close the browser...")
    driver.quit()
