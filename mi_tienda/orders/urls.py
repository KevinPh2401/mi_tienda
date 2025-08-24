from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/method/', views.payment_method, name='payment_method'),
    path('payment/process/', views.payment_process, name='payment_process'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('', views.order_list, name='order_list'),
]