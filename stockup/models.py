from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    business_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    



class Inventory(models.Model):
    category_choices = [ ("electronics", "Electronics"),

            ("fashion", "Fashion"),

            ("groceries", "Groceries"),

            ("beauty", "Beauty & Personal Care"),

            ("home", "Home & Kitchen"),

            ("accessories", "Accessories"),

            ("other", "Other"),

    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=category_choices)
    is_low_stock = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name

    
 


class Sales(models.Model):
    product = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, related_name="sales")
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_per_item= models.DecimalField(decimal_places=2 , max_digits=12)

    
