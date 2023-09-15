from unittest import mock
from unittest.mock import call

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from application.tests.factories import ScriptFactory, GroupFactory, DeviceFactory


class PostRunScriptTest(APITestCase):
    @classmethod
    def setUp(cls):
        cls.test_script = ScriptFactory()
        cls.test_device1 = DeviceFactory()
        cls.test_device2 = DeviceFactory()
        cls.test_group1 = GroupFactory(devices=[cls.test_device1, cls.test_device2])
        cls.test_group2 = GroupFactory(devices=[])

    @mock.patch("application.api.views.run_script.run_script_on_device")
    def test_group_with_devices(self, task_mock):
        url = reverse("run_script")
        data = {
            "group": self.test_group1.id,
            "script": self.test_script.id,
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        calls = [
            call.delay(
                group=self.test_group1.id,
                device=self.test_device1.id,
                script=self.test_script.id,
            ),
            call.delay(
                group=self.test_group1.id,
                device=self.test_device2.id,
                script=self.test_script.id,
            ),
        ]
        task_mock.assert_has_calls(calls)
        task_mock.assert_not_called()

    @mock.patch("application.api.views.run_script.run_script_on_device")
    def test_group_without_devices(self, task_mock):
        url = reverse("run_script")
        data = {
            "group": self.test_group2.id,
            "script": self.test_script.id,
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        task_mock.assert_not_called()
        task_mock.delay.assert_not_called()

    @mock.patch("application.api.views.run_script.run_script_on_device")
    def test_group_not_exists(self, task_mock):
        url = reverse("run_script")
        data = {
            "group": max(self.test_group1.id, self.test_group2.id) + 1,
            "script": self.test_script.id,
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        task_mock.assert_not_called()
        task_mock.delay.assert_not_called()

    @mock.patch("application.api.views.run_script.run_script_on_device")
    def test_script_not_exists(self, task_mock):
        url = reverse("run_script")
        data = {
            "group": self.test_group2.id,
            "script": self.test_script.id + 1,
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        task_mock.assert_not_called()
        task_mock.delay.assert_not_called()
