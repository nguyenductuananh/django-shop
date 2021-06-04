from django.contrib import messages
from order.models import Order, OrderLine, Shipping
from django.shortcuts import redirect, render
from product.models import Category, Product
from user.models import Person
# Create your views here.
def index(request) :
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
    except : 
        return redirect('/user/login/')
    try : 
        q = request.GET.get('q')
        products = Product.objects.filter(name__contains=q)
        return render(request, 'page/index.html', {'products' : products})
    except : 
        products = Product.objects.all()
        return render(request, 'page/index.html', {'products' : products})
def update_item(request, id) :
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
    except : 
        return redirect('/user/login/')
    if request.method == 'GET' :
        product = Product.objects.get(id = id)
        categories = Category.objects.all()
        return render(request, 'update-item/index.html', {'product' : product, 'categories' : categories})
    if request.method == 'POST' :
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category = request.POST.get('category')
        Product.objects.filter(id = id).update(name = name, price = price, description = description, category = Category(id = category))
        return redirect('/employee/')
def add_item(request) :
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
    except : 
        return redirect('/user/login/')
    if request.method == 'GET' :
        categories = Category.objects.all()
        return render(request, 'create-item/index.html', {'categories' : categories})
    if request.method == 'POST' :
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category = request.POST.get('category')
        Product.objects.create(name = name, price = price, description = description, category = Category(id = category))
        return redirect('/employee/')
def delete_item(request, id) :
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
    except : 
        return redirect('/user/login/')
    product  = Product(id = id)
    Product.delete(product)
    return redirect('/employee/')
def orders(request) : 
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
    except : 
        return redirect('/user/login/')
    shipping = Shipping.objects.filter(shipStatus = "PROCESSING")
    orders = Order.objects.filter(shipping__in = shipping)
    return render(request, 'page/orders.html', {"orders" : orders})
def detailed_order(request, id) :
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
    except : 
        return redirect('/user/login/')
    order= Order.objects.get(id = id)
    products = OrderLine.objects.filter(order_id = order.id)
    return render(request, 'page/detailed-order.html', {"order" : order, "products" : products}) 
def shipping_orders(request) : 
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
    except : 
        return redirect('/user/login/')
    shipping = Shipping.objects.filter(shipStatus = "SHIPPING")
    orders = Order.objects.filter(shipping__in = shipping)
    return render(request, 'page/orders.html', {"orders" : orders})
def shipped_change(request, id) : 
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
    except : 
        return redirect('/user/login/')
    order = Order.objects.get(id = id)
    Shipping.objects.filter(id = order.shipping.id).update(shipStatus = "SHIPPING")
    return redirect('/employee/orders/')
    