from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('my-receipts/', views.my_receipts, name='my_receipts'),
    path('create-receipt/', views.create_receipt, name='create_receipt'),
    path('receipt/<int:pk>/', views.receipt_detail, name='receipt_detail'),
]