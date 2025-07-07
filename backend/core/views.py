from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Price
from .scraper import scrape_jumia, scrape_kilimall
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
def scrape_kilimall():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    service = Service('C:/path/to/chromedriver.exe')  # Change path

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.kilimall.co.ke/new/commoditysearch?keyword=phone")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = soup.find_all('div', class_='product-box')
    results = [product.text.strip() for product in products]
    return results


def scrape_jumia():
    url = "https://www.jumia.co.ke/catalog/?q=phone"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = soup.find_all('article', class_='prd')
    results = [product.text.strip() for product in products]
    return results


def scrape_view(request):
    jumia_products = scrape_jumia()
    kilimall_products = scrape_kilimall()

    combined = "<h1>Scraped Products</h1><h2>Jumia:</h2><ul>"
    for p in jumia_products:
        combined += f"<li>{p}</li>"
    combined += "</ul><h2>Kilimall:</h2><ul>"
    for p in kilimall_products:
        combined += f"<li>{p}</li>"
    combined += "</ul>"

    return HttpResponse(combined)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to the login page
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})