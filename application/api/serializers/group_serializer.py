from rest_framework import serializers

from application.models.group import Group


class GroupSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Group
        fields = "__all__"
        extra_kwargs = {
            "public_key": {"required": True},
            "devices": {"required": True},
        }


class GroupAddDevicesSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    public_key = serializers.ReadOnlyField()

    def validate_devices(self, devices):
        if any(device in self.instance.devices.all() for device in devices):
            raise serializers.ValidationError("At least one device already in group")
        return devices + list(self.instance.devices.all())

    class Meta:
        model = Group
        fields = "__all__"
        extra_kwargs = {
            "devices": {"required": True},
        }
