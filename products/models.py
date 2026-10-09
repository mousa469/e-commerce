from django.utils import timezone
from django.core.validators import MinValueValidator , MaxValueValidator
from django.db import models

from core.exceptions import CustomValidationError
from core.models import BaseModel

# Create your models here.


class Category(BaseModel):
    name = models.CharField(max_length=200 , null=False, blank=False ,unique=True)
    is_available = models.BooleanField(null=False, blank=False , default=True)

    def __str__(self):
        return self.name



class Product(BaseModel):
    SIZE_ORDER = {"XXS": 1,"XS": 2,"S": 3,"M": 4,"L": 5,"XL": 6,"XXL": 7,"3XL": 8,"4XL": 9,"5XL": 10,"OS": 11,}
    name = models.CharField(max_length=200 , unique=True, null=False, blank=False)
    description = models.TextField( null=False, blank=False )
    category = models.ForeignKey(Category , on_delete=models.PROTECT ,related_name='products' , null=False, blank=False)
    brand = models.CharField(max_length=200 , null=False, blank=False)
    price = models.DecimalField(null=False, blank=False ,validators=[MinValueValidator(0.00)] , max_digits=10,decimal_places=2,)
    image = models.ImageField(upload_to="products/", null=False, blank=False)
    is_available = models.BooleanField(null=False, blank=False , default=True)

    def __str__(self):
        return self.name

    def get_active_discount(self):
        if hasattr(self, 'active_discounts'):
            return self.active_discounts[0] if self.active_discounts else None
        return None

    def get_effective_price(self):
        discount = self.get_active_discount()
        if discount:
            percentage = discount.percentage
            price = self.price - ((self.price * percentage) / 100)
            return price
        return self.price

    def get_product_available_variants(self):
        variants = self.available_variants
        return variants

    def get_Product_available_sizes(self):
        variants = self.get_product_available_variants()
        sizes = {v.size for v in variants}
        return sorted(sizes , key=lambda s : self.SIZE_ORDER.get(s, 99))


class ProductVariants(BaseModel):
        product = models.ForeignKey(Product , on_delete=models.CASCADE ,related_name='variants' , null=False, blank=False)
        color = models.CharField(max_length=200 , null=False, blank=False)
        size = models.CharField(max_length=200 , null=False, blank=False)
        image = models.ImageField(upload_to="products/", null=False, blank=False)
        quantity = models.PositiveIntegerField(null=False, blank=False)
        is_available = models.BooleanField(null=False, blank=False , default=True)

        class Meta:
            unique_together = (('product', 'color','size'),)


        def __str__(self):
            return f"{self.product.name} - {self.color} - {self.size}"


class Discount(BaseModel):
    product = models.ForeignKey(Product , on_delete=models.CASCADE ,related_name='discounts' , null=False, blank=False)
    percentage = models.DecimalField(null=False, blank=False, max_digits=5, decimal_places=2 , validators=[MaxValueValidator(100) , MinValueValidator(1)])
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=False, blank=False)
    is_available = models.BooleanField(null=False, blank=False )

    def clean(self):
        if self.percentage <= 0 or self.percentage > 100:
            raise CustomValidationError("Percentage must be between 0 and 100.")
        if self.end_date <= self.start_date:
            raise CustomValidationError("end date must be after start date.")
