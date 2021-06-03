from order.models import Order, Shipping
from django.shortcuts import redirect, render
from product.models import Category, Product
from user.models import Person
# Create your views here.
def index(request) :
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
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
    product  = Product(id = id)
    Product.delete(product)
    return redirect('/employee/')
def orders(request) : 
    shipping = Shipping.objects.filter(shipStatus = "PROCESSING")
    orders = Order.objects.filter(shipping__in = shipping)
    return render(request, 'page/orders.html', {"orders" : orders})
def detailed_order(request, id) :
    order= Order.objects.get(id = id)
    return render(request, 'page/detailed-order.html', {"order" : order}) 
def shipping_orders(request) : 
    shipping = Shipping.objects.filter(shipStatus = "SHIPPING")
    orders = Order.objects.filter(shipping__in = shipping)
    return render(request, 'page/orders.html', {"orders" : orders})
def shipped_change(request, id) : 
    order = Order.objects.get(id = id)
    Shipping.objects.filter(id = order.shipping.id).update(shipStatus = "SHIPPING")
    return redirect('/employee/orders/')
    