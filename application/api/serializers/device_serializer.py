from rest_framework import serializers

from application.models.device import Device


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True, allow_null=True)
    is_password_set = serializers.SerializerMethodField()

    def get_is_password_set(self, obj):
        if obj.password is None:
            return False
        return True

    class Meta:
        model = Device
        fields = "__all__"
        extra_kwargs = {
            "port": {"required": True},
            "key_pair": {"required": True},
            "password": {"required": True},
            "public_key": {"required": True},
        }
