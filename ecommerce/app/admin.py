# admin.py
from django.contrib import admin
from .models import Product, CarouselImage , Cart, Profile, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'size', 'image', 'description') 

@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user' , "address" , "phone_number")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user","full_name","phone_number", "product","quantity","date","total","shipping_address","status")

    # custom actions 

    def delivered(self, request, queryset):
        queryset.update(status = Order.DELIVERED )

    def notDelivered(self, request, queryset):
        queryset.update(status = Order.NOT_DELIVERED )

    actions=[delivered,notDelivered,]


