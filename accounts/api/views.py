from rest_framework.views import APIView
from core.views import CrudAPIView
from .serializers import CreateRegistrationSerializer
from rest_framework.permissions import AllowAny
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status


class UserRegistration(CrudAPIView):
    model = User
    http_method_names = ["post"]
    create_serializer = CreateRegistrationSerializer

    def get_permissions(self):
        return [AllowAny()]

    def post(self, request):
        super().post(request)
        return Response(
            {"status_code": 201, "message": "Registration successful. Please log in."},
            status.HTTP_201_CREATED,
        )



