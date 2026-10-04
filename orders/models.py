from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from core.models import BaseModel
from products.models import ProductVariants


# Create your models here.
class Order(BaseModel):

    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders"
    )



    status = models.CharField(
        max_length=20,
        choices=[
            (PENDING, "Pending"),
            (SHIPPED, "Shipped"),
            (DELIVERED, "Delivered"),
            (CANCELLED, "Cancelled"),
        ],
        default="pending"
    )

    # payment_status = models.CharField(
    #     max_length=20,
    #     choices=[
    #         ("pending", "Pending"),
    #         ("paid", "Paid"),
    #         ("failed", "Failed"),
    #         ("refunded", "Refunded"),
    #     ],
    #     default="pending"
    # )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    shipping_address = models.TextField(null=False, blank=False)

    notes = models.TextField(
        blank=True,
        null=True
    )


    def __str__(self):
        return f"{self.id}"

    def get_status_display(self):
        return f"{self.status}"


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_variant = models.ForeignKey(
        ProductVariants,
        on_delete=models.PROTECT,
        related_name="order_items"
    )

    quantity = models.PositiveIntegerField(default=1 , blank=False, null=False)

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )