from rest_framework import generics


from application.models import Script


class ScriptList(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView ):
    queryset = Script.objects.all()
    serializer_class = DeviceSerializer