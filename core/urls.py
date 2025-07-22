from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Default homepage
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),  
    path('contact/', views.contact, name='contact'),
    path('cart/<int:pk>/', views.cart, name='cart'),
    path('shop-single/<int:pk>/', views.shop_single, name='shop_single'),
    path('search/', views.search, name='search'),
    # Removed duplicate '' path
    path('home/', views.home, name='home'),  # Changed '' to 'home/' to avoid conflict
    path('checkout/', views.checkout, name='checkout'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('register/', views.register, name='regis'),
    path('login/', views.login_v, name='logn'),
    path('add_product',views.add_product,name='add_product'),
    path('orderlist',views.orderlist,name='orderlist'),
    path('payment',views.payment,name='payment'),   
    path('handlerequest/', views.handlerequest, name='handlerequest'),
    path('search_results/', views.search_results, name='search_results'),           
]
