from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login_index, name='login'),
    path('logout/', views.logout_index, name='logout'),
    path('register/', views.register_index, name='register'),
    path('', views.user_index, name='user'),
    path('update/', views.update_user, name='update_user'),
]