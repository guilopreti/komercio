from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import CustomUserManager


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(
        unique=True, error_messages={"unique": "Email already exists."}
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField()

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()
