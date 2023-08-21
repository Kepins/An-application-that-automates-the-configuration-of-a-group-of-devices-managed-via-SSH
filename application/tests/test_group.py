import json

from django.test import TestCase
from rest_framework import status

from application.tests.factories import (
    setup_test_environment,
    GroupFactory,
    DeviceFactory,
)


def assert_group_matches_json(test_case, group, group_json):
    test_case.assertEquals(group_json["id"], group.id)
    test_case.assertEquals(group_json["name"], group.name)
    if group.public_key:
        test_case.assertEquals(group_json["public_key"], group.public_key.id)
    else:
        test_case.assertEquals(group_json["public_key"], None)
    test_case.assertEquals(len(group.devices.all()), len(group_json["devices"]))
    for device_id in group_json["devices"]:
        test_case.assertTrue(group.devices.filter(pk=device_id).exists())


class GetGroupListTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_empty(self):
        resp = self.client.get(
            "/api/groups/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 0)

    def test_one(self):
        group = GroupFactory(devices=[DeviceFactory(port=2222)])
        group.save()

        resp = self.client.get(
            "/api/groups/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 1)
        assert_group_matches_json(self, group, resp.json()[0])

    def test_many(self):
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


class PostGroupListTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_empty_device_list(self):
        group = GroupFactory.build()

        resp = self.client.post(
            "/api/groups/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": group.name,
                    "public_key": None,
                    "devices": [],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        group.id = resp.json()["id"]
        assert_group_matches_json(self, group, resp.json())

    def test_not_empty_device_list(self):
        group = GroupFactory.build()
        devices = [DeviceFactory(name="Device1111"), DeviceFactory(port=2222)]

        resp = self.client.post(
            "/api/groups/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": group.name,
                    "public_key": None,
                    "devices": [device.id for device in devices],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        group.id = resp.json()["id"]
        assert_group_matches_json(self, group, resp.json())

    def test_no_device_list(self):
        group = GroupFactory.build()

        resp = self.client.post(
            "/api/groups/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": group.name,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_pub_key(self):
        group = GroupFactory.build()

        resp = self.client.post(
            "/api/groups/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": group.name,
                    "public_key": 1,
                    "devices": [],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)


class GetDeviceDetailTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_not_exists(self):
        resp = self.client.get(
            "/api/groups/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_exists(self):
        group = GroupFactory()
        group.save()

        resp = self.client.get(
            f"/api/groups/{group.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        assert_group_matches_json(self, group, resp.json())


class PutDeviceDetailTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_not_all_fields(self):
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
        group = GroupFactory()
        group.save()
        new_group = GroupFactory.build(name="NEW NAME")

        resp = self.client.put(
            f"/api/groups/{group.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_group.name,
                    "public_key": None,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_all_fields(self):
        group = GroupFactory()
        group.save()
        new_group = GroupFactory.build(name="NEW NAME", public_key=None)
        devices = [DeviceFactory(name="Device1111"), DeviceFactory(port=2222)]

        resp = self.client.put(
            f"/api/groups/{group.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": new_group.name,
                    "public_key": new_group.public_key,
                    "devices": [device.id for device in devices],
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        new_group.id = resp.json()["id"]
        assert_group_matches_json(self, new_group, resp.json())


class PatchDeviceDetailTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_not_all_fields(self):
        group = GroupFactory()
        group.save()
        new_group = GroupFactory.build(name="NEW NAME", public_key=group.public_key)

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


class DeleteDeviceDetailTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_not_exists(self):
        resp = self.client.delete(
            "/api/groups/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_exists(self):
        group = GroupFactory()
        group.save()

        resp = self.client.delete(
            f"/api/groups/{group.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_204_NO_CONTENT)


class AddDevicesGroupTest(TestCase):
    def setUp(self):
        setup_test_environment()
        self.devices = DeviceFactory.create_batch(5)

    def test_add_to_empty(self):
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

    def test_add_to_not_empty(self):
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


class DeleteDevicesGroupTest(TestCase):
    def setUp(self):
        setup_test_environment()
        self.devices = DeviceFactory.create_batch(5)

    def test_delete_from_empty(self):
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

    def test_one_not__in(self):
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
