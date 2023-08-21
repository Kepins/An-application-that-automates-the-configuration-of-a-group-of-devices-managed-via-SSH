import json

from django.test import TestCase
from rest_framework import status

from application.tests.factories import setup_test_environment, PublicKeyFactory


def assert_public_key_matches_json(test_case, public_key, public_key_json):
    test_case.assertEquals(public_key_json["id"], public_key.id)
    test_case.assertEquals(public_key_json["key_content"], public_key.key_content)


class GetPublicKeyListTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_empty(self):
        resp = self.client.get(
            "/api/keys/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 0)

    def test_one(self):
        public_key = PublicKeyFactory()
        public_key.save()

        resp = self.client.get(
            "/api/keys/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 1)
        assert_public_key_matches_json(self, public_key, resp.json()[0])

    def test_many(self):
        NUM_KEYS = 10
        public_keys = {}

        for i in range(NUM_KEYS):
            public_key = PublicKeyFactory(key_content=str(i))
            public_key.save()
            public_keys[public_key.id] = public_key

        resp = self.client.get(
            "/api/keys/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), NUM_KEYS)
        for i in range(NUM_KEYS):
            id = resp.json()[i]["id"]
            assert_public_key_matches_json(self, public_keys[id], resp.json()[i])


class PostPublicKeyListTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_new(self):
        public_key = PublicKeyFactory.build()

        resp = self.client.post(
            "/api/keys/",
            content_type="application/json",
            data=json.dumps(
                {
                    "key_content": public_key.key_content,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        public_key.id = resp.json()["id"]
        assert_public_key_matches_json(self, public_key, resp.json())

    def test_exists(self):
        public_key = PublicKeyFactory.build()
        public_key.save()

        resp = self.client.post(
            "/api/keys/",
            content_type="application/json",
            data=json.dumps(
                {
                    "key_content": public_key.key_content,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_content(self):
        public_key = PublicKeyFactory.build()
        public_key.save()

        resp = self.client.post(
            "/api/keys/",
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)


class GetPublicKeyDetail(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_not_exists(self):
        resp = self.client.get(
            "/api/keys/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_exists(self):
        public_key = PublicKeyFactory()
        public_key.save()

        resp = self.client.get(
            f"/api/keys/{public_key.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        assert_public_key_matches_json(self, public_key, resp.json())


class PutPublicKeyDetailTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_not_exists(self):
        resp = self.client.put(
            "/api/keys/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_all_fields(self):
        public_key = PublicKeyFactory()
        public_key.save()

        new_public_key = PublicKeyFactory.build(key_content="12345")

        resp = self.client.put(
            f"/api/keys/{public_key.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "key_content": new_public_key.key_content,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        new_public_key.id = resp.json()["id"]
        assert_public_key_matches_json(self, new_public_key, resp.json())


class PatchPublicKeyDetailTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_not_exists(self):
        resp = self.client.patch(
            "/api/keys/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_all_fields(self):
        public_key = PublicKeyFactory()
        public_key.save()

        new_public_key = PublicKeyFactory.build(key_content="12345")

        resp = self.client.patch(
            f"/api/keys/{public_key.id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "key_content": new_public_key.key_content,
                }
            ),
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        new_public_key.id = resp.json()["id"]
        assert_public_key_matches_json(self, new_public_key, resp.json())


class DeletePublicKeyDetailTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def test_not_exists(self):
        resp = self.client.delete(
            "/api/keys/1/",
        )
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_all_fields(self):
        public_key = PublicKeyFactory()
        public_key.save()
        resp = self.client.delete(
            f"/api/keys/{public_key.id}/",
        )
        self.assertEquals(resp.status_code, status.HTTP_204_NO_CONTENT)
