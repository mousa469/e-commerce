from cart.models import Cart , CartItem
from core.exceptions import CustomNotFound


class CartServices:
    @staticmethod
    def add_item(user , validated_data):
        variant = validated_data['product_variant']
        quantity = validated_data['quantity']

        if not  variant.is_available :
            raise CustomNotFound("This product is not found ")

        cart , created = Cart.objects.get_or_create(user=user)
        item , created = CartItem.objects.get_or_create( cart = cart , product_variant=variant)
        if not created:
            item.quantity += quantity
            item.save()
            return item




