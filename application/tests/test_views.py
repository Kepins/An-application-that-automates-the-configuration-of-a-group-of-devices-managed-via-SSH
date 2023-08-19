import json

from rest_framework.test import APIClient, APITestCase

from application.tests.factory import UserFactory, ScriptFactory


class TestLoginUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "test_pass"
        cls.test_user = UserFactory(password=cls.password)
        cls.client = APIClient()
        cls.url = "/api-token-auth/"

    def test_login_user_200(self):
        data = {"username": self.test_user.username, "password": self.password}

        response = self.client.post(self.url, data=data, format="json")
        res_content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertTrue(res_content['access'])
        self.assertTrue(res_content['refresh'])

    def test_login_user_wrong_username_401(self):
        data = {"username": "wrong_username",  "password": self.password}

        response = self.client.post(self.url, data=data, format="json")

        res_content = json.loads(response.content)

        self.assertEqual(401, response.status_code)
        self.assertEqual("No active account found with the given credentials", res_content['detail'])

    def test_login_user_wrong_password_401(self):
        data = {"username": self.test_user.username,  "password": "wrong_password"}

        response = self.client.post(self.url, data=data, format="json")

        res_content = json.loads(response.content)

        self.assertEqual(401, response.status_code)
        self.assertEqual("No active account found with the given credentials", res_content['detail'])


class TestScriptApiViews(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_script = ScriptFactory()







