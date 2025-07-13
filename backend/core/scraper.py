import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from .models import Product, Retailer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# ────────────── JUMIA SCRAPER ──────────────
def scrape_jumia(query, update_existing=False):
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

        obj, created = Product.objects.get_or_create(
            name=product_name,
            retailer=retailer,
            product_url=product_link,
            defaults={
                'image_url': product_image,
                'price': product_price,
            }
        )
        if not created and update_existing:
            obj.price = product_price
            obj.image_url = product_image
            obj.save()

# ────────────── EBRAHIMS SCRAPER ──────────────
def scrape_ebrahims(query, update_existing=False):
    search_url = f"https://ebrahims.co.ke/?s={query}&post_type=product"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve Ebrahims page")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    # Update the selector below based on actual HTML structure
    product_containers = soup.select('li.product')

    for item in product_containers:
        name_tag = item.select_one('h2.woocommerce-loop-product__title')
        price_tag = item.select_one('span.woocommerce-Price-amount')
        link_tag = item.select_one('a.woocommerce-LoopProduct-link')
        image_tag = item.select_one('img')

        if not name_tag or not price_tag or not link_tag or not image_tag:
            continue

        product_name = name_tag.text.strip()
        product_price = price_tag.text.strip()
        product_link = link_tag['href']
        product_image = image_tag.get('src')

        print(f"Ebrahims: {product_name}, Price: {product_price}, Image: {product_image}")

        retailer, _ = Retailer.objects.get_or_create(name="Ebrahims", url="https://ebrahims.co.ke")
        obj, created = Product.objects.get_or_create(
            name=product_name,
            retailer=retailer,
            product_url=product_link,
            defaults={
                'image_url': product_image,
                'price': product_price,
            }
        )
        if not created and update_existing:
            obj.price = product_price
            obj.image_url = product_image
            obj.save()




