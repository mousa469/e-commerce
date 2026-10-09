from django.db.models.aggregates import Count
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.views import  CrudAPIView
from products.api.filters import ProductFilter
from products.api.serializers import CategorySerializer, ProductSerializer, ProductVariantSerializer, \
    ReadProductDetailsSerializer, CreateDiscountSerializer, DiscountDetailsSerializer
from products.models import Category, Product, ProductVariants, Discount
from core.permissions import IsAdmin
from core.exceptions import CustomNotFound
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg, Prefetch
from django.utils import timezone

from ..admin import ProductVariant


class CategoryAPIView(CrudAPIView):
    model = Category
    basic_serializer = CategorySerializer
    http_method_names = ['post' , 'get' , 'delete' , 'patch']
    read_kwargs = {"is_available": True}
    permission_classes = [IsAdmin]


class ProductAPIView(CrudAPIView):
    model = Product
    read_detail_serializer = ReadProductDetailsSerializer
    read_serializer = ProductSerializer
    basic_serializer = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['post' , 'get', 'delete' ,'patch']
    read_kwargs = {"is_available": True , "category__is_available": True}
    permission_classes = [IsAdmin]
    filter = ProductFilter
    paginator = PageNumberPagination
    page_size = 10



    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(rate=Avg("reviews__rate"))

        now = timezone.now()
        active_discounts = Discount.objects.filter(
            is_available=True, start_date__lte=now, end_date__gte=now
        )
        queryset = queryset.prefetch_related(
            Prefetch("discounts", queryset=active_discounts, to_attr="active_discounts"),
        )
        return queryset



    def get_object(self, id):
        try:
            now = timezone.now()
            active_discounts = Discount.objects.filter(
                is_available=True, start_date__lte=now, end_date__gte=now
            )
            queryset = (Product.objects
                        .select_related("category")
                        .annotate(rate=Avg("reviews__rate"), reviews_count=Count("reviews"))
                        .prefetch_related(
                Prefetch("discounts", queryset=active_discounts , to_attr="active_discounts")
            )
                        .get(pk=id))


            return queryset
        except Product.DoesNotExist:
            raise CustomNotFound()





    def perform_update(self, is_Partial, object):

        if not object.is_available:
            raise CustomNotFound()

        return super().perform_update(is_Partial, object)
class ProductVariantAPIView(CrudAPIView):
    model = ProductVariants
    read_serializer = ProductVariantSerializer
    basic_serializer = ProductVariantSerializer
    parser_classes = [MultiPartParser , FormParser]
    http_method_names = ['post' , "get" , 'delete' ,"patch"]
    read_kwargs = {"is_available": True}
    permission_classes = [IsAdmin]

    def perform_update(self, is_Partial, object):

        if not object.is_available:
            raise CustomNotFound()

        return super().perform_update(is_Partial, object)

class DiscountsAPIView(CrudAPIView):
    model = Discount
    basic_serializer = CreateDiscountSerializer
    read_serializer = DiscountDetailsSerializer
    http_method_names = ['post' , 'patch', 'get']
    permission_classes = [ IsAuthenticated , IsAdmin ]
    update_serializer = CreateDiscountSerializer
    def get_permissions(self):
        return [perm() for perm in self.permission_classes]


class ProductDiscountsAPIView(APIView):
    permission_classes = [ IsAuthenticated ,IsAdmin]
    http_method_names = ['get']

    def get(self , request , id):
        try:
            product = Product.objects.get(pk = id)
        except Product.DoesNotExist :
            raise CustomNotFound()

        discounts = product.discounts.all()
        serializer = DiscountDetailsSerializer(discounts, many=True)
        return Response(serializer.data)











