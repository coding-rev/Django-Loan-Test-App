from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup


def crawl_site():
    # Use Selenium to navigate to the website
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("https://www.eib.org/en/projects/loans/index.htm")
    driver.implicitly_wait(10)

    # Use BeautifulSoup4 to parse the HTML and extract the data from the data
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Locate and change pagination from default to 100
    select = Select(driver.find_element(By.XPATH, '//select[@id="show-entries"]'))
    select.select_by_value("100")
    time.sleep(10)

    data = driver.find_elements(By.XPATH, "//div/article")

    # return data
    return data
