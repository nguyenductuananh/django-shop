from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='addcart'),
    path('item/<int:id>/', views.item, name = 'item'),
    path('comment/<int:id>/', views.rate_item, name='comment-rate'),
    path('create-order/', views.create_order, name = 'create-order'),
]