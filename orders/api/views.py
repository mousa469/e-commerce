from django.db import transaction
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import CustomNotFound, CustomValidationError, UpdateOrderStatusException
from core.views import CrudAPIView
from orders.api.serializers import CreateOrderSerializer, OrderDetailsSerializer, OrderListSerializer, \
    UpdateOrderStatusSerializer
from orders.api.services import OrderService
from orders.models import Order
from core.permissions import IsClient, IsOrderOwner, IsAdmin


class OrderAPIView(CrudAPIView):
    model = Order
    http_method_names = ['post' , 'get']
    basic_serializer = OrderListSerializer
    read_detail_serializer = OrderDetailsSerializer
    permission_classes = [IsAuthenticated , IsClient ,  IsOrderOwner]

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]


    def post(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = OrderService.place(
            user=request.user,
            data=serializer.validated_data
        )
        return Response(OrderDetailsSerializer(order).data , status=status.HTTP_201_CREATED)

    def get_object(self, id):
        try:
            order = self.model.objects.prefetch_related("items__product_variant__product").get(pk=id)
            self.check_object_permissions(self.request, order)
            return order
        except self.model.DoesNotExist:
            raise CustomNotFound()

    def get_read_kwargs(self):
        return {'user': self.request.user}




class CancelOrderAPIView(APIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated , IsClient , IsOrderOwner]
    def post(self, request, id):
     order = OrderService.cancel(user=request.user , order_id=id)
     order = Order.objects.prefetch_related("items__product_variant__product").get(pk=id)
     serializer = OrderDetailsSerializer(order)
     return Response(serializer.data)



class UpdateOrderStatysAPIView(APIView):

    permission_classes = [IsAuthenticated,IsAdmin]

    def patch(self, request, id):
          serializer = UpdateOrderStatusSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          order = OrderService.update_order_status(order_id=id, new_status=serializer.validated_data['status'])
          order = Order.objects.prefetch_related("items__product_variant__product").get(pk=id)
          serializer = OrderDetailsSerializer(order)
          return Response(serializer.data)





