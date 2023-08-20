from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from application.api.serializers.group_serializer import (
    GroupSerializer,
    GroupAddDevicesSerializer,
)
from application.models.group import Group


class GroupKeyViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    serializer_add_devices = GroupAddDevicesSerializer

    def get_serializer_class(self):
        if self.action == "add_devices":
            return self.serializer_add_devices
        return self.serializer_class

    @action(detail=True, methods=["POST"])
    def add_devices(self, request, pk):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
