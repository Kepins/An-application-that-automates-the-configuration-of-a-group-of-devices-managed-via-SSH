import factory
from factory import random, Sequence, PostGenerationMethodCall

from application.models import Group, CustomUser, Script, KeyPair, Device


def setup_test_environment():
    random.reseed_random("my_seed")
    DeviceFactory.reset_sequence()


class KeyPairFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KeyPair
        django_get_or_create = (
            "public_key_content",
            "private_key_content",
        )

    public_key_content = "ssh-rsa AABBB3NzaC1yc2EAAAADAQABAAACAQDz+uXxmJnI0vHe9ym2yBSuoOkhStNg4cN2P7gGUD7TFe7KmpAsvS5l7YLcLfdpNSP5oJKdBpoCvn3WCA3xVCg/tZlxMcDfDRnhPEwtLqKEysSe5Djp62nxWzV39AphZcytfZSB3BejhddPWoqH39tkYY7Qk3wa/KBPFVXGghK0bII2yjIQlOrJWWHsa/rC6+7gVq2skPuGlxHeWP4th2twgrBJhql+cw0m71ynx2zdXnZSDD9kG/JcJc2DeB1dD1RTckK/wmghxlsfRJxvB59RJehrKJNwe94n6EGcRLkASzWt/cSmJib0gbhRIoPnU0HELNtqyv0mSuFiz2IF1yeWrd53ufb9+ZiYeJfM99+vIf2nShODat3QeK1OVsMEpz+VGkTPyQcxRUJMQhFG2JBLXpsrNxYnTjXZqjmEDglm44M/YVNEYxyYodGqNgaOlx6v/seNg/swr2Yn9u0f75k90xTIuwnHGjPVjpBvH6f4UXQyOWCtTshyXFRDdsOsXD90EhEuec/+CMjbREGf0v8wp7PxYVOBhPddXQH+RW5YEA1te/ZjPVdTt0P0MhuSLOzQuTZcDISuS2iCSx+nk0QjSh50iHWBafZBva6fvT+6oFtwMYPeFdna5OeMSQ960eS2VIxIIjs34A2aT7YrQwo42JtBIWH8por3SAjwazxm2Q== user@example.com"
    private_key_content = "1234"


class DeviceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Device

    name = factory.Sequence(lambda n: f"Device name {n}")
    hostname = factory.Sequence(lambda n: f"device{1}.example.com")
    port = 22
    key_pair = factory.SubFactory(KeyPairFactory)
    password = None


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"Group name {n}")
    key_pair = factory.SubFactory(KeyPairFactory)

    @factory.post_generation
    def devices(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of devices were passed in, use them
            for device in extracted:
                self.devices.add(device)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = Sequence(lambda n: "testuser%s@test.com" % n)
    email = Sequence(lambda n: "testuser%s@test.com" % n)
    password = PostGenerationMethodCall("set_password", "password")


class ScriptFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Script

    name = Sequence(lambda n: "name-%s" % n)
    script = Sequence(lambda n: "test_content-%s" % n)
