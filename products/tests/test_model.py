from accounts.models import User
from django.test import TestCase
from products.models import Product
from products.serializers import CreateProductSerializer
from rest_framework.exceptions import ValidationError


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.description = """Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua."""
        cls.price = 99.99
        cls.quantity = 5

        cls.user = User.objects.create_user(
            email="gui@mail",
            password="123456",
            first_name="Guilherme",
            last_name="Silva",
            is_seller=True,
        )

    def test_price_max_digits_and_decimal_places(self):
        product = Product.objects.create(
            description=self.description,
            price=self.price,
            quantity=self.quantity,
            user=self.user,
        )

        max_digits = product._meta.get_field("price").max_digits
        decimal_places = product._meta.get_field("price").decimal_places

        self.assertEqual(max_digits, 12)
        self.assertEqual(decimal_places, 2)

    def test_quantity_not_positive_value_error(self):
        with self.assertRaises(ValidationError):
            serializer = CreateProductSerializer(
                data={
                    "description": self.description,
                    "price": self.price,
                    "quantity": 0,
                    "user": self.user,
                }
            )
            serializer.is_valid(raise_exception=True)

    def test_product_fields_values(self):
        product = Product.objects.create(
            description=self.description,
            price=self.price,
            quantity=self.quantity,
            user=self.user,
        )

        self.assertEqual(product.description, self.description)
        self.assertEqual(product.price, self.price)
        self.assertEqual(product.quantity, self.quantity)
        self.assertEqual(product.is_active, True)
        self.assertEqual(product.user, self.user)

    def test_user_may_contain_multiple_products(self):
        products = []
        for _ in range(20):
            new_product = Product.objects.create(
                description=self.description,
                price=self.price,
                quantity=self.quantity,
                user=self.user,
            )
            products.append(new_product)

        self.assertEqual(len(products), self.user.products.count())

        for product in products:
            self.assertIs(product.user, self.user)

    def test_product_cannot_belong_to_more_than_one_user(self):
        products = []
        for _ in range(20):
            new_product = Product.objects.create(
                description=self.description,
                price=self.price,
                quantity=self.quantity,
                user=self.user,
            )
            products.append(new_product)

        user_two = User.objects.create_user(
            email="lucira@mail",
            password="123456",
            first_name="Lucira",
            last_name="Silva",
            is_seller=True,
        )

        for product in products:
            product.user = user_two
            product.save()

        for product in products:
            self.assertNotIn(product, self.user.products.all())
            self.assertIn(product, user_two.products.all())
