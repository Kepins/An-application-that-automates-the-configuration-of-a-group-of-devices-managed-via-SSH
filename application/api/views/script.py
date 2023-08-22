from rest_framework import viewsets

from application.api.serializers.script_serializer import ScriptSerializer
from application.models import Script


class ScriptViewSet(viewsets.ModelViewSet):
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer
