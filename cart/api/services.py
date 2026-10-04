from cart.models import Cart , CartItem
from core.exceptions import CustomNotFound , CustomValidationError


class CartServices:
    @staticmethod
    def add_item(user , validated_data):
        variant = validated_data['product_variant']
        quantity = validated_data['quantity']

        cart , created = Cart.objects.get_or_create(user=user)
        item , created = CartItem.objects.get_or_create( cart = cart , product_variant=variant)
        if not created:
            if quantity + item.quantity > variant.quantity:
                raise CustomValidationError(f"Requested quantity exceeds available stock. Only {variant.quantity} items are available.")
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return item


    @staticmethod
    def increment_item_quantity( cart_item , variant ):
        if cart_item.quantity + 1 > variant.quantity:
            raise CustomValidationError(
                f"Requested quantity exceeds available stock. Only {variant.quantity} items are available.")
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
        return cart_item

    @staticmethod
    def check_if_cart_item_exists(id , user):
        try:
             cart_item = CartItem.objects.select_for_update().select_related("product_variant").get(id=id , cart__user=user)
             return cart_item
        except CartItem.DoesNotExist:
            raise CustomNotFound()


    @staticmethod
    def decrement_item_quantity( cart_item , variant ):
        if cart_item.quantity  <= 1 :
            raise CustomValidationError("Minimum quantity is 1. Remove the item from your cart instead.")
        cart_item.quantity -= 1
        cart_item.save()
        return cart_item



