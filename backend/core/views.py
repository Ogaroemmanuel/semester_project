from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .scraper import scrape_jumia, scrape_ebrahims
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
    query = request.GET.get('q')
    products = []
    if query:
        scrape_jumia(query)
        scrape_ebrahims(query)
        products = Product.objects.filter(name__icontains=query)
    print("Products found:", len(products))
    for p in products:
        print(p.name, p.price, p.retailer.name)
    return render(request, 'index.html', {'products': products, 'query': query})
