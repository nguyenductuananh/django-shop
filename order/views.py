from django.contrib import messages
from django.utils import timezone
from order.models import ProductInStock, Order, OrderLine, Shipping, OrderNotification, OrderNotificationAccount , Warehouse, ImportedProduct
from django.shortcuts import redirect, render
from product.models import Category, Product, Supplier
from user.models import Person
# Create your views here.
def index(request) :
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
        q = request.GET.get('q')
        products = Product.objects.filter(name__contains=q)
        return render(request, 'page/index.html', {'products' : products, "person" : person})
    except KeyError: 
        return redirect('/user/login/')
    except : 
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
        products = Product.objects.all()
        return render(request, 'page/index.html', {'products' : products, "person" : person})
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
        next =request.GET.get('next')
        return redirect(next or '/employee/')
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
    if request.method == 'GET' : 
        try :
            person = Person.objects.get(id = request.COOKIES["person_id"])
            if person.account.role == 0 :
                messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
                return redirect('/')
        except : 
            return redirect('/user/login/')
        shipping = Shipping.objects.filter(shipStatus = "SHIPPING")
        orders = Order.objects.filter(shipping__in = shipping)
        return render(request, 'page/shipping-orders.html', {"orders" : orders})
    if request.method == "POST" : 
        orderId = request.POST.get('orderId')
        order = Order.objects.get(id = orderId)
        Shipping.objects.filter(id = order.shipping.id).update(shipStatus = "DONE")
        orderNoti = OrderNotification.objects.create(order_id = order.id, description="Đơn hàng đã được giao thành công!!")
        orderNoti.save()
        ona = OrderNotificationAccount.objects.create(person_id = order.person_id, orderNotification_id = orderNoti.id, isRead = False)
        return redirect('./')
def shipped_change(request, id) : 
    try :
        person = Person.objects.get(id = request.COOKIES["person_id"])
        if person.account.role == 0 :
            messages.warning(request, message="Đường dẫn không đúng hoặc không có quyền truy nhập")
            return redirect('/')
        order = Order.objects.get(id = id)
        Shipping.objects.filter(id = order.shipping.id).update(shipStatus = "SHIPPING")
        orderNoti = OrderNotification.objects.create(order_id = order.id, description="Đơn hàng của bạn đang được vận chuyển. Vui lòng đợi cho tới khi nhận được cuộc gọi của người giao hàng")
        orderNoti.save()
        ona = OrderNotificationAccount.objects.create(person_id = order.person_id, orderNotification_id = orderNoti.id, isRead = False)
        ona.save()
        return redirect('/employee/orders/')
    except : 
        return redirect('/user/login/')
def import_item(request) : 
    if request.method == 'GET' : 
        products = Product.objects.all()
        warehouses = Warehouse.objects.all()
        suppliers = Supplier.objects.all()
        return render(request, 'page/import-item.html', {"products" : products, "warehouses" : warehouses, "suppliers" : suppliers})
    if request.method == "POST" : 
        productid = request.POST.get('product')
        warehouseid = request.POST.get('warehouse')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        supplierid = request.POST.get('supplier')
        importedProduct = ImportedProduct.objects.create(product_id = productid, supplier_id = supplierid, warehouse_id = warehouseid, importPrice = price, quantity= quantity, date = timezone.now())
        importedProduct.save()
        try : 
            productInStock = ProductInStock.objects.get(product_id = productid, warehouse_id = warehouseid)
            ProductInStock.objects.filter(id = productInStock.id).update(quantity = productInStock.quantity + quantity)
        except : 
            ProductInStock.objects.create(product_id = productid, warehouse_id = warehouseid, importPrice = price, quantity = quantity)
        return redirect('/employee/') 
