from rest_framework import serializers

from application.models.device import Device


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True, allow_null=True)

    class Meta:
        model = Device
        fields = "__all__"
        extra_kwargs = {
            "port": {"required": True},
            "key_pair": {"required": True},
            "password": {"required": True},
        }
