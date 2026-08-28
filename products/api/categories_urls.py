from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryAPIView.as_view(), ),
    path('<int:id>', views.CategoryAPIView.as_view(), ),

]