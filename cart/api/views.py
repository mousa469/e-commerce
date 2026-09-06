from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from cart.api.serializers import CreateCartItemSerializer, CartItemSerializer, UpdateCartItemSerializer
from cart.models import Cart ,CartItem
from core.exceptions import CustomValidationError, CustomNotFound
from core.permissions import IsCartOwner
from core.views import CrudAPIView
from rest_framework.response import Response
from core.services import CartServices







class CartAPIView(CrudAPIView):
    model = CartItem
    create_serializer = CreateCartItemSerializer
    basic_serializer = CartItemSerializer
    read_serializer = CartItemSerializer
    update_serializer = UpdateCartItemSerializer
    http_method_names = ['post' , 'get' , 'delete' , 'patch']
    permission_classes = [IsCartOwner]



    def post(self, request, *args, **kwargs):
        serializer = CreateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = CartServices.add_item(user= request.user, validated_data=serializer.validated_data)
        serializer = CartItemSerializer(item)
        return  Response(serializer.data, status=status.HTTP_201_CREATED)




    def get_read_kwargs(self):
        return {'cart__user': self.request.user.id}

    def get_queryset(self):
        return CartItem.objects.select_related('product_variant').filter(**self.get_read_kwargs())
