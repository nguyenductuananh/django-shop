from django.contrib import admin
from .models import Account, Person, Address, FullName
# Register your models here.
admin.site.register(Account)
admin.site.register(Person)
admin.site.register(Address)
admin.site.register(FullName)