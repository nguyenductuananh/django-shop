from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Product, Cart, Comment, Rate, SelectedProduct
from user.models import  Person
from order.models import Order, OrderLine, Payment, Shipping
from django.utils import timezone
# Create your views here.
def index(request) : 
    try : 
        person = Person.objects.get(id = request.COOKIES['person_id'])
        items = Product.objects.all()
        return render(request, 'homepage/index.html', {"items" : items, "person" : person})
    except :
        return redirect('/user/login/')
def cart(request) :
    per = Person.objects.get(id = request.COOKIES['person_id'])
    cart = Cart.objects.get(account_id = per.account_id)
    selectedProducts = SelectedProduct.objects.filter(cart_id = cart.id)
    total = 0
    for p in selectedProducts : 
        total += p.product.price * p.quantity
    return render(request, 'cart/index.html', {"selectedProducts" : selectedProducts, 'total' : total, "person" : per})
def add_to_cart(request, id) : 
    try : 
        per = Person.objects.get(id = request.COOKIES['person_id'])
        cart = Cart.objects.get(account_id = per.account_id)
        selectedProduct = Product(id = id)
        s = SelectedProduct.objects.filter(cart = cart, product = selectedProduct)
        s.update(quantity = s[0].quantity + 1)
    except : 
        sp = SelectedProduct.objects.create(cart = cart, product = selectedProduct, quantity = 1)
        sp.save()
    messages.success(request, message='Mặt hàng đã được thêm vào giỏ')
    return redirect('/')

def item(request, id) : 
    product = Product.objects.filter(id = id)
    comments = Comment.objects.filter(item_id = id)
    return render(request, 'item/index.html', {"product" : product[0], "comments" : comments})
def rate_item(request, id) : 
    content = request.POST.get('content')
    rate = int(request.POST.get('rate'))
    created = timezone.now()
    item = Product(id = id)
    account = Person.objects.get(id = request.COOKIES['person_id']).account
    url = request.GET.get('next')
    Comment.objects.create(content = content, account = account, created = created, item = item)
    Rate.objects.create(rate = rate, account = account, created = created, item = item)
    return redirect(url)

def create_order(request) :
    if request.method == "GET" :
        person = Person.objects.get(id = request.COOKIES['person_id'])
        cart = Cart.objects.get(account_id = person.account_id)
        products = SelectedProduct.objects.filter(cart_id = cart.id)
        if len(products) == 0  :
            messages.warning(request, message='Bạn cần chọn ít nhât một sản phẩm để thanh toán')
            return redirect('/')
        total = 0
        for pro in products : 
            total += pro.product.price * pro.quantity       
        return render(request, 'order/create-order.html', {"person" : person, "products" : products, "total" : total})
    if request.method == "POST" :
        person = Person.objects.get(id = request.COOKIES['person_id'])
        cart = Cart.objects.get(account_id = person.account_id)
        products = SelectedProduct.objects.filter(cart_id = cart.id)        
        paymentMethod = request.POST.get("paymentmethod")
        total = request.POST.get("total")
        payment = Payment.objects.create(amount = total, paymentMethod = paymentMethod, paymentDate = timezone.now())
        payment.save()
        shipping = Shipping.objects.create(companyName="GHTK", shipperName = "Nguyen Duc Tuan Anh", shipperPhone="012345678", address = person.address)
        shipping.save()
        order = Order.objects.create(payment = payment, date = timezone.now(), person = person, shipping = shipping)
        order.save()   
        for product in products : 
            OrderLine.objects.create(product= product.product, unitPrice = product.product.price, quantity = product.quantity, order = order)
        products.delete()
        messages.success(request, message="Hóa đơn đã được nhận!")
        return redirect('/')
def view_orders(request) :
    try : 
        person = Person.objects.get(id = request.COOKIES['person_id'])
        orders = Order.objects.filter(person_id = request.COOKIES['person_id'])
        return render(request, 'order/view-order.html', {'orders' : orders, "person" : person})
    except : 
        return redirect('/user/login/')
def remove_item(request, id) : 
    SelectedProduct.objects.filter(id = id).delete()
    return redirect('/cart')