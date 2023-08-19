from factory import django, Sequence, PostGenerationMethodCall

from devices.models.custom_user import CustomUser

class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = Sequence(lambda n: "testuser%s@test.com" % n)
    email = Sequence(lambda n: "testuser%s@test.com" % n)
    password = PostGenerationMethodCall("set_password", "password")
