from django.urls import path
from  . import views



urlpatterns = [
    path("items" , views.CartAPIView.as_view() ),
    path("items/<int:id>", views.CartAPIView.as_view()),
    path("items/<int:id>/increment",views.IncrementCartItemQuantity.as_view()),
    path("items/<int:id>/decrement",views.DecrementCartItemQuantity.as_view()),

]