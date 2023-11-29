from rest_framework import serializers

from application.utils.task_utils import RunScriptStatus


class RunScriptStatusSerializer(serializers.Serializer):
    request_uuid = serializers.UUIDField(required=False)
    device = serializers.IntegerField(min_value=1)
    status = serializers.CharField()
    warnings = serializers.ListField(child=serializers.CharField())
    result_std = serializers.CharField(allow_blank=True)
    result_err = serializers.CharField(allow_blank=True)
