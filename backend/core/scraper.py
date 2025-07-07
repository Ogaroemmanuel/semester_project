import requests
from bs4 import BeautifulSoup
from .models import Product, Retailer

def scrape_jumia(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.jumia.co.ke/catalog/?q={query}"
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
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
        product_image = image_tag['src']
        Product.objects.get_or_create(
            name=product_name,
            retailer=retailer,
            product_url=product_link,
            defaults={
                'image_url': product_image,
                'price': product_price,
            }
        )

def scrape_kilimall(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.kilimall.co.ke/new/commoditysearch?search={query}"
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    retailer, _ = Retailer.objects.get_or_create(name="Kilimall", url="https://www.kilimall.co.ke")
    product_containers = soup.select('div.product-card')  # Adjust selector as needed

    for item in product_containers:
        name_tag = item.select_one('.title')
        price_tag = item.select_one('.price')
        link_tag = item.select_one('a')
        image_tag = item.select_one('img')
        if not name_tag or not price_tag or not link_tag or not image_tag:
            continue
        product_name = name_tag.text.strip()
        product_price = price_tag.text.strip()
        product_link = "https://www.kilimall.co.ke" + link_tag['href']
        product_image = image_tag['src']
        Product.objects.get_or_create(
            name=product_name,
            retailer=retailer,
            product_url=product_link,
            defaults={
                'image_url': product_image,
                'price': product_price,
            }
        )