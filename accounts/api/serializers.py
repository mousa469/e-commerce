from rest_framework import serializers
from .services import password_validator, name_validator
from ..models import User


class CreateRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(validators=[name_validator])
    last_name = serializers.CharField(validators=[name_validator])
    email = serializers.EmailField()
    password = serializers.CharField(validators=[password_validator], write_only=True)

    def create(self, validated_data):
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        email = validated_data["email"]
        password = validated_data["password"]

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value


