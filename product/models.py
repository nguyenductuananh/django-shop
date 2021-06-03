from django.db import models
from user.models import Account, Person
# Create your models here.
class Category(models.Model) : 
    type = models.CharField(max_length=200)
class Product(models.Model) : 
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200, default="")
    price  = models.BigIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
class Supplier(models.Model) :
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    description =models.TextField(default="", max_length=200)
class Comment(models.Model) :
    content = models.CharField(max_length=500)
    created = models.DateTimeField(blank = True, auto_now_add=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, default="2")
class Rate(models.Model) : 
    rate = models.BigIntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(blank = True, auto_now_add=True)
class Cart(models.Model) : 
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
class SelectedProduct(models.Model) : 
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
