from rest_framework import serializers

from config.application.models import Device, PublicKey


class PublicKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicKey
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    key_content = serializers.SlugRelatedField(
        slug_field="key_content",
        queryset=PublicKey.objects.all(),
        required=False,
        source="public_key",
        many=False,
    )

    class Meta:
        model = Device
        fields = [
            "id",
            "name",
            "hostname",
            "key_content",
        ]
