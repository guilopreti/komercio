from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(
        self, email, is_seller, password, is_staff, is_superuser, **extra_fields
    ):
        now = timezone.now()

        if not email:
            raise ValueError("The given email must be set")

        if is_seller != False and is_seller != True:
            raise ValueError("The is_seller atribute must be set")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            is_seller=is_seller,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, is_seller, password=None, **extra_fields):
        return self._create_user(
            email, is_seller, password, True, False, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, False, password, True, True, **extra_fields)
