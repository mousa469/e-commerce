from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.views import CrudAPIView
from core.permissions import IsClient , ReviewOwner
from products.models import Product
from .serializers import ReviewSerializer , UpdateReviewSerializer
from ..models import Review
from  .filters import ReviewFilter
from rest_framework.pagination import PageNumberPagination




class ReviewAPIView(CrudAPIView):
    model = Review
    basic_serializer = ReviewSerializer
    http_method_names = ['post','delete' , 'get' , 'patch']
    permission_classes = [ReviewOwner]
    update_serializer = UpdateReviewSerializer
    read_serializer = ReviewSerializer


    def get_queryset(self):
        return Review.objects.select_related("user")




class ProductReviewAPIView(CrudAPIView):
    model = Product
    basic_serializer = ReviewSerializer
    http_method_names = ['get']



    def get(self,request,*args, **kwargs):
        product = self.get_object(id= kwargs['id'])
        reviews = Review.objects.filter(product=product)
        reviews =  ReviewFilter(request.GET, queryset=reviews).qs
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(reviews, request)
        serializer = self.basic_serializer(page, many=True)
        return Response(serializer.data)


