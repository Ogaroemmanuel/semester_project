from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Price
from .scraper import scrape_jumia, scrape_kilimall, scrape_masoko

def home(request):
    query = request.GET.get('q')
    products = []
    if query:
        scrape_jumia(query)
        scrape_kilimall(query)
        scrape_masoko(query)
        products = Price.objects.filter(product__name__icontains=query)
    return render(request, "index.html", {"products": products, "query": query})
