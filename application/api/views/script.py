from rest_framework import generics

from application.api.serializers.script_serializer import ScriptSerializer
from application.models import Script


class ScriptListCreateAPIView(generics.ListCreateAPIView):
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer


class ScriptDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer