from rest_framework import viewsets

from application.api.serializers.device_serializer import DeviceSerializer
from application.models.device import Device


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.order_by("id")
    serializer_class = DeviceSerializer
