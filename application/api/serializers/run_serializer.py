from rest_framework import serializers

from application.models import Group, Script


class RunSerializer(serializers.Serializer):
    script = serializers.PrimaryKeyRelatedField(queryset=Script.objects.all())
