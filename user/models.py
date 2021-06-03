from django.db import models
from enum import Enum
# Create your models here.
class ROLE(Enum) :
    CUSTOMER = 0
    MANAGER = 2
    EMPLOYEE = 1
class Account(models.Model) :
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    role = models.IntegerField(default=0)
class FullName(models.Model) :
    firstName = models.CharField(max_length=200)
    middleName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
class Address(models.Model) :
    province = models.CharField(max_length=200)
    wards = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    addressDetail = models.CharField(max_length=200)
class Person(models.Model) :
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    dob = models.DateField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='updated_by_person')
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='updated_by_person')
    fullName = models.OneToOneField(FullName, on_delete=models.CASCADE, related_name='updated_by_person')
