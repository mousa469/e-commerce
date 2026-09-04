from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from core.views import  CrudAPIView
from products.api.filters import ProductFilter
from products.api.serializers import CategorySerializer, ProductSerializer, ProductVariantSerializer  ,ReadProductDetailsSerializer
from products.models import Category, Product , ProductVariants
from core.permissions import IsAdmin
from core.exceptions import CustomNotFound
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg




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
        return queryset

    def get_object(self, id):
        try:
            return Product.objects.annotate(rate=Avg("reviews__rate")).get(pk=id)
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






