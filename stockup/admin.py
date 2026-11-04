from django.contrib import admin

# Register your models here.
from .models import User, Inventory, Sales

admin.site.register(User)
admin.site.register(Inventory)
admin.site.register(Sales)
