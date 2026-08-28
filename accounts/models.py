from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from django.contrib.auth.base_user import BaseUserManager
from core.constants import USER_ROLES , CLIENT_ROLE

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = None
    role = models.CharField(choices=USER_ROLES ,default=CLIENT_ROLE, max_length=20)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
