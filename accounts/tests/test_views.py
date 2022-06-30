from accounts.models import User
from accounts.serializers import ChangeActiveSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserCreateViewTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "gui@mail.com",
            "password": "123456",
            "first_name": "Guilherme",
            "last_name": "Silva",
        }

    def test_create_seller_user(self):
        self.user_data["is_seller"] = True
        response = self.client.post("/api/accounts/", self.user_data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["is_seller"], True)
        self.assertEqual(
            UserSerializer(instance=User.objects.get(id=1)).data, response.data
        )

    def test_create_not_seller_user(self):
        self.user_data["is_seller"] = False
        response = self.client.post("/api/accounts/", self.user_data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["is_seller"], False)
        self.assertEqual(
            UserSerializer(instance=User.objects.get(id=1)).data, response.data
        )

    def test_incorrect_create_user_fields(self):
        self.user_data["is_seller"] = False
        User.objects.create_user(**self.user_data)

        incorrect_data = {
            "email": "gui@mail.com",
            "password": False,
            "first_name": "",
            "last_name": "CincoCincoCincoCincoCincoCincoCincoCincoCincoCinco1",
            "is_seller": "banana",
        }

        serializer = UserSerializer(data=incorrect_data)

        self.assertEqual(serializer.is_valid(), False)

        response = self.client.post("/api/accounts/", incorrect_data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(serializer._errors, response.data)


class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "123456"
        cls.user_one = User.objects.create_user(
            email="gui@mail.com",
            password=cls.password,
            first_name="Guilherme",
            last_name="Silva",
            is_seller=True,
        )
        cls.token_one = Token.objects.create(user=cls.user_one)

        cls.user_two = User.objects.create_user(
            email="lucira@mail.com",
            password=cls.password,
            first_name="Lucira",
            last_name="Silva",
            is_seller=False,
        )
        cls.token_two = Token.objects.create(user=cls.user_two)

    def test_login_seller_user(self):

        login_data = {"email": self.user_one.email, "password": self.password}

        response = self.client.post("/api/login/", login_data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual({"token": self.token_one.key}, response.data)

    def test_login_not_seller_user(self):

        login_data = {"email": self.user_two.email, "password": self.password}

        response = self.client.post("/api/login/", login_data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual({"token": self.token_two.key}, response.data)


class UserUpdateListViewsTest(APITestCase):
    @classmethod
    def setUp(cls):
        cls.user_one = User.objects.create_user(
            email="gui@mail.com",
            password="123456",
            first_name="Guilherme",
            last_name="Silva",
            is_seller=True,
        )
        cls.token_one = Token.objects.create(user=cls.user_one)

        cls.super_user = User.objects.create_superuser(
            email="Lucira@mail.com",
            password="123456",
            first_name="Lucira",
            last_name="Silva",
        )
        cls.token_super = Token.objects.create(user=cls.super_user)

        cls.users = [cls.user_one, cls.super_user]

    def test_update_account_owner(self):
        update_data = {"last_name": "Lopreti"}

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_one.key}")

        response = self.client.patch(
            f"/api/accounts/{self.user_one.id}/", update_data, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["last_name"], "Lopreti")
        self.assertEqual(
            UserSerializer(instance=User.objects.get(id=self.user_one.id)).data,
            response.data,
        )

    def test_user_not_owner_cannot_update_another_account(self):
        update_data = {"last_name": "Lopreti"}

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_super.key}")

        response = self.client.patch(
            f"/api/accounts/{self.user_one.id}/", update_data, format="json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            {"detail": "You do not have permission to perform this action."},
            response.data,
        )

    def test_adm_user_can_deactivate_account(self):
        update_data = {"is_active": False}

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_super.key}")

        response = self.client.patch(
            f"/api/accounts/{self.user_one.id}/management/", update_data, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_active"], False)
        self.assertEqual(
            ChangeActiveSerializer(instance=User.objects.get(id=self.user_one.id)).data,
            response.data,
        )

    def test_not_adm_user_cannot_deactivate_account(self):
        update_data = {"is_active": False}

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_one.key}")

        response = self.client.patch(
            f"/api/accounts/{self.user_one.id}/management/", update_data, format="json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            {"detail": "You do not have permission to perform this action."},
            response.data,
        )

    def test_anyone_can_list_accounts(self):

        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            UserSerializer(self.users[0:5], many=True).data, response.data["results"]
        )
