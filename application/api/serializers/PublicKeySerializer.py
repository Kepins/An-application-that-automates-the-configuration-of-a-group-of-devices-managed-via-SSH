from rest_framework import serializers

from application.models.PublicKey import PublicKey


class PublicKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicKey
        fields = "__all__"
