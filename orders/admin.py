from django.contrib import admin

from orders.models import OrderItem, Order



# Register your models here.
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
        model = OrderItem
        list_display = ["id" ,  "order" ,"quantity" , "product_variant" , "unit_price"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ["id" , "user" , "status" , "total_price" , "shipping_address" , "notes"]
