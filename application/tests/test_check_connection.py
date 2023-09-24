import uuid
from unittest import mock
from unittest.mock import call

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse

from application.tests.factories import (
    GroupFactory,
    DeviceFactory,
    UserFactory,
)


class PostAsyncCheckConnectionTest(APITestCase):
    @classmethod
    def setUp(cls):
        cls.test_device1 = DeviceFactory()
        cls.test_device2 = DeviceFactory()
        cls.test_group1 = GroupFactory(devices=[cls.test_device1, cls.test_device2])
        cls.test_group2 = GroupFactory(devices=[])
        cls.user = UserFactory()
        cls.client = APIClient()

    @mock.patch("application.api.views.group.check_connection_task")
    def test_group_with_devices(self, task_mock):
        self.client.force_authenticate(self.user)
        url = reverse("api:groups-async-check-connection", args=[self.test_group1.pk])
        response = self.client.post(url)
        res_content = response.json()
        self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
        calls = [
            call(
                self.test_group1.id,
                self.test_device1.id,
                request_uuid=uuid.UUID(res_content["request_uuid"]),
            ),
            call(
                self.test_group1.id,
                self.test_device2.id,
                request_uuid=uuid.UUID(res_content["request_uuid"]),
            ),
        ]
        task_mock.delay.assert_has_calls(calls)
        task_mock.assert_not_called()

    def test_not_authenticated(self):
        url = reverse("api:groups-async-check-connection", args=[self.test_group1.pk])
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch("application.api.views.group.check_connection_task")
    def test_group_without_devices(self, task_mock):
        self.client.force_authenticate(self.user)
        url = reverse("api:groups-async-check-connection", args=[self.test_group2.pk])
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
        task_mock.assert_not_called()
        task_mock.delay.assert_not_called()

    @mock.patch("application.api.views.group.check_connection_task")
    def test_group_not_exists(self, task_mock):
        self.client.force_authenticate(self.user)
        url = reverse(
            "api:groups-async-check-connection",
            args=[max(self.test_group1.id, self.test_group2.id) + 1],
        )
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        task_mock.assert_not_called()
        task_mock.delay.assert_not_called()
