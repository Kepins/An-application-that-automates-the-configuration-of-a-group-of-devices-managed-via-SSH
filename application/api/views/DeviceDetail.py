from rest_framework import generics

from application.api.serializers.DeviceSerializer import DeviceSerializer
from application.models.Device import Device


class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
