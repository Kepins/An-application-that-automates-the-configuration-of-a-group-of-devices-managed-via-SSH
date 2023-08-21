import factory
import factory.random

from application.models.device import Device
from application.models.public_key import PublicKey
from application.models import Group


def setup_test_environment():
    factory.random.reseed_random("my_seed")
    DeviceFactory.reset_sequence()


class PublicKeyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PublicKey
        django_get_or_create = ("key_content",)

    key_content = "ssh-rsa AABBB3NzaC1yc2EAAAADAQABAAACAQDz+uXxmJnI0vHe9ym2yBSuoOkhStNg4cN2P7gGUD7TFe7KmpAsvS5l7YLcLfdpNSP5oJKdBpoCvn3WCA3xVCg/tZlxMcDfDRnhPEwtLqKEysSe5Djp62nxWzV39AphZcytfZSB3BejhddPWoqH39tkYY7Qk3wa/KBPFVXGghK0bII2yjIQlOrJWWHsa/rC6+7gVq2skPuGlxHeWP4th2twgrBJhql+cw0m71ynx2zdXnZSDD9kG/JcJc2DeB1dD1RTckK/wmghxlsfRJxvB59RJehrKJNwe94n6EGcRLkASzWt/cSmJib0gbhRIoPnU0HELNtqyv0mSuFiz2IF1yeWrd53ufb9+ZiYeJfM99+vIf2nShODat3QeK1OVsMEpz+VGkTPyQcxRUJMQhFG2JBLXpsrNxYnTjXZqjmEDglm44M/YVNEYxyYodGqNgaOlx6v/seNg/swr2Yn9u0f75k90xTIuwnHGjPVjpBvH6f4UXQyOWCtTshyXFRDdsOsXD90EhEuec/+CMjbREGf0v8wp7PxYVOBhPddXQH+RW5YEA1te/ZjPVdTt0P0MhuSLOzQuTZcDISuS2iCSx+nk0QjSh50iHWBafZBva6fvT+6oFtwMYPeFdna5OeMSQ960eS2VIxIIjs34A2aT7YrQwo42JtBIWH8por3SAjwazxm2Q== user@example.com"


class DeviceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Device

    name = factory.Sequence(lambda n: f"Device name {n}")
    hostname = factory.Sequence(lambda n: f"device{1}.example.com")
    port = 22
    public_key = factory.SubFactory(PublicKeyFactory)
    password = None


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"Group name {n}")
    public_key = factory.SubFactory(PublicKeyFactory)

    @factory.post_generation
    def devices(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of devices were passed in, use them
            for device in extracted:
                self.devices.add(device)
