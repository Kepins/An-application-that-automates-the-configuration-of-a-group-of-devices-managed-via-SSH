from rest_framework import serializers

from application.models import Group, Script


class RunSerializer(serializers.Serializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    script = serializers.PrimaryKeyRelatedField(queryset=Script.objects.all())
