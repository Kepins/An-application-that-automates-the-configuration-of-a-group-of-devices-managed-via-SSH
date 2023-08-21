from rest_framework import serializers

from application.models.public_key import PublicKey


class PublicKeySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = PublicKey
        fields = "__all__"
