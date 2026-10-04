from itertools import product

from rest_framework import serializers

from products.models import Category, Product, ProductVariants
from core.exceptions import CustomValidationError
from core.services import calculate_price_after_discount


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariants
        fields = [
            "id",
            "product",
            "size",
            "color",
            "image",
            "quantity",
        ]


class ProductSerializer(serializers.ModelSerializer):
    rate = serializers.FloatField(read_only=True)
    discounted_price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = ["id", "name"  ,"price" ,  "discount" ,  "discounted_price", "image" , "rate"]
        read_only_fields = ["id"]

    def get_discounted_price(self, obj):
        discounted_price = obj.price  - calculate_price_after_discount(price = obj.price  ,discount=obj.discount)
        return discounted_price




class ReadProductDetailsSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()
    rate = serializers.FloatField(read_only=True)
    discounted_price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "brand",
            "price",
            "discount",
            "discounted_price",
            "image",
            "rate",
            "variants"
        ]

    def get_discounted_price(self, obj):
            discounted_price = calculate_price_after_discount(price=obj.price, discount=obj.discount)
            return discounted_price



    def get_variants(self, obj):
        variants = obj.variants.filter(is_available=True)
        return ProductVariantSerializer(
            variants,
            many=True
        ).data


