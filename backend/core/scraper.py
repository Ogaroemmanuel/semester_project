import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from .models import Product, Retailer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# ────────────── JUMIA SCRAPER ──────────────
def scrape_jumia(query):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    search_url = f"https://www.jumia.co.ke/catalog/?q={quote_plus(query)}"
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve Jumia page")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    retailer, _ = Retailer.objects.get_or_create(name="Jumia", url="https://www.jumia.co.ke")
    product_containers = soup.select('article.prd')

    for item in product_containers:
        name_tag = item.select_one('h3.name')
        price_tag = item.select_one('div.prc')
        link_tag = item.select_one('a.core')
        image_tag = item.select_one('img')

        if not name_tag or not price_tag or not link_tag or not image_tag:
            continue

        product_name = name_tag.text.strip()
        product_price = price_tag.text.strip()
        product_link = "https://www.jumia.co.ke" + link_tag['href']
        product_image = image_tag.get("data-src") or image_tag.get("src")
        if product_image and product_image.startswith('/'):
            product_image = 'https://www.jumia.co.ke' + product_image

        print(f"Jumia: {product_name}, Price: {product_price}, Image: {product_image}")

        Product.objects.get_or_create(
            name=product_name,
            retailer=retailer,
            product_url=product_link,
            defaults={
                'image_url': product_image,
                'price': product_price,
            }
        )

# ────────────── KILIMALL SCRAPER ──────────────
def scrape_kilimall(query):
    options = Options()
    # Comment out headless for debugging if needed
    # options.add_argument('--headless')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    search_url = f"https://www.kilimall.co.ke/new/commoditysearch?search={quote_plus(query)}"
    driver.get(search_url)

    # Wait for the listings container to appear
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.listings"))
        )
    except Exception as e:
        print("Timeout waiting for product listings:", e)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    listings = soup.select_one('div.listings')
    if listings:
        product_containers = listings.select('div')
    else:
        product_containers = []

    print("Kilimall containers found:", len(product_containers))
    for item in product_containers[:3]:
        print(item.prettify()[:500])  # Print first 3 for inspection

    for item in product_containers:
        # Update these selectors based on actual HTML structure
        name_tag = item.select_one('.product-name')
        price_tag = item.select_one('.price')
        link_tag = item.select_one('.product-link')
        image_tag = item.select_one('.product-image img') or item.select_one('.product-image')

        if not name_tag or not price_tag or not link_tag or not image_tag:
            continue

        product_name = name_tag.text.strip()
        product_price = price_tag.text.strip()
        product_link = link_tag['href']
        if product_link.startswith('/'):
            product_link = 'https://www.kilimall.co.ke' + product_link
        product_image = image_tag.get('src')
        if product_image and product_image.startswith('/'):
            product_image = 'https://www.kilimall.co.ke' + product_image

        print(f"Kilimall: {product_name}, Price: {product_price}, Image: {product_image}")

        Product.objects.get_or_create(
            name=product_name,
            retailer=retailer,
            product_url=product_link,
            defaults={
                'image_url': product_image,
                'price': product_price,
            }
        )



