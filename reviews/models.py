from django.core.validators import MinValueValidator ,MaxValueValidator
from django.db import models

from products.models import Product
from core.models import BaseModel
from accounts.models import User


# Create your models here.

class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL , related_name='reviews' , null=True)
    review = models.TextField()
    rate = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('product', 'user'),)