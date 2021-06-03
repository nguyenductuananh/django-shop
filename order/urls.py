from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='employee-index'),
    path('update-item/<int:id>/', views.update_item, name='update'),
    path('add-item/', views.add_item, name='add'),
    path('delete-item/<int:id>/', views.delete_item, name='delete'),
    path('orders/', views.orders, name='orders-list'),
    path('order/<int:id>', views.detailed_order, name='orders-list'),
    path('shipping-orders/', views.shipping_orders, name='orders-list'),
    path('shipped/<int:id>', views.shipped_change, name='shipped'),
]