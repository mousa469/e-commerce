from django.contrib import admin
from .models import Cart , CartItem

# Register your models here.

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    model = CartItem
    list_display = ["id" , "product_variant" , "cart" , "quantity"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ["id" , "user"]
