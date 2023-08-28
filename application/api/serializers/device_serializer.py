from rest_framework import serializers

from application.models.device import Device


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Device
        fields = "__all__"
        extra_kwargs = {
            "port": {"required": True},
            "key_pair": {"required": True},
            "password": {"required": True},
        }
