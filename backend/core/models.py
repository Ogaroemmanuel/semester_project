from django.db import models

# Create your models here.
from django.db import models

class Retailer(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

class Product(models.Model):
    name = models.CharField(max_length=255)

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_url = models.URLField()
    image_url = models.URLField(null=True, blank=True)  # ✅ Add this
    date_scraped = models.DateTimeField(auto_now_add=True)
