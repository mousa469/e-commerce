from typing import Any

from rest_framework import serializers

import cart
from cart.models import CartItem, Cart
from core.exceptions import CustomValidationError
from products.api.serializers import ProductVariantSerializer
from products.models import ProductVariants


class CreateCartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(required=False, default=1, min_value=1)
    class Meta:
        model = CartItem
        fields = ["product_variant"  , "quantity" ]

    def validate(self, attrs: Any) -> Any:
        product_variant = attrs["product_variant"]
        quantity = attrs["quantity"]
        if quantity > product_variant.quantity  :
            raise CustomValidationError(f"Requested quantity exceeds available stock. Only {product_variant.quantity} items are available.")
        return attrs

    def create(self, validated_data: dict):
        product_variant = validated_data.get("product_variant")
        quantity = validated_data.get("quantity")
        CartItem.objects.create(cart = cart , product_variant = product_variant , quantity = quantity)




class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ["id" , "quantity"  , "cart" , "product_variant" ,  "created_at" , "updated_at"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

    def validate(self, attrs: Any):
            cartItem =  self.context["object"]
            quantity = attrs.get("quantity")
            if quantity > cartItem.quantity:
                raise CustomValidationError("Quantity cannot exceed available stock.")
            return attrs







