from rest_framework import serializers


class ConnStatusSerializer(serializers.Serializer):
    request_uuid = serializers.UUIDField(required=False)
    device = serializers.IntegerField(min_value=1)
    status = serializers.CharField()
    warnings = serializers.ListField(child=serializers.CharField())
