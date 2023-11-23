import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from application.tests.factories import (
    setup_test_environment,
    DeviceFactory,
    KeyPairFactory,
    UserFactory,
)


def assert_device_matches_json(test_case, device, device_json):
    test_case.assertEquals(device_json["id"], device.id)
    test_case.assertEquals(device_json["name"], device.name)
    test_case.assertEquals(device_json["username"], device.username)
    test_case.assertEquals(device_json["hostname"], device.hostname)
    if device.key_pair:
        test_case.assertEquals(device_json["key_pair"], device.key_pair.id)
    else:
        test_case.assertEquals(device_json["key_pair"], None)
    if device.password:
        test_case.assertEquals(device_json["is_password_set"], True)
    else:
        test_case.assertEquals(device_json["is_password_set"], False)


class GetDeviceListTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_authenticated(self):
        resp = self.client.get(
            "/api/devices/",
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get(
            "/api/devices/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 0)

    def test_one(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory()
        device.save()

        resp = self.client.get(
            "/api/devices/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 1)
        assert_device_matches_json(self, device, resp.json()[0])

    def test_many(self):
        self.client.force_authenticate(self.user)
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


class PostDeviceListTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.key_content = "ssh-rsa AABBB3NzaC1yc2EAAAADAQABAAACAQDz+uXxmJnI0vHe9ym2yBSuoOkhStNg4cN2P7gGUD7TFe7KmpAsvS5l7YLcLfdpNSP5oJKdBpoCvn3WCA3xVCg/tZlxMcDfDRnhPEwtLqKEysSe5Djp62nxWzV39AphZcytfZSB3BejhddPWoqH39tkYY7Qk3wa/KBPFVXGghK0bII2yjIQlOrJWWHsa/rC6+7gVq2skPuGlxHeWP4th2twgrBJhql+cw0m71ynx2zdXnZSDD9kG/JcJc2DeB1dD1RTckK/wmghxlsfRJxvB59RJehrKJNwe94n6EGcRLkASzWt/cSmJib0gbhRIoPnU0HELNtqyv0mSuFiz2IF1yeWrd53ufb9+ZiYeJfM99+vIf2nShODat3QeK1OVsMEpz+VGkTPyQcxRUJMQhFG2JBLXpsrNxYnTjXZqjmEDglm44M/YVNEYxyYodGqNgaOlx6v/seNg/swr2Yn9u0f75k90xTIuwnHGjPVjpBvH6f4UXQyOWCtTshyXFRDdsOsXD90EhEuec/+CMjbREGf0v8wp7PxYVOBhPddXQH+RW5YEA1te/ZjPVdTt0P0MhuSLOzQuTZcDISuS2iCSx+nk0QjSh50iHWBafZBva6fvT+6oFtwMYPeFdna5OeMSQ960eS2VIxIIjs34A2aT7YrQwo42JtBIWH8por3SAjwazxm2Q== user@example.com"
        self.user = UserFactory()
        self.client = APIClient()

    def test_key_pair_empty(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory.build()
        device.key_pair = None

        resp = self.client.post(
            "/api/devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": device.name,
                    "hostname": device.hostname,
                    "username": device.username,
                    "key_pair": None,
                    "port": device.port,
                    "password": device.password,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        device.id = resp.json()["id"]
        assert_device_matches_json(self, device, resp.json())

    def test_key_pair_doesnt_exist(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory.build()

        resp = self.client.post(
            "/api/devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": device.name,
                    "hostname": device.hostname,
                    "key_pair": 1,
                    "port": device.port,
                    "password": device.password,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_key_pair_exists(self):
        self.client.force_authenticate(self.user)
        key_pair = KeyPairFactory()
        key_pair.save()
        device = DeviceFactory.build(key_pair=key_pair)

        resp = self.client.post(
            "/api/devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": device.name,
                    "hostname": device.hostname,
                    "username": device.username,
                    "key_pair": key_pair.id,
                    "port": device.port,
                    "password": device.password,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        device.id = resp.json()["id"]
        assert_device_matches_json(self, device, resp.json())

    def test_not_authenticated(self):
        device = DeviceFactory.build()

        resp = self.client.post(
            "/api/devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": device.name,
                    "hostname": device.hostname,
                    "key_pair": 1,
                    "port": device.port,
                    "password": device.password,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class GetDeviceDetailTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_exists(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get(
            "/api/devices/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_exists(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory()
        device.save()

        resp = self.client.get(
            f"/api/devices/{device.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        assert_device_matches_json(self, device, resp.json())

    def test_exists_with_key_pair(self):
        self.client.force_authenticate(self.user)
        key_pair = KeyPairFactory()
        key_pair.save()
        device = DeviceFactory(key_pair=key_pair)
        device.save()

        resp = self.client.get(
            f"/api/devices/{device.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        assert_device_matches_json(self, device, resp.json())

    def test_not_authenticated(self):
        device = DeviceFactory()
        device.save()
        resp = self.client.get(
            f"/api/devices/{device.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PutDeviceDetailTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_exists(self):
        self.client.force_authenticate(self.user)
        resp = self.client.put(
            "/api/devices/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_all_fields(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory()
        device.save()
        new_device = DeviceFactory.build(port=2222)

        resp = self.client.put(
            f"/api/devices/{device.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_device.name,
                    "hostname": new_device.hostname,
                    "username": device.username,
                    "key_pair": new_device.key_pair.id,
                    "port": new_device.port,
                    "password": new_device.password,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        new_device.id = resp.json()["id"]
        assert_device_matches_json(self, new_device, resp.json())

    def test_null_key_pair(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory()
        device.save()
        new_device = DeviceFactory.build(key_pair=None, port=2222)

        resp = self.client.put(
            f"/api/devices/{device.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_device.name,
                    "hostname": new_device.hostname,
                    "username": device.username,
                    "key_pair": None,
                    "port": new_device.port,
                    "password": new_device.password,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        new_device.id = resp.json()["id"]
        assert_device_matches_json(self, new_device, resp.json())

    def test_not_all_fields(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory()
        device.save()
        new_device = DeviceFactory.build(key_pair=None, port=2222)

        resp = self.client.put(
            f"/api/devices/{device.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_device.name,
                    "hostname": new_device.hostname,
                    "port": new_device.port,
                    "password": new_device.password,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_authenticated(self):
        device = DeviceFactory()
        device.save()
        new_device = DeviceFactory.build(port=2222)

        resp = self.client.put(
            f"/api/devices/{device.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_device.name,
                    "hostname": new_device.hostname,
                    "username": device.username,
                    "key_pair": new_device.key_pair.id,
                    "port": new_device.port,
                    "password": new_device.password,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PatchDeviceDetailTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_exists(self):
        self.client.force_authenticate(self.user)
        resp = self.client.patch(
            "/api/devices/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_all_fields(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory()
        device.save()
        new_device = DeviceFactory.build(port=2222)

        resp = self.client.patch(
            f"/api/devices/{device.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_device.name,
                    "hostname": new_device.hostname,
                    "key_pair": new_device.key_pair.id,
                    "port": new_device.port,
                    "password": new_device.password,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        new_device.id = resp.json()["id"]
        assert_device_matches_json(self, new_device, resp.json())

    def test_null_key_pair(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory()
        device.save()
        device.key_pair = None

        resp = self.client.patch(
            f"/api/devices/{device.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "key_pair": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        device.id = resp.json()["id"]
        assert_device_matches_json(self, device, resp.json())

    def test_two_field(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory()
        device.save()
        device.name = "changed_name"
        device.port = 2222

        resp = self.client.patch(
            f"/api/devices/{device.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": device.name,
                    "port": 2222,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        device.id = resp.json()["id"]
        assert_device_matches_json(self, device, resp.json())

    def test_not_authenticated(self):
        device = DeviceFactory()
        device.save()
        device.key_pair = None

        resp = self.client.patch(
            f"/api/devices/{device.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "key_pair": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteDeviceDetailTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_exists(self):
        self.client.force_authenticate(self.user)
        resp = self.client.delete(
            "/api/devices/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_exists(self):
        self.client.force_authenticate(self.user)
        device = DeviceFactory()
        device.save()

        resp = self.client.delete(
            f"/api/devices/{device.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_authenticated(self):
        device = DeviceFactory()
        device.save()

        resp = self.client.delete(
            f"/api/devices/{device.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)
