import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from application.tests.factories import (
    setup_test_environment,
    GroupFactory,
    DeviceFactory,
    UserFactory,
)


def assert_group_matches_json(test_case, group, group_json):
    test_case.assertEquals(group_json["id"], group.id)
    test_case.assertEquals(group_json["name"], group.name)
    if group.key_pair:
        test_case.assertEquals(group_json["key_pair"], group.key_pair.id)
    else:
        test_case.assertEquals(group_json["key_pair"], None)
    test_case.assertEquals(len(group.devices.all()), len(group_json["devices"]))
    for device_id in group_json["devices"]:
        test_case.assertTrue(group.devices.filter(pk=device_id).exists())


class GetGroupListTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_empty(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get(
            "/api/groups/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 0)

    def test_one(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(devices=[DeviceFactory(port=2222)])
        group.save()

        resp = self.client.get(
            "/api/groups/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 1)
        assert_group_matches_json(self, group, resp.json()[0])

    def test_many(self):
        self.client.force_authenticate(self.user)
        NUM_GROUPS = 10
        groups = []

        for _ in range(NUM_GROUPS):
            group = GroupFactory()
            group.save()
            groups.append(group)

        resp = self.client.get(
            "/api/groups/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), NUM_GROUPS)
        for i in range(NUM_GROUPS):
            assert_group_matches_json(self, groups[i], resp.json()[i])

    def test_not_authenticated(self):
        group = GroupFactory(devices=[DeviceFactory(port=2222)])
        group.save()

        resp = self.client.get(
            "/api/groups/",
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PostGroupListTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_empty_device_list(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory.build()

        resp = self.client.post(
            "/api/groups/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": group.name,
                    "key_pair": None,
                    "devices": [],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        group.id = resp.json()["id"]
        assert_group_matches_json(self, group, resp.json())

    def test_not_authenticated(self):
        group = GroupFactory.build()

        resp = self.client.post(
            "/api/groups/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": group.name,
                    "key_pair": None,
                    "devices": [],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_empty_device_list(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory.build()
        devices = [DeviceFactory(name="Device1111"), DeviceFactory(port=2222)]

        resp = self.client.post(
            "/api/groups/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": group.name,
                    "key_pair": None,
                    "devices": [device.id for device in devices],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        group.id = resp.json()["id"]
        assert_group_matches_json(self, group, resp.json())

    def test_no_device_list(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory.build()

        resp = self.client.post(
            "/api/groups/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": group.name,
                    "key_pair": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_pub_key(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory.build()

        resp = self.client.post(
            "/api/groups/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": group.name,
                    "key_pair": 1,
                    "devices": [],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)


class GetDeviceDetailTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_exists(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get(
            "/api/groups/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_exists(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory()
        group.save()

        resp = self.client.get(
            f"/api/groups/{group.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        assert_group_matches_json(self, group, resp.json())

    def test_not_authenticated(self):
        group = GroupFactory()
        group.save()

        resp = self.client.get(
            f"/api/groups/{group.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PutDeviceDetailTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_all_fields(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory()
        group.save()
        new_group = GroupFactory.build(name="NEW NAME")

        resp = self.client.put(
            f"/api/groups/{group.id}/",
            content_type="application/json",
            data=json.dumps({"name": new_group.name, "devices": []}),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_all_fields2(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory()
        group.save()
        new_group = GroupFactory.build(name="NEW NAME")

        resp = self.client.put(
            f"/api/groups/{group.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_group.name,
                    "key_pair": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_all_fields(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory()
        group.save()
        new_group = GroupFactory.build(name="NEW NAME", key_pair=None)
        devices = [DeviceFactory(name="Device1111"), DeviceFactory(port=2222)]

        resp = self.client.put(
            f"/api/groups/{group.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_group.name,
                    "key_pair": new_group.key_pair,
                    "devices": [device.id for device in devices],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        new_group.id = resp.json()["id"]
        assert_group_matches_json(self, new_group, resp.json())

    def test_not_authenticated(self):
        group = GroupFactory()
        group.save()
        new_group = GroupFactory.build(name="NEW NAME", key_pair=None)
        devices = [DeviceFactory(name="Device1111"), DeviceFactory(port=2222)]

        resp = self.client.put(
            f"/api/groups/{group.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_group.name,
                    "key_pair": new_group.key_pair,
                    "devices": [device.id for device in devices],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PatchDeviceDetailTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_all_fields(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory()
        group.save()
        new_group = GroupFactory.build(name="NEW NAME", key_pair=group.key_pair)

        resp = self.client.patch(
            f"/api/groups/{group.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_group.name,
                    "devices": [],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        new_group.id = resp.json()["id"]
        assert_group_matches_json(self, new_group, resp.json())

    def test_devices(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory()
        group.save()
        devices = [DeviceFactory(name="Device1111"), DeviceFactory(port=2222)]

        resp = self.client.patch(
            f"/api/groups/{group.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in devices],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        assert_group_matches_json(self, group, resp.json())

    def test_not_authenticated(self):
        group = GroupFactory()
        group.save()
        devices = [DeviceFactory(name="Device1111"), DeviceFactory(port=2222)]

        resp = self.client.patch(
            f"/api/groups/{group.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in devices],
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
            "/api/groups/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_exists(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory()
        group.save()

        resp = self.client.delete(
            f"/api/groups/{group.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_authenticated(self):
        group = GroupFactory()
        group.save()

        resp = self.client.delete(
            f"/api/groups/{group.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class AddDevicesGroupTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.devices = DeviceFactory.create_batch(5)
        self.user = UserFactory()
        self.client = APIClient()

    def test_add_to_empty(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory()
        group.save()

        resp = self.client.patch(
            f"/api/groups/{group.id}/add_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:3]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(group.devices.all()), 3)
        assert_group_matches_json(self, group, resp.json())

    def test_not_authenticated(self):
        group = GroupFactory()
        group.save()

        resp = self.client.patch(
            f"/api/groups/{group.id}/add_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:3]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_to_not_empty(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(devices=[self.devices[4]])
        group.save()

        resp = self.client.patch(
            f"/api/groups/{group.id}/add_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:3]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(group.devices.all()), 4)
        assert_group_matches_json(self, group, resp.json())

    def test_one_already_in(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(devices=[self.devices[2]])
        group.save()

        resp = self.client.patch(
            f"/api/groups/{group.id}/add_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:3]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(len(group.devices.all()), 1)

    def test_all_already_in(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(
            devices=[self.devices[0], self.devices[1], self.devices[2]]
        )
        group.save()

        resp = self.client.patch(
            f"/api/groups/{group.id}/add_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:3]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(len(group.devices.all()), 3)

    def test_post(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(devices=[self.devices[4]])
        group.save()

        resp = self.client.post(
            f"/api/groups/{group.id}/add_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:3]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEquals(len(group.devices.all()), 1)

    def test_put(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(devices=[self.devices[4]])
        group.save()

        resp = self.client.put(
            f"/api/groups/{group.id}/add_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:3]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEquals(len(group.devices.all()), 1)


class DeleteDevicesGroupTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.devices = DeviceFactory.create_batch(5)
        self.user = UserFactory()
        self.client = APIClient()

    def test_delete_from_empty(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory()
        group.save()

        resp = self.client.patch(
            f"/api/groups/{group.id}/remove_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:3]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(len(group.devices.all()), 0)

    def test_delete_not_empty(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(
            devices=[self.devices[0], self.devices[1], self.devices[2]]
        )
        group.save()

        resp = self.client.patch(
            f"/api/groups/{group.id}/remove_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:2]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(group.devices.all()), 1)
        self.assertEquals(group.devices.first(), self.devices[2])
        assert_group_matches_json(self, group, resp.json())

    def test_not_authenticated(self):
        group = GroupFactory(
            devices=[self.devices[0], self.devices[1], self.devices[2]]
        )
        group.save()

        resp = self.client.patch(
            f"/api/groups/{group.id}/remove_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:2]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_one_not__in(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(
            devices=[self.devices[0], self.devices[1], self.devices[2]]
        )
        group.save()

        resp = self.client.patch(
            f"/api/groups/{group.id}/remove_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[1:4]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(len(group.devices.all()), 3)

    def test_all_in(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(
            devices=[self.devices[0], self.devices[1], self.devices[2]]
        )
        group.save()

        resp = self.client.patch(
            f"/api/groups/{group.id}/remove_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [device.id for device in self.devices[0:3]],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(group.devices.all()), 0)

    def test_post(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(devices=[self.devices[0]])
        group.save()

        resp = self.client.post(
            f"/api/groups/{group.id}/remove_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [self.devices[0].id],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEquals(len(group.devices.all()), 1)

    def test_put(self):
        self.client.force_authenticate(self.user)
        group = GroupFactory(devices=[self.devices[0]])
        group.save()

        resp = self.client.put(
            f"/api/groups/{group.id}/remove_devices/",
            content_type="application/json",
            data=json.dumps(
                {
                    "devices": [self.devices[0].id],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEquals(len(group.devices.all()), 1)
