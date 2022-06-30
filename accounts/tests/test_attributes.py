from accounts.models import User
from django.db import IntegrityError
from django.test import TestCase


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "gui@mail.com"
        cls.first_name = "Guilherme"
        cls.last_name = "Silva"
        cls.is_seller = False

        cls.user = User.objects.create(
            email=cls.email,
            password="123456",
            first_name=cls.first_name,
            last_name=cls.last_name,
            is_seller=cls.is_seller,
        )

    def test_email_unique(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email=self.email,
                password="123456",
                first_name=self.first_name,
                last_name=self.last_name,
                is_seller=self.is_seller,
            )

    def test_first_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 50)

    def test_last_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 50)

    def test_user_fields_values(self):
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.last_name, self.last_name)
        self.assertEqual(self.user.is_seller, self.is_seller)
