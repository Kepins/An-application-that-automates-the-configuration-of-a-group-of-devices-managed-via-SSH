import json

from django.test import TestCase
from rest_framework import status

from application.tests.factories import (
    setup_test_environment,
    DeviceFactory,
    PublicKeyFactory,
)


def assert_device_matches_json(test_case, device, device_json):
    test_case.assertEquals(device_json["id"], device.id)
    test_case.assertEquals(device_json["name"], device.name)
    test_case.assertEquals(device_json["hostname"], device.hostname)
    if device.public_key:
        test_case.assertEquals(device_json["public_key"], device.public_key.id)
    else:
        test_case.assertEquals(device_json["public_key"], None)


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


class PostDeviceListTest(TestCase):
    def setUp(self):
        setup_test_environment()
        self.key_content = "ssh-rsa AABBB3NzaC1yc2EAAAADAQABAAACAQDz+uXxmJnI0vHe9ym2yBSuoOkhStNg4cN2P7gGUD7TFe7KmpAsvS5l7YLcLfdpNSP5oJKdBpoCvn3WCA3xVCg/tZlxMcDfDRnhPEwtLqKEysSe5Djp62nxWzV39AphZcytfZSB3BejhddPWoqH39tkYY7Qk3wa/KBPFVXGghK0bII2yjIQlOrJWWHsa/rC6+7gVq2skPuGlxHeWP4th2twgrBJhql+cw0m71ynx2zdXnZSDD9kG/JcJc2DeB1dD1RTckK/wmghxlsfRJxvB59RJehrKJNwe94n6EGcRLkASzWt/cSmJib0gbhRIoPnU0HELNtqyv0mSuFiz2IF1yeWrd53ufb9+ZiYeJfM99+vIf2nShODat3QeK1OVsMEpz+VGkTPyQcxRUJMQhFG2JBLXpsrNxYnTjXZqjmEDglm44M/YVNEYxyYodGqNgaOlx6v/seNg/swr2Yn9u0f75k90xTIuwnHGjPVjpBvH6f4UXQyOWCtTshyXFRDdsOsXD90EhEuec/+CMjbREGf0v8wp7PxYVOBhPddXQH+RW5YEA1te/ZjPVdTt0P0MhuSLOzQuTZcDISuS2iCSx+nk0QjSh50iHWBafZBva6fvT+6oFtwMYPeFdna5OeMSQ960eS2VIxIIjs34A2aT7YrQwo42JtBIWH8por3SAjwazxm2Q== user@example.com"

    def test_public_key_empty(self):
        device = DeviceFactory.build()
        device.public_key = None

        resp = self.client.post(
            "/api/devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": device.name,
                    "hostname": device.hostname,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        device.id = resp.json()["id"]
        assert_device_matches_json(self, device, resp.json())

    def test_public_key_doesnt_exist(self):
        device = DeviceFactory.build()

        resp = self.client.post(
            "/api/devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": device.name,
                    "hostname": device.hostname,
                    "public_key": 1,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_public_key_exists(self):
        public_key = PublicKeyFactory()
        public_key.save()
        device = DeviceFactory.build(public_key=public_key)

        resp = self.client.post(
            "/api/devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": device.name,
                    "hostname": device.hostname,
                    "public_key": public_key.id,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        device.id = resp.json()["id"]
        assert_device_matches_json(self, device, resp.json())
