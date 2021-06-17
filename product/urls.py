from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='addcart'),
    path('item/<int:id>/', views.item, name = 'item'),
    path('remove-from-cart/<int:id>/', views.remove_item, name = 'item'),
    path('comment/<int:id>/', views.rate_item, name='comment-rate'),
    path('create-order/', views.create_order, name = 'create-order'),
    path('orders/', views.view_orders, name = 'list-order'),
    path('order/<int:orderId>/', views.view_order, name = 'view-order'),
    path('report/', views.feedback, name = 'feedback'),
    path('buy-now/<int:id>/', views.buynow, name='buynow'),
    path('noti/<int:id>/', views.change_noti, name="change-notification"),
    path('onoti/<int:id>/', views.change_onoti, name="change-order-notification"),
    path('feedback-order/<int:id>/', views.feedback_order, name="feedback-order"),
    path('detail-feedback/<int:id>/', views.detail_feedback, name="feedback-order"),
]