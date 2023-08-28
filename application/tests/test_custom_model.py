import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from application.models import CustomUser
from application.tests.factories import UserFactory


class TestRegisterApiView(APITestCase):
    def test_register(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "password": "NewPassword123",
            "password2": "NewPassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, "newuser")

    def test_register_existing_user(self):
        UserFactory()
        url = reverse("register")  # Use the actual URL name from your urls.py
        data = {
            "username": "existinguser",
            "password": "NewPassword123",
            "password2": "NewPassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_register_missing_fields(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "password": "NewPassword123",
            # 'password2' is missing
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)


class TestLoginUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "test_pass"
        cls.test_user = UserFactory(password=cls.password)
        cls.client = APIClient()
        cls.url = reverse("login")

    def test_login_user_200(self):
        data = {"username": self.test_user.username, "password": self.password}

        response = self.client.post(self.url, data=data, format="json")
        res_content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertTrue(res_content["access"])
        self.assertTrue(res_content["refresh"])

    def test_login_user_wrong_username_401(self):
        data = {"username": "wrong_username", "password": self.password}

        response = self.client.post(self.url, data=data, format="json")

        res_content = json.loads(response.content)

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            "No active account found with the given credentials", res_content["detail"]
        )

    def test_login_user_wrong_password_401(self):
        data = {"username": self.test_user.username, "password": "wrong_password"}

        response = self.client.post(self.url, data=data, format="json")

        res_content = json.loads(response.content)

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            "No active account found with the given credentials", res_content["detail"]
        )
