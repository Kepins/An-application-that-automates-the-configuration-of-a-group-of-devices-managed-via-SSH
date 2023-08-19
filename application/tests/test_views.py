import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from application.models import Script
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


class ScriptListCreateAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_script_1 = ScriptFactory()
        cls.test_script_2 = ScriptFactory()

    def test_list_many(self):
        response = self.client.get(reverse('api:scripts-list'))
        res_content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        for scripts in res_content:
            self.assertTrue(scripts['id'])
            self.assertTrue(scripts['name'])
            self.assertTrue(scripts['script'])


    def test_list_one(self):
        self.test_script_1.delete()

        response = self.client.get(reverse('api:scripts-list'))
        res_content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertTrue(res_content[0]['id'])
        self.assertTrue(res_content[0]['name'])
        self.assertTrue(res_content[0]['script'])

    def test_empty_list(self):
        Script.objects.all().delete()  # Remove all scripts

        response = self.client.get(reverse('api:scripts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create(self):
        data = {
            'name': 'New Script',
            'script': 'Script content',
        }
        response = self.client.post(reverse('api:scripts-list'), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Script.objects.count(), 3)

    def test_create_validation_error(self):
        data = {
            'name': 'A very long title that exceeds the maximum character limit of 100 characters. ' * 2,
            'script': 'Script content',
        }
        response = self.client.post(reverse('api:scripts-list'), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Script.objects.count(), 2)

    def test_delete_script(self):
        script_to_delete = self.test_script_1
        url = reverse('api:scripts-detail', args=[script_to_delete.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Script.objects.filter(pk=script_to_delete.pk).exists())

    def test_delete_nonexistent_script(self):
        nonexistent_script_pk = 9999
        url = reverse('api:scripts-detail', args=[nonexistent_script_pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_script(self):
        script_to_update = self.test_script_1
        url = reverse('api:scripts-detail', args=[script_to_update.pk])
        data = {
            'name': 'Updated Title',
            'script': 'Updated Content',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        script_to_update.refresh_from_db()
        self.assertEqual(script_to_update.name, data['name'])
        self.assertEqual(script_to_update.script, data['script'])

    def test_update_nonexistent_script(self):
        nonexistent_script_pk = 9999  # A PK that does not exist
        url = reverse('api:scripts-detail', args=[nonexistent_script_pk])
        data = {
            'name': 'Updated Title',
            'script': 'Updated Content',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_validation_error(self):
        script_to_update = self.test_script_1
        url = reverse('api:scripts-detail', args=[script_to_update.pk])
        data = {
            'name': 'A very long title that exceeds the maximum character limit of 100 characters. ' * 2,
            'script': 'Updated Content',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('Ensure this field has no more than 100 characters.', response.data['name'])

    def test_retrieve_script(self):
        script_to_retrieve = self.test_script_1
        url = reverse('api:scripts-detail', args=[script_to_retrieve.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], script_to_retrieve.name)
        self.assertEqual(response.data['script'], script_to_retrieve.script)

    def test_retrieve_nonexistent_script(self):
        nonexistent_script_pk = 9999  # A PK that does not exist
        url = reverse('api:scripts-detail', args=[nonexistent_script_pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)













