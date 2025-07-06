import requests
from bs4 import BeautifulSoup
from .models import Product, Retailer, Price


def scrape_jumia(query):
    
    print("Scraping jumia...")


    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.jumia.co.ke/catalog/?q={query}"
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data from Jumia. Status code: {response.status_code}")
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
        price_text = price_tag.text.strip().replace("KSh", "").replace(",", "")
        try:
            price = float(price_text)
        except ValueError:
            continue

        product_url = "https://www.jumia.co.ke" + link_tag['href']
        image_url = image_tag.get('data-src') or image_tag.get('src')

        product, _ = Product.objects.get_or_create(name=product_name)
        Price.objects.create(
            product=product,
            retailer=retailer,
            price=price,
            product_url=product_url,
            image_url=image_url
        )
        print(f"Saved product: {product_name} from jumia")
        

def scrape_kilimall(query):
    print("Scraping Kilimall...")

    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.kilimall.co.ke/catalog/?q={query}"
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data from Kilimall. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    retailer, _ = Retailer.objects.get_or_create(name="Kilimall", url="https://www.kilimall.co.ke")

    product_containers = soup.select('div.item')

    for item in product_containers:
        name_tag = item.select_one('div.title')
        price_tag = item.select_one('span.price')
        link_tag = item.select_one('a')
        image_tag = item.select_one('img')

        if not name_tag or not price_tag or not link_tag or not image_tag:
            continue

        product_name = name_tag.text.strip()
        price_text = price_tag.text.strip().replace("KSh", "").replace(",", "")
        try:
            price = float(price_text)
        except ValueError:
            continue

        product_url = "https://www.kilimall.co.ke" + link_tag['href']
        image_url = image_tag.get('src')

        product, _ = Product.objects.get_or_create(name=product_name)
        Price.objects.create(
            product=product,
            retailer=retailer,
            price=price,
            product_url=product_url,
            image_url=image_url
        )
        print(f"Saved product: {product_name} from kilimall")

