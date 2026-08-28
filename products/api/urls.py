from django.urls import path
from . import  views
urlpatterns = [
    path('', views.ProductAPIView.as_view(), ),
    path('<int:id>', views.ProductAPIView.as_view(), ),

]