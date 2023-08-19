from factory import django, Sequence, PostGenerationMethodCall

from application.models import CustomUser, Script

class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = Sequence(lambda n: "testuser%s@test.com" % n)
    email = Sequence(lambda n: "testuser%s@test.com" % n)
    password = PostGenerationMethodCall("set_password", "password")


class ScriptFactory(django.DjangoModelFactory):
    class Meta:
        model = Script

    name = Sequence(lambda n: "name-%s" % n)
    script = Sequence(lambda n: "test_content-%s" % n)
