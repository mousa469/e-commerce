from django.urls import path
from . import  views
from reviews.api.views import ProductReviewAPIView
urlpatterns = [
    path('', views.ProductAPIView.as_view(), ),
    path('<int:id>', views.ProductAPIView.as_view(), ),

    path('<int:id>/reviews', ProductReviewAPIView.as_view(), ),

]