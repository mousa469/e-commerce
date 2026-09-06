from typing import Any

from rest_framework import serializers
from cart.models import CartItem
from core.exceptions import CustomValidationError
from products.api.serializers import ProductVariantSerializer
from products.models import ProductVariants


class CreateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product_variant"  , "quantity" ]

    def validate(self, attrs: Any) -> Any:
        product_variant = attrs.get("product_variant")
        quantity = attrs.get("quantity")

        if quantity > product_variant.quantity:
            raise CustomValidationError("Quantity cannot exceed available stock.")
        return attrs



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







