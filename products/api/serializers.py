from itertools import product

from rest_framework import serializers

from products.models import Category, Product, ProductVariants
from core.exceptions import CustomValidationError


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
    class Meta:
        model = Product
        fields = ["id", "name" , "description" , "brand" , "category" ,"price" , "image" , "rate"]
        read_only_fields = ["id"]




class ReadProductDetailsSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()
    rate = serializers.FloatField(read_only=True)
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "brand",
            "price",
            "image",
            "is_available",
            "rate",
            "variants"
        ]

    def get_variants(self, obj):
        variants = obj.variants.filter(is_available=True)
        return ProductVariantSerializer(
            variants,
            many=True
        ).data


