from rest_framework import viewsets

from application.api.serializers.key_pair_serializer import KeyPairSerializer
from application.models.key_pair import KeyPair


class KeyPairViewSet(viewsets.ModelViewSet):
    queryset = KeyPair.objects.all()
    serializer_class = KeyPairSerializer
