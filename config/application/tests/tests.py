from django.test import TestCase
from rest_framework import status

from config.application.tests.factories import setup_test_environment, DeviceFactory


def assert_device_matches_json(test_case, device, device_json):
    test_case.assertEquals(device_json["id"], device.id)
    test_case.assertEquals(device_json["name"], device.name)
    test_case.assertEquals(device_json["hostname"], device.hostname)
    if device.public_key:
        test_case.assertEquals(
            device_json["key_content"], device.public_key.key_content
        )
    else:
        test_case.assertEquals(device_json["key_content"], None)


class GetDeviceListTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_empty(self):
        resp = self.client.get(
            "/api/devices/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 0)

    def test_one(self):
        device = DeviceFactory()
        device.save()

        resp = self.client.get(
            "/api/devices/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 1)
        assert_device_matches_json(self, device, resp.json()[0])

    def test_many(self):
        NUM_DEVICES = 10
        devices = []

        for _ in range(NUM_DEVICES):
            device = DeviceFactory()
            device.save()
            devices.append(device)

        resp = self.client.get(
            "/api/devices/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), NUM_DEVICES)
        for i in range(NUM_DEVICES):
            assert_device_matches_json(self, devices[i], resp.json()[i])
