from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.core.management.base import BaseCommand
from .scraper import scrape_jumia, scrape_ebrahims
from collections import defaultdict
from .models import Product

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def index(request):
    query = request.GET.get('q', '').strip().lower()
    products = Product.objects.all()

    # Split query into words
    query_words = query.split()

    # Filter products in Python to match all words in any order
    filtered_products = []
    for product in products:
        name = product.name.strip().lower()
        if all(word in name for word in query_words):
            filtered_products.append(product)

    # Check if we have products from each retailer
    has_jumia = any(p.retailer.name == 'Jumia' for p in filtered_products)
    has_ebrahims = any(p.retailer.name == 'Ebrahims' for p in filtered_products)

    # Scrape missing retailer(s) if query is present
    if query:
        scrape_needed = False
        if not has_jumia:
            scrape_jumia(query, update_existing=True)
            scrape_needed = True
        if not has_ebrahims:
            scrape_ebrahims(query, update_existing=True)
            scrape_needed = True
        # Only re-query if scraping was done
        if scrape_needed:
            products = Product.objects.all()
            filtered_products = []
            for product in products:
                name = product.name.strip().lower()
                if all(word in name for word in query_words):
                    filtered_products.append(product)

    # Group products by name for side-by-side comparison
    grouped = defaultdict(dict)
    for product in filtered_products:
        key = product.name.strip().lower()
        grouped[key][product.retailer.name] = product

    product_rows = []
    for name, sources in grouped.items():
        product_rows.append({
            'name': name,
            'jumia': sources.get('Jumia'),
            'ebrahims': sources.get('Ebrahims'),
        })

    return render(request, 'index.html', {'product_rows': product_rows, 'query': query})

