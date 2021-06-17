import datetime
from django.db.models.fields import EmailField
from datetime import date, timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from product.models import Cart
from .models import Account, Address, FullName, Person
# Create your views here.
def login_index(request) :
    try : 
        if request.COOKIES['person_id'] : 
            return redirect('/')
    except:  
        if request.method == 'GET' : 
            return render(request, 'login/index.html', {})
        else : 
            try : 
                username = request.POST.get('username')
                password = request.POST.get('password')
                acc = Account.objects.get(username = username, password = password)
                person = Person.objects.get(account = acc)
                next = redirect('/')
                next.set_cookie('person_id', person.id)
                request.session['account_id'] = person.account_id
                return next
            except : 
                messages.warning(request, 'Wrong username or password')
                return render(request, 'login/index.html')
def logout_index (request) : 
    res = redirect('/user/login/')
    res.delete_cookie('person_id')
    return res
def register_index(request) : 
    if request.method == 'GET' : 
        return render(request, 'register/index.html', {})
    elif request.method == 'POST' : 
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstName = request.POST.get('firstName')
        middleName = request.POST.get('middleName')
        lastName = request.POST.get('lastName')
        wards = request.POST.get('wards')
        province = request.POST.get('province')
        district = request.POST.get('district')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        acc = Account(username = username, password = password, role = 0)
        acc.save()
        fullName = FullName.objects.create(middleName = middleName, firstName = firstName, lastName = lastName)
        fullName.save()
        cart = Cart.objects.create(account_id = acc.id)
        cart.save()
        address = Address.objects.create(wards = wards, province = province,district = district)
        Person.objects.create(address_id = address.id, account_id = acc.id, fullName_id = fullName.id, dob = dob, email = email, phone = phone)
        messages.success(request, "Create successfully, let's login...!")
        return redirect('/user/login/')
def user_index(request) :
    try : 
        person = Person.objects.get(id = request.COOKIES['person_id'])
        person.dob = person.dob.strftime('%Y-%m-%d')
        return render(request, 'user/index.html', {"person" : person})
    except : 
        return redirect('/user/login/')
def update_user(request) :
    try :
        if request.method == "GET" :
            u = Person.objects.get(id = request.COOKIES['person_id'])
            u.dob = u.dob.strftime('%Y-%m-%d')
            return render(request, 'user/update/index.html', {"person" : u})
        if request.method == "POST" :
            firstName = request.POST.get('firstName')
            middleName = request.POST.get('middleName')
            lastName = request.POST.get('lastName')
            wards = request.POST.get('wards')
            province = request.POST.get('province')
            district = request.POST.get('district')
            dob = request.POST.get('dob')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            person = Person.objects.filter(id = request.COOKIES['person_id'])
            person.update( dob = dob, email = email, phone = phone)
            FullName.objects.filter(id = person[0].fullName.id).update(middleName = middleName, firstName = firstName, lastName = lastName)
            Address.objects.filter(id = person[0].address.id).update(wards = wards, province = province,district = district)
            return redirect('../')
    except : 
        return redirect('/user/logout/')
