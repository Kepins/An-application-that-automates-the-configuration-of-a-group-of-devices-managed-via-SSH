from rest_framework import generics


from application.api.serializers.DeviceSerializer import DeviceSerializer
from application.models.Device import Device


class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
