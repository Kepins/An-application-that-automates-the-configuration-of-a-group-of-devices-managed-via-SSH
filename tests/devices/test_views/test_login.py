from rest_framework.test import APIClient, APITestCase


from django.urls import reverse

from tests.factory import UserFactory
#user poprawnie zalogowany

#user z blednym haslem

#user z blednym loginem


class TestLoginUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "test_pass"
        cls.test_user = UserFactory()
        cls.client = APIClient()
        cls.url = "/api-token-auth/"

    def test_login_user_200(self):
        data = {"username": self.test_user.username, "password": self.password}

        response = self.client.post(self.url, data=data, format="json")

        self.assertEqual(200, response.status_code)
        #assert contain tokens

    def test_login_user_wrong_username_400(self):
        data = {"username": "wrong_username",  "password": self.password}

        response = self.client.post(reverse(self.url), data=data, format="json")

        self.assertEqual(400, response.status_code)
        # assert text error

    def test_login_user_wrong_password_400(self):
        data = {"username": self.test_user.username,  "password": "wrong_password"}

        response = self.client.post(reverse(self.url), data=data, format="json")

        self.assertEqual(400, response.status_code)
        # assert text error




