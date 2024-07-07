from django.contrib import admin
from django.urls import include, path
from app import views


urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('product/', views.product, name='product'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.loginUser, name='login'),
    path("logout/", views.logoutUser, name="logout"),
    path('signup/', views.signupuser, name='signup'),
    path('shop/', views.shop, name='shop'),
    path('buy/', views.buy, name='buy'),  # For handling multiple products from the cart
    path('buy/<int:product_id>/', views.buy, name='buy_single'),  # For handling single product purchase
    path('productdetails/<int:pk>/', views.productdetails, name='productdetails'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
]