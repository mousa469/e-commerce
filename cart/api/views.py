from rest_framework import status
from rest_framework.views import APIView

import cart
from cart.api.serializers import CreateCartItemSerializer, CartItemSerializer, UpdateCartItemSerializer
from cart.models import Cart ,CartItem
from core.exceptions import CustomNotFound, CustomValidationError
from core.permissions import IsCartOwner , IsClient
from core.views import CrudAPIView
from rest_framework.response import Response
from  .services import CartServices
from django.db import transaction
from rest_framework.permissions import  IsAuthenticated







class CartAPIView(CrudAPIView):
    model = CartItem
    create_serializer = CreateCartItemSerializer
    basic_serializer = CartItemSerializer
    read_serializer = CartItemSerializer
    update_serializer = UpdateCartItemSerializer
    http_method_names = ['post' , 'get' , 'delete']
    permission_classes = [IsAuthenticated , IsClient ,IsCartOwner]



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


class IncrementCartItemQuantity(APIView):
    permission_classes = [IsAuthenticated ,IsClient , IsCartOwner]
    def post(self, request, id):
      with transaction.atomic():
        cart_item = CartServices.check_if_cart_item_exists(id , request.user)
        variant = cart_item.product_variant
        cart_item=  CartServices.increment_item_quantity(cart_item, variant)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)



class DecrementCartItemQuantity(APIView):
    permission_classes = [IsAuthenticated ,IsClient,IsCartOwner]
    def post(self, request, id):
        with transaction.atomic():
            cart_item = CartServices.check_if_cart_item_exists(id , request.user)
            variant = cart_item.product_variant
            cart_item = CartServices.decrement_item_quantity(cart_item, variant)
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)












