from django.db import models
from django.contrib import admin
from enum import Enum
from user.models import Address, Account, Person
from product.models import Product, Supplier
# Create your models here.
class Feedback(models.Model) : 
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=50)
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
    status  = [(1 , "SHIPPING"),
    (2, "DONE"),
    (0 , "PROCESSING")]
    companyName = models.CharField(max_length=200)
    shipperName = models.CharField(max_length=200)
    shipperPhone = models.CharField(max_length=200)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipStatus = models.IntegerField(choices=status, default=0)
class Order(models.Model) :
    date = models.DateTimeField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)  
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return 'Order ' + self.date.strftime("%d/%m/%y-%H:%M:%S")
    
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
    store = models.ForeignKey(Store , on_delete=models.CASCADE) 
# Bonus
class NotificationAccount(models.Model) :
    account = models.ForeignKey(to = Account, on_delete=models.CASCADE )
    notification = models.ForeignKey(to = Notification, on_delete=models.CASCADE )
    isRead = models.BooleanField()
class ImportedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    importPrice = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField( auto_now=False, auto_now_add=False)
    class Meta:
        verbose_name = ("ImportedProduct")
        verbose_name_plural = ("ImportedProducts")

    def get_absolute_url(self):
        return reverse("ImportedProduct_detail", kwargs={"pk": self.pk})
class ProductInStock(models.Model) :
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    importPrice = models.IntegerField()
class OrderNotification(models.Model) : 
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    description = models.TextField()
class OrderNotificationAccount(models.Model) :
    person = models.ForeignKey(Person, on_delete=models.CASCADE) 
    isRead = models.BooleanField()
    orderNotification = models.ForeignKey(OrderNotification, on_delete=models.CASCADE)
class OrderFeedback(models.Model) : 
    isFeedback = models.BooleanField(default=False)
    quality = models.IntegerField( choices=[(1, "Terrible"), (2, "Bad"), (3, "OK"), (4, "Good"), (5, "Awesome")])
    action = models.IntegerField(choices=[(1, "Tr??? h??ng"), (2, "Kh??ng")])
    content = models.TextField()
    order = models.ForeignKey(Order , on_delete=models.CASCADE, null=True)