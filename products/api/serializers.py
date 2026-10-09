from django.utils import timezone
from rest_framework import serializers

from products.models import Category, Product, ProductVariants, Discount
from core.exceptions import CustomValidationError
from core.services import calculate_price_after_discount


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):
    in_stock = serializers.SerializerMethodField()
    class Meta:
        model = ProductVariants
        fields = [
            "id",
            "product",
            "size",
            "color",
            "image",
            "quantity",
            "in_stock",
        ]

    def get_in_stock(self, obj):
        return obj.quantity > 0


class ProductSerializer(serializers.ModelSerializer):
    rate = serializers.FloatField(read_only=True)
    discount = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    # sizes = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id", "name"  ,"price" , "discount" ,  "discounted_price" , "image" , "rate"]
        read_only_fields = ["id"]

    def get_discount(self, obj):
        discount = obj.get_active_discount()
        if discount:
            return discount.percentage
        return 0

    def get_discounted_price(self, obj):
        return  obj.get_effective_price()

class ReadProductDetailsSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()
    rate = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    discount = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
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
            "reviews_count",
            "variants"
        ]
    def get_discount(self,obj):
        discount = obj.get_active_discount()
        if discount:
            return discount.percentage
        return 0

    def get_discounted_price(self, obj):
        price = obj.get_effective_price()
        return price

    def get_variants(self, obj):
        variants = obj.variants.filter(is_available=True)
        return ProductVariantSerializer(
            variants,
            many=True
        ).data


class CreateDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ["product", "percentage" , "start_date" , "end_date", "is_available"]

    def validate(self, attrs):
        instance = self.instance
        product = attrs.get("product" , instance.product if instance else None)
        percentage = attrs.get("percentage" , instance.percentage if instance else None)
        start_date = attrs.get("start_date" , instance.start_date if instance else None)
        end_date = attrs.get("end_date" , instance.end_date if instance else None)
        is_available =  attrs.get("is_available" , instance.is_available if instance else None)
        now = timezone.now()

        if start_date < now:
            raise CustomValidationError("The start date must be a future date")

        if end_date  < start_date :
            raise CustomValidationError("End date must be greater than start date")

        if is_available:
            overlap_qs = Discount.objects.filter(
                product=product, is_available=True,
                start_date__lt=end_date, end_date__gt=start_date,
            )
            if instance:
                overlap_qs = overlap_qs.exclude(pk=instance.pk)
            if overlap_qs.exists():
                raise CustomValidationError("An active or overlapping discount already exists for this product.")

        return attrs


class DiscountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
       model = Discount
       fields = ["id" , "product" ,  "percentage" , "start_date" , "end_date" , "is_available" , "created_at" , "updated_at"]