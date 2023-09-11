from rest_framework import serializers

from application.utils.task_utils import ConnectionStatus


class RunScriptStatusSerializer(serializers.Serializer):
    request_uuid = serializers.UUIDField(required=False)
    device = serializers.IntegerField(min_value=1)
    status = serializers.ChoiceField(choices=[(e.value, e.name) for e in ConnectionStatus])
    warnings = serializers.ListField(child=serializers.CharField())
