from rest_framework import serializers

from application.models.Device import Device, PublicKey


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
