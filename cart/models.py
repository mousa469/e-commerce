from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

from products.models import ProductVariants
from core.models import BaseModel


# Create your models here.


class Cart(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='cart')

    def __str__(self):
        return f"cart of  {self.user}"






class CartItem(BaseModel):
    product_variant = models.ForeignKey(ProductVariants, on_delete=models.PROTECT , related_name="cart_items")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , related_name='items')
    quantity = models.PositiveIntegerField(default=1, null=False, blank=False , validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('product_variant', 'cart')

