from django.urls import path
from  . import  views





urlpatterns = [
    path('', views.DiscountsAPIView.as_view()),
    path('<int:id>' , views.DiscountsAPIView.as_view()),
]