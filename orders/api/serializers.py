from rest_framework import serializers

from orders.models import Order, OrderItem


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["shipping_address" , "notes"]




class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "created_at"]



class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    variant = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields =[ "id" , "product_name", "variant", "quantity", "unit_price", "total_price"]

    def get_product_name(self, obj):
            return obj.product_variant.product.name

    def get_variant(self, obj):
            return { "id" : obj.product_variant.id , "color": obj.product_variant.color, "size": obj.product_variant.size , "image": obj.product_variant.image.url  }


class OrderDetailsSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id" , "user", "shipping_address" , "status" , "notes" , "total_price" , "items"  , "created_at" , "updated_at"]



class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]




