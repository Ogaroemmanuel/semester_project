from django.db import models

# Create your models here.
from django.db import models

class Retailer(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    product_url = models.URLField(blank=True, null=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
