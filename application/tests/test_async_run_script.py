import json
import uuid
from unittest import mock
from unittest.mock import call

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse

from application.tests.factories import (
    ScriptFactory,
    GroupFactory,
    DeviceFactory,
    UserFactory,
)


class PostAsyncRunScriptTest(APITestCase):
    @classmethod
    def setUp(cls):
        cls.test_script = ScriptFactory()
        cls.test_device1 = DeviceFactory()
        cls.test_device2 = DeviceFactory()
        cls.test_group1 = GroupFactory(devices=[cls.test_device1, cls.test_device2])
        cls.test_group2 = GroupFactory(devices=[])
        cls.user = UserFactory()
        cls.client = APIClient()

    @mock.patch("application.api.views.group.run_script_on_device")
    def test_group_with_devices(self, task_mock):
        self.client.force_authenticate(self.user)
        url = reverse("api:groups-async-run-script", args=[self.test_group1.pk])
        data = {
            "script": self.test_script.id,
        }
        response = self.client.post(url, data)
        res_content = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
        calls = [
            call.delay(
                self.test_group1.id,
                self.test_device1.id,
                self.test_script.id,
                request_uuid=uuid.UUID(res_content["request_uuid"]),
            ),
            call.delay(
                self.test_group1.id,
                self.test_device2.id,
                self.test_script.id,
                request_uuid=uuid.UUID(res_content["request_uuid"]),
            ),
        ]
        task_mock.assert_has_calls(calls)
        task_mock.assert_not_called()

    def test_not_authenticated(self):
        url = reverse("api:groups-async-run-script", args=[self.test_group1.pk])
        data = {
            "script": self.test_script.id,
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch("application.api.views.group.run_script_on_device")
    def test_group_without_devices(self, task_mock):
        self.client.force_authenticate(self.user)
        url = reverse("api:groups-async-run-script", args=[self.test_group2.pk])
        data = {
            "script": self.test_script.id,
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
        task_mock.assert_not_called()
        task_mock.delay.assert_not_called()

    @mock.patch("application.api.views.group.run_script_on_device")
    def test_group_not_exists(self, task_mock):
        self.client.force_authenticate(self.user)
        url = reverse(
            "api:groups-async-run-script",
            args=[max(self.test_group1.id, self.test_group2.id) + 1],
        )
        data = {
            "script": self.test_script.id,
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        task_mock.delay.assert_not_called()

    @mock.patch("application.api.views.group.run_script_on_device")
    def test_script_not_exists(self, task_mock):
        self.client.force_authenticate(self.user)
        url = reverse("api:groups-async-run-script", args=[self.test_group1.id])
        data = {
            "script": self.test_script.id + 1,
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        task_mock.assert_not_called()
        task_mock.delay.assert_not_called()
