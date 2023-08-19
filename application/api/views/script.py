from rest_framework import generics

from application.api.serializers.script_serializer import ScriptSerializer
from application.models import Script


class ScriptList(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView ):
    queryset = Script.objects.all()
    serializer = ScriptSerializer