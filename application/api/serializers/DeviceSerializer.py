from rest_framework import serializers

from application.models.Device import Device, PublicKey


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Device
        fields = "__all__"
