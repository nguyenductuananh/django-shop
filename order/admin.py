from django.contrib import admin
from .models import OrderFeedback, OrderNotification, OrderNotificationAccount, ProductInStock, ImportedProduct, NotificationAccount, Order, Payment, Store, Warehouse, Shipping, OrderLine, Notification, Event ,Discount
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
admin.site.register(ImportedProduct)
admin.site.register(OrderNotification)
admin.site.register(OrderNotificationAccount)
admin.site.register(ProductInStock)
admin.site.register(OrderFeedback)
