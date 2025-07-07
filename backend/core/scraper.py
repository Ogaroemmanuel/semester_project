# === IMPORT REQUIRED MODULES ===
from selenium import webdriver  # lets us control the browser
from selenium.webdriver.chrome.service import Service  # helps run ChromeDriver
from selenium.webdriver.chrome.options import Options  # allows headless mode (no window)
from bs4 import BeautifulSoup  # lets us extract content from HTML
import requests  # for simple web requests
import time  # to pause and wait for pages to load


# === FUNCTION TO SCRAPE KILIMALL ===
def scrape_kilimall():
    print("\nScraping Kilimall...")

    # 1. Set up Chrome in headless mode (so it runs in background)
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run without opening browser window
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # 2. Tell Selenium where to find ChromeDriver
    service = Service('C:/path/to/chromedriver.exe')  # Change to your real path

    # 3. Start Chrome using Selenium
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 4. Go to Kilimall search page
    url = "https://www.kilimall.co.ke/new/commoditysearch?keyword=phone"
    driver.get(url)

    # 5. Wait for the page to fully load (especially JavaScript)
    time.sleep(5)

    # 6. Get the HTML code of the page
    html = driver.page_source

    # 7. Use BeautifulSoup to extract data from that HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 8. Find product boxes (inspect the site to find correct class name)
    products = soup.find_all('div', class_='product-box')  # may need to change this

    # 9. Print each product (simplified)
    for product in products:
        print("Kilimall Product:", product.text.strip())

    # 10. Close the browser
    driver.quit()


# === FUNCTION TO SCRAPE JUMIA ===
def scrape_jumia():
    print("\nScraping Jumia...")

    # 1. Set up the URL and headers
    url = "https://www.jumia.co.ke/catalog/?q=phone"
    headers = {
        "User-Agent": "Mozilla/5.0"  # Pretend to be a normal browser
    }

    # 2. Make a web request to Jumia
    response = requests.get(url, headers=headers)

    # 3. Use BeautifulSoup to read the HTML from the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # 4. Find product containers (inspect site to confirm class name)
    products = soup.find_all('article', class_='prd')  # common for Jumia

    # 5. Print each product (simplified)
    for product in products:
        print("Jumia Product:", product.text.strip())


# === MAIN CODE ===
if __name__ == "__main__":
    scrape_kilimall()  # Scrape Kilimall using Selenium
    scrape_jumia()     # Scrape Jumia using BeautifulSoup