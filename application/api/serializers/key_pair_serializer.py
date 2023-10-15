from rest_framework import serializers

from application.models.key_pair import KeyPair


class KeyPairSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    private_key_content = serializers.CharField(write_only=True)

    class Meta:
        model = KeyPair
        fields = "__all__"
