from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Price
from .scraper import scrape_jumia, scrape_kilimall

def home(request):
    query = request.GET.get('q')
    products = []
    if query:
        scrape_jumia(query)
        scrape_kilimall(query)
        products = Price.objects.filter(product__name__icontains=query)
    return render(request, "index.html", {"products": products, "query": query})

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