from django.contrib import admin
from django.db import models
from .models import Cart, Category, Product, Rate, SelectedProduct, Supplier, Comment
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Supplier)
admin.site.register(Rate)
admin.site.register(SelectedProduct)
admin.site.register(Cart)