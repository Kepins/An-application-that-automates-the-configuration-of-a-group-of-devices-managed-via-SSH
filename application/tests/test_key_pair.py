import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from application.tests.factories import (
    setup_test_environment,
    KeyPairFactory,
    UserFactory,
)


def assert_key_pair_matches_json(test_case, key_pair, key_pair_json):
    test_case.assertEquals(key_pair_json["id"], key_pair.id)
    test_case.assertEquals(
        key_pair_json["private_key_content"], key_pair.private_key_content
    )
    test_case.assertEquals(
        key_pair_json["public_key_content"], key_pair.public_key_content
    )


class GetPublicKeyListTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_empty(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get(
            "/api/keys/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 0)

    def test_one(self):
        self.client.force_authenticate(self.user)
        key_pair = KeyPairFactory()
        key_pair.save()

        resp = self.client.get(
            "/api/keys/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 1)
        assert_key_pair_matches_json(self, key_pair, resp.json()[0])

    def test_not_authenticated(self):
        key_pair = KeyPairFactory()
        key_pair.save()

        resp = self.client.get(
            "/api/keys/",
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_many(self):
        self.client.force_authenticate(self.user)
        NUM_KEYS = 10
        key_pairs = {}

        for i in range(NUM_KEYS):
            key_pair = KeyPairFactory(
                public_key_content=str(i), private_key_content=str(i)
            )
            key_pair.save()
            key_pairs[key_pair.id] = key_pair

        resp = self.client.get(
            "/api/keys/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), NUM_KEYS)
        for i in range(NUM_KEYS):
            id = resp.json()[i]["id"]
            assert_key_pair_matches_json(self, key_pairs[id], resp.json()[i])


class PostPublicKeyListTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_new(self):
        self.client.force_authenticate(self.user)
        key_pair = KeyPairFactory.build()

        resp = self.client.post(
            "/api/keys/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": key_pair.name,
                    "private_key_content": key_pair.private_key_content,
                    "public_key_content": key_pair.public_key_content,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        key_pair.id = resp.json()["id"]
        assert_key_pair_matches_json(self, key_pair, resp.json())

    def test_not_authenticated(self):
        key_pair = KeyPairFactory.build()

        resp = self.client.post(
            "/api/keys/",
            content_type="application/json",
            data=json.dumps(
                {
                    "private_key_content": key_pair.private_key_content,
                    "public_key_content": key_pair.public_key_content,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # TODO: Think of this testcase
    # def test_exists(self):
    #     key_pair = KeyPairFactory.build()
    #     key_pair.save()
    #
    #     resp = self.client.post(
    #         "/api/keys/",
    #         content_type="application/json",
    #         data=json.dumps(
    #             {
    #                 "private_key_content": key_pair.private_key_content,
    #                 "public_key_content": key_pair.public_key_content,
    #             }
    #         ),
    #     )
    #     self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_content(self):
        self.client.force_authenticate(self.user)
        key_pair = KeyPairFactory.build()
        key_pair.save()

        resp = self.client.post(
            "/api/keys/",
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)


class GetPublicKeyDetail(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_exists(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get(
            "/api/keys/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_exists(self):
        self.client.force_authenticate(self.user)
        key_pair = KeyPairFactory()
        key_pair.save()

        resp = self.client.get(
            f"/api/keys/{key_pair.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        assert_key_pair_matches_json(self, key_pair, resp.json())

    def test_not_authenticated(self):
        key_pair = KeyPairFactory()
        key_pair.save()

        resp = self.client.get(
            f"/api/keys/{key_pair.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PutPublicKeyDetailTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_exists(self):
        self.client.force_authenticate(self.user)
        resp = self.client.put(
            "/api/keys/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_all_fields(self):
        self.client.force_authenticate(self.user)
        key_pair = KeyPairFactory()
        key_pair.save()

        new_key_pair = KeyPairFactory.build(
            public_key_content="12345", private_key_content="54321"
        )

        resp = self.client.put(
            f"/api/keys/{key_pair.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": key_pair.name,
                    "private_key_content": new_key_pair.private_key_content,
                    "public_key_content": new_key_pair.public_key_content,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        new_key_pair.id = resp.json()["id"]
        assert_key_pair_matches_json(self, new_key_pair, resp.json())

    def test_not_authenticated(self):
        key_pair = KeyPairFactory()
        key_pair.save()

        new_key_pair = KeyPairFactory.build(
            public_key_content="12345", private_key_content="54321"
        )

        resp = self.client.put(
            f"/api/keys/{key_pair.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "private_key_content": new_key_pair.private_key_content,
                    "public_key_content": new_key_pair.public_key_content,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PatchPublicKeyDetailTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_exists(self):
        self.client.force_authenticate(self.user)
        resp = self.client.patch(
            "/api/keys/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_all_fields(self):
        self.client.force_authenticate(self.user)
        key_pair = KeyPairFactory()
        key_pair.save()

        new_key_pair = KeyPairFactory.build(
            public_key_content="12345", private_key_content="54321"
        )

        resp = self.client.patch(
            f"/api/keys/{key_pair.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "private_key_content": new_key_pair.private_key_content,
                    "public_key_content": new_key_pair.public_key_content,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        new_key_pair.id = resp.json()["id"]
        assert_key_pair_matches_json(self, new_key_pair, resp.json())

    def test_not_authenticated(self):
        key_pair = KeyPairFactory()
        key_pair.save()

        new_key_pair = KeyPairFactory.build(
            public_key_content="12345", private_key_content="54321"
        )

        resp = self.client.patch(
            f"/api/keys/{key_pair.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "private_key_content": new_key_pair.private_key_content,
                    "public_key_content": new_key_pair.public_key_content,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class DeletePublicKeyDetailTest(APITestCase):
    def setUp(self):
        setup_test_environment()
        self.user = UserFactory()
        self.client = APIClient()

    def test_not_exists(self):
        self.client.force_authenticate(self.user)
        resp = self.client.delete(
            "/api/keys/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_all_fields(self):
        self.client.force_authenticate(self.user)
        key_pair = KeyPairFactory()
        key_pair.save()
        resp = self.client.delete(
            f"/api/keys/{key_pair.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_authenticated(self):
        key_pair = KeyPairFactory()
        key_pair.save()
        resp = self.client.delete(
            f"/api/keys/{key_pair.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)
