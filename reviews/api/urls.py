from django.urls import path

from . import views

urlpatterns = [
    path('', views.ReviewAPIView.as_view()),
    path('<int:id>', views.ReviewAPIView.as_view()),

]