from django.urls import path
from . import views


urlpatterns = [
    path('' , views.OrderAPIView.as_view()),
    path('<int:id>', views.OrderAPIView.as_view()),
    path('<int:id>/cancel', views.CancelOrderAPIView.as_view()),
    path('<int:id>/status', views.UpdateOrderStatysAPIView.as_view()),

]