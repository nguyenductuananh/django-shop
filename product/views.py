from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Product, Cart, Comment, Rate, SelectedProduct, Category
from user.models import  Person
from order.models import Feedback, ProductInStock, Order, OrderLine, Payment, Shipping, NotificationAccount, OrderNotification, OrderNotificationAccount
from django.utils import timezone
# Create your views here.
def index(request) : 
    # try :   
        person = Person.objects.get(id = request.COOKIES['person_id'])
        categories = Category.objects.all()
        q = request.GET.get('type')
        s = request.GET.get('search')
        items = []
        if q :
            items = queryItemByType(q)
        elif s : 
            products = Product.objects.filter(name__contains = s)
            items = ProductInStock.objects.filter(product__in = products)
        else : items = ProductInStock.objects.all()
        if len(items) == 0 : 
            messages.warning(request, message = "Không có kết quả tìm kiếm phù hợp!")
        notifications = NotificationAccount.objects.filter(account_id = person.account.id, isRead = False)
        orderNotifications = OrderNotificationAccount.objects.filter(person_id = person.id, isRead = False)
        notificationsNum = len(notifications) + len(orderNotifications)
        return render(request, 'homepage/index.html', {"items" : items, "categories" : categories, "person" : person, "notificationsNum" : notificationsNum, "notifications" : notifications, "orderNotifications" : orderNotifications})
    # except :
    #     return redirect('/user/login/')
def queryItemByType(t) : 
        if t == "book" :
            category = Category.objects.get(query = t)
            return ProductInStock.objects.filter(product__in = Product.objects.filter(category = category))
        elif t == "electronic" : 
            category = Category.objects.get(query = t)
            return ProductInStock.objects.filter(product__in = Product.objects.filter(category = category))
        else : return ProductInStock.objects.all()
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
            productInStock = ProductInStock.objects.get(product_id = product.product.id)
            ProductInStock.objects.filter(product_id = product.product.id).update(quantity = productInStock.quantity - product.quantity)
            OrderLine.objects.create(product= product.product, unitPrice = product.product.price, quantity = product.quantity, order = order)
        products.delete()
        orderNoti = OrderNotification.objects.create(order_id = order.id, description = "Đơn hàng của bạn được khởi tạo thành công.")
        orderNoti.save()
        ona = OrderNotificationAccount.objects.create(orderNotification_id = orderNoti.id, person_id = person.id, isRead = False)
        ona.save()
        return redirect('/')
def view_orders(request) :
    try : 
        person = Person.objects.get(id = request.COOKIES['person_id'])
        orders = Order.objects.filter(person_id = request.COOKIES['person_id'])
        return render(request, 'order/view-order.html', {'orders' : orders, "person" : person})
    except : 
        return redirect('/user/login/')
def view_order(request, orderId) :
    try : 
        person = Person.objects.get(id = request.COOKIES['person_id'])
        order = Order.objects.get(person_id = request.COOKIES['person_id'], id = orderId)
        orderLines = OrderLine.objects.filter(order_id = order.id)
        return render(request, 'order/detail-order.html', {'orderLines' : orderLines, 'order' : order, "person" : person})
    except : 
        return redirect('/user/login/')
def remove_item(request, id) : 
    SelectedProduct.objects.filter(id = id).delete()
    return redirect('/cart')
def feedback(request) :
    # try :
        person = Person.objects.get(id = request.COOKIES['person_id'])
        if (request.method == "POST") :
            content = request.POST.get('feedback-content')
            feedback = Feedback.objects.create(person = person, status = "RECEIVED", content= content)
            messages.success(request, message="Phản ánh của bạn đã được tiếp nhận. Chúng tôi sẽ khắc phục trong thời gian sớm nhất. Xin lỗi vì sự bất tiện này")
        return render(request, 'feedback/index.html', {})
def buynow(request, id) : 
    if request.method == 'GET' : 
        person =  Person.objects.get(id = request.COOKIES['person_id'])
        product = Product.objects.get(id = id)
        products = SelectedProduct(product = product)
        return render(request, 'order/create-order.html', {'person' : person, 'product' : product})
    elif request.method == "POST" : 
        person = Person.objects.get(id = request.COOKIES['person_id'])
        cart = Cart.objects.get(account_id = person.account_id)
        product = Product.objects.get(id = id)    
        paymentMethod = request.POST.get("paymentmethod")
        total = product.price
        payment = Payment.objects.create(amount = total, paymentMethod = paymentMethod, paymentDate = timezone.now())
        payment.save()
        shipping = Shipping.objects.create(companyName="GHTK", shipperName = "Nguyen Duc Tuan Anh", shipperPhone="012345678", address = person.address)
        shipping.save()
        order = Order.objects.create(payment = payment, date = timezone.now(), person = person, shipping = shipping)
        order.save()  
        productInStock = ProductInStock.objects.get(product_id = product.id)
        ProductInStock.objects.filter(product_id = product.id).update(quantity = productInStock.quantity - 1)
        OrderLine.objects.create(product= product, unitPrice = product.price, quantity = 1, order = order)
        orderNoti = OrderNotification.objects.create(order_id = order.id, description = "Đơn hàng của bạn được khởi tạo thành công.")
        orderNoti.save()
        ona = OrderNotificationAccount.objects.create(orderNotification_id = orderNoti.id, person_id = person.id, isRead = False)
        ona.save()
        return redirect('/')   
def change_noti(request, id) :
    person = Person.objects.get(id = request.COOKIES['person_id'])
    NotificationAccount.objects.filter(person_id = person.id, id = id).update(isRead = True)
    return redirect('/')
def change_onoti(request, id) :
    person = Person.objects.get(id = request.COOKIES['person_id'])
    OrderNotificationAccount.objects.filter(person_id = person.id, id = id).update(isRead = True)
    return redirect('/')