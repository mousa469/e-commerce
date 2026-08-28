from django.core.validators import MinValueValidator , MaxValueValidator
from django.db import models
from core.models import BaseModel

# Create your models here.


class Category(BaseModel):
    name = models.CharField(max_length=200 , null=False, blank=False ,unique=True)
    is_available = models.BooleanField(null=False, blank=False , default=True)

    def __str__(self):
        return self.name



class Product(BaseModel):
    name = models.CharField(max_length=200 , unique=True, null=False, blank=False)
    description = models.TextField( null=False, blank=False )
    category = models.ForeignKey(Category , on_delete=models.PROTECT ,related_name='products' , null=False, blank=False)
    brand = models.CharField(max_length=200 , null=False, blank=False)
    price = models.FloatField(null=False, blank=False ,validators=[MinValueValidator(0.00)])
    image = models.ImageField(upload_to="products/", null=False, blank=False)
    is_available = models.BooleanField(null=False, blank=False , default=True)

    def __str__(self):
        return self.name


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
