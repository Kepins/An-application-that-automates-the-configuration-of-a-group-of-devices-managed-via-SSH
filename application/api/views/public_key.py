from rest_framework import viewsets

from application.api.serializers.public_key_serializer import PublicKeySerializer
from application.models.public_key import PublicKey


class PublicKeyViewSet(viewsets.ModelViewSet):
    queryset = PublicKey.objects.all()
    serializer_class = PublicKeySerializer
