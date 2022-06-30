from accounts.models import User
from products.models import Product
from products.serializers import CreateProductSerializer, ListProductSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class ProductCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_seller = User.objects.create_user(
            email="gui@mail",
            password="123456",
            first_name="Guilherme",
            last_name="Silva",
            is_seller=True,
        )
        cls.token_seller = Token.objects.create(user=cls.user_seller)

        cls.user_not_seller = User.objects.create_user(
            email="lucira@mail",
            password="123456",
            first_name="Lucira",
            last_name="Silva",
            is_seller=False,
        )
        cls.token_not_seller = Token.objects.create(user=cls.user_not_seller)

    def test_seller_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_seller.key}")

        product_data = {
            "description": "Bola de basquete vazia e laranja",
            "price": 100.00,
            "quantity": 20,
        }

        response = self.client.post("/api/products/", product_data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.get(id=1).user, self.user_seller)
        self.assertEqual(
            CreateProductSerializer(instance=Product.objects.get(id=1)).data,
            response.data,
        )

    def test_not_seller_cannot_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_not_seller.key}")

        product_data = {
            "description": "Bola de basquete vazia e laranja",
            "price": 100.00,
            "quantity": 20,
        }

        response = self.client.post("/api/products/", product_data, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            {"detail": "You do not have permission to perform this action."},
            response.data,
        )

    def test_incorrect_create_product_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_seller.key}")

        incorrect_data = {"description": "", "price": False, "quantity": 0}

        serializer = CreateProductSerializer(data=incorrect_data)

        self.assertEqual(serializer.is_valid(), False)

        response = self.client.post("/api/products/", incorrect_data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(serializer._errors, response.data)


class ProductListsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_seller = User.objects.create_user(
            email="gui@mail",
            password="123456",
            first_name="Guilherme",
            last_name="Silva",
            is_seller=True,
        )

        cls.products = []
        for _ in range(1, 6):
            product = Product.objects.create(
                description="Bola de basquete vazia e laranja",
                price=100.00,
                quantity=20,
                user=cls.user_seller,
            )
            cls.products.append(product)

    def test_anyone_can_list_products(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.products))
        self.assertEqual(
            ListProductSerializer(self.products, many=True).data, response.data
        )

    def test_anyone_can_filter_a_product(self):
        response = self.client.get(f"/api/products/{self.products[0].id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            ListProductSerializer(instance=self.products[0]).data, response.data
        )


class ProductUpdateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_seller = User.objects.create_user(
            email="gui@mail",
            password="123456",
            first_name="Guilherme",
            last_name="Silva",
            is_seller=True,
        )
        cls.token_seller = Token.objects.create(user=cls.user_seller)

        cls.user_not_seller = User.objects.create_user(
            email="lucira@mail",
            password="123456",
            first_name="Lucira",
            last_name="Silva",
            is_seller=False,
        )
        cls.token_not_seller = Token.objects.create(user=cls.user_not_seller)

        cls.product = Product.objects.create(
            description="Bola de basquete vazia e laranja",
            price=100.00,
            quantity=20,
            user=cls.user_seller,
        )

    def test_owner_can_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_seller.key}")

        update_data = {
            "description": "Bola de basquete vermelha autografada por Michael Jordan",
            "price": 2500.00,
        }

        response = self.client.patch(
            f"/api/products/{self.product.id}/", update_data, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["description"],
            "Bola de basquete vermelha autografada por Michael Jordan",
        )
        self.assertEqual(response.json()["price"], "2500.00")
        self.assertEqual(
            CreateProductSerializer(
                instance=Product.objects.get(id=self.product.id)
            ).data,
            response.data,
        )

    def test_not_owner_cannot_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_not_seller.key}")

        update_data = {
            "description": "Bola de basquete vermelha autografada por Michael Jordan",
            "price": 2500.00,
        }

        response = self.client.patch(
            f"/api/products/{self.product.id}/", update_data, format="json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            {"detail": "You do not have permission to perform this action."},
            response.data,
        )
