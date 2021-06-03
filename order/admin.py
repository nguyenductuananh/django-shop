from django.contrib import admin
from .models import NotificationAccount, Order, Payment, Store, Warehouse, Shipping, OrderLine, Notification, Event ,Discount
# Register your models here.
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Store)
admin.site.register(Warehouse)
admin.site.register(Shipping)
admin.site.register(OrderLine)
admin.site.register(Notification)
admin.site.register(Event)
admin.site.register(Discount)
admin.site.register(NotificationAccount)