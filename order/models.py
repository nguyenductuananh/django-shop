from django.db import models
from enum import Enum
from user.models import Address, Account, Person
from product.models import Product
# Create your models here.

class Store(models.Model) : 
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=200)
class Payment(models.Model) : 
    methodChoice = [('BANK' , 'BANK'), ('COD', "COD")]
    paymentDate = models.DateTimeField()
    amount = models.FloatField()
    paymentMethod = models.CharField(max_length=200, choices=methodChoice)
class Shipping(models.Model) : 
    status  = [("SHIPPING" , "SHIPPING"),
    ("DONE" , "DONE"),
    ('PROCESSING' , "PROCESSING")]
    companyName = models.CharField(max_length=200)
    shipperName = models.CharField(max_length=200)
    shipperPhone = models.CharField(max_length=200)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipStatus = models.CharField(max_length=200, choices=status, default="PROCESSING")
class Order(models.Model) :
    date = models.DateTimeField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)  
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, null=True)
class OrderLine(models.Model) :
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    unitPrice = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
class SHIP_STATUS(Enum) :
    SHIPPING = "SHIPPING"
    DONE = "DONE"
    PROCESSING = "PROCESSING"
class Event(models.Model) : 
    name = models.CharField(max_length=200)
    startDate = models.DateField()
    endDate =models.DateField()
    description = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
class Discount(models.Model) : 
    discountRate = models.IntegerField()
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
class Warehouse(models.Model) :
    name = models.CharField(max_length=200)
    description = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
class Notification(models.Model) : 
    description = models.TextField()
    status = models.BooleanField() 
    store = models.ForeignKey(Store , on_delete=models.CASCADE) 
class NotificationAccount(models.Model) :
    account = models.ForeignKey(to = Account, on_delete=models.CASCADE )
    notification = models.ForeignKey(to = Notification, on_delete=models.CASCADE )
    isRead = models.BooleanField()