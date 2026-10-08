from typing import List

from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone

from cart.models import Cart, CartItem
from core.exceptions import CustomValidationError, CustomNotFound, UpdateOrderStatusException
from orders.models import Order , OrderItem
from products.models import ProductVariants, Product, Discount
from core.services import calculate_price_after_discount


class OrderService:
    ALLOWED_TRANSITIONS = {
        Order.PENDING: [Order.SHIPPED, Order.CANCELLED],
        Order.SHIPPED: [Order.DELIVERED, Order.CANCELLED],
        Order.DELIVERED: [],
        Order.CANCELLED: [],
    }

    @staticmethod
    def update_order_status(order_id, new_status = None):
     if new_status == Order.CANCELLED:
            order = OrderService.cancel(order_id=order_id  , allowed_transitions = (Order.PENDING , Order.SHIPPED ,))
            return order


     with transaction.atomic():
        try:
            order = Order.objects.select_for_update().get(pk=order_id)
        except Order.DoesNotExist:
            raise CustomNotFound()

        current_status = order.status
        if new_status not in OrderService.ALLOWED_TRANSITIONS.get(current_status, []):
            raise UpdateOrderStatusException(
                current_status=current_status,
                requested_status=new_status,
            )
        order.status = new_status
        order.save(update_fields=["status"])
     return order





    @staticmethod
    def place(user, data):
        with transaction.atomic():

            try:
                cart = Cart.objects.select_for_update().get(user=user)
            except Cart.DoesNotExist:
                raise CustomValidationError(
                    "Cannot create an order with an empty cart."
                )

            now = timezone.now()
            active_discounts = Discount.objects.filter(
                is_available=True, start_date__lte=now, end_date__gte=now
            )

            cart_items = list(
                cart.items
                .select_related("product_variant__product")
                .prefetch_related(
                    Prefetch("product_variant__product__discounts", queryset=active_discounts,
                             to_attr="active_discounts")
                )
                .select_for_update(of=("product_variant",))
                .order_by("product_variant_id")
            )

            if not cart_items:
                raise CustomValidationError(
                    "Cannot create an order with an empty cart."
                )

            order = Order.objects.create(
                user=user,
                shipping_address=data["shipping_address"],
                notes=data.get("notes"),
            )

            total_price = 0
            now = timezone.now()

            for cart_item in cart_items:

                variant = cart_item.product_variant


                if cart_item.quantity > variant.quantity:
                    raise CustomValidationError(
                        f"Insufficient stock for "
                        f"{variant.product.name} "
                        f"({variant.color}, {variant.size}). "
                        f"Available: {variant.quantity}, "
                        f"requested: {cart_item.quantity}."
                    )

                unit_price = variant.product.get_effective_price()

                item_total = unit_price * cart_item.quantity

                OrderItem.objects.create(
                    order=order,
                    product_variant=variant,
                    quantity=cart_item.quantity,
                    unit_price=unit_price,
                    total_price=item_total,
                )

                variant.quantity -= cart_item.quantity
                variant.save(update_fields=["quantity"])

                total_price += item_total

            order.total_price = total_price
            order.save(update_fields=["total_price"])
            cart.items.all().delete()


        order_id = order.id
        order= Order.objects.prefetch_related("items__product_variant__product").get(pk=order_id)




        return order

    @staticmethod
    def cancel(order_id , user = None , allowed_transitions = (Order.PENDING ,)):
        with transaction.atomic():

          qs = Order.objects.select_for_update()
          if user is not None:
              qs = qs.filter(user=user)

        try:
            order = qs.get(pk=order_id)
        except Order.DoesNotExist:
            raise CustomNotFound()

        if order.status not in allowed_transitions:
            raise UpdateOrderStatusException(
                current_status=order.status,
                requested_status=Order.CANCELLED,
            )

        items = order.items.select_related("product_variant").select_for_update(of=("product_variant",)).order_by("product_variant__id")
        for item in items:
                order_item_quantity = item.quantity
                variant = item.product_variant
                variant.quantity += order_item_quantity
                variant.save(update_fields=["quantity"])


        order.status = Order.CANCELLED
        order.save(update_fields=["status"])
        return order


