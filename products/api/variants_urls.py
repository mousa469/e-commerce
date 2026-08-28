from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductVariantAPIView.as_view(), ),
    path('<int:id>', views.ProductVariantAPIView.as_view(), ),

]