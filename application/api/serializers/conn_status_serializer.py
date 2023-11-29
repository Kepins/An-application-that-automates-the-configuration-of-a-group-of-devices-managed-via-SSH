from rest_framework import serializers

from application.utils.task_utils import ConnectionStatus


class ConnStatusSerializer(serializers.Serializer):
    request_uuid = serializers.UUIDField(required=False)
    device = serializers.IntegerField(min_value=1)
    status = serializers.CharField()
    warnings = serializers.ListField(child=serializers.CharField())
